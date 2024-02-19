from flask import Flask, request, jsonify
import base_classes as bc
import json
from datetime import datetime, timedelta
from quizgame import QuizGameRoom

channel_config = {

    "control" : {

        "open" : True,
        "whitelist" : False,
        "use_list" : [],
        "max_length" : 10,
        "allow_duplicate" : True

    },

    "answer" : {

        "open" : True,
        "whitelist" : False,
        "use_list" : [],
        "max_length" : 10,
        "allow_duplicate" : True
        
    }

}



app = Flask(__name__)

def js_r(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)

room = QuizGameRoom(bc.RoomConfig(), js_r("quizgame.json"))
roomset = bc.RoomSet()
room.start_loop()

e, key = roomset.add_room(room)
print(key)

@app.route('/')
def page():
    return open("webpage/login_page.html").read(),200

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

    e, new_user = room.user_pool.add_user(remote_location, bc.UserConfig(name, 0))

    return {"uuid" : new_user.uuid.hex(), "secret" : new_user.secret.hex()}, 200
    
@app.route("/play", methods=['POST'])
def play():

    body_json = request.get_json()

    e, room = roomset.get_room_by_code(body_json["room_code"])

    if room is None:
        return "Invalid Room", 400

    if ((current_user := room.user_pool.get_user_by_uuid(bytes.fromhex(body_json["user_hex"]))) == None):
        return "Invalid Session", 400
    
    if (bytes.fromhex(body_json["user_secret"]) != current_user.secret):
        return "Forbidden", 400
    
    match(body_json["type"]):

        case "wake":
            current_user.last_awake = datetime.now()
            return "Session Refreshed", 200
        
        case "input":
            e, q = room.iwrap.send_input(body_json["context"]["channel_key"], bytes.fromhex(body_json["user_hex"]), body_json["context"]["data"])
            return ("Sent", 200) if not q is None else ("Error", 400)

        case "output":
            e, q = room.owrap.get_output(body_json["context"]["channel_key"], bytes.fromhex(body_json["user_hex"]))
            return q, 200
        
        case "stat":
            e, q = room.user_pool.get_stat(bytes.fromhex(body_json["user_hex"]), body_json["context"]["channel_key"])
            return (q,200) if e is None else ("Forbidden", 200)


if __name__ == '__main__':
    app.run(port=5001)