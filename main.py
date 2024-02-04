from flask import Flask, request, jsonify
import base_classes as bc
import json
from datetime import datetime, timedelta

app = Flask(__name__)

room = bc.Room(bc.UserPool(), bc.RoomConfig())
room.start_loop()

@app.route("/list")
def index():
    target_str = ""
    for user in room.user_pool.users.values():
        target_str += f"[{user.user_config.display_name}, {user.last_awake}]"
    room.user_pool.del_users_after_last_awake(datetime.now() - timedelta(seconds=300))
    return target_str, 200

@app.route("/join", methods=['POST'])
def join():
    body_json = request.get_json()
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr

    remote_location = bc.RemoteLocation(user_ip, request.environ["REMOTE_PORT"])
    name = body_json["name"]

    new_user = room.user_pool.add_user(remote_location, bc.UserConfig(name, 0))

    return new_user.uuid.hex(), 200
    
@app.route("/play", methods=['POST'])
def play():

    body_json = request.get_json()

    if ((current_user := room.user_pool.get_user_by_uuid(bytes.fromhex(body_json["user_hex"]))) == None):
        return "Invalid Session", 400
    
    match(body_json["type"]):

        case "wake":
            current_user.last_awake = datetime.now()
            return "Session Refreshed", 200
        
        case "context":
            return str(room.room_context['value']), 200

            


if __name__ == '__main__':
    app.run()