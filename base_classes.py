from flask import Flask, Request
import time, threading
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass

class RemoteLocation:

    def __init__(self, addr:str, port:int) -> None:
        self.addr = addr
        self.port = port
    
    def __eq__(self, other):
        return (self.addr, self.port) == (other.addr, other.port)
    
    def __str__(self):
        return f"{self.addr}:{self.port}"
    
    def __repr__(self):
        return str(self)

class UserConfig:

    def __init__(self, display_name:str, color_id:int) -> None:
        self.display_name = display_name
        self.color_id = color_id

    def __str__(self):
        return f"[{self.display_name},{self.color_id}]"
    
    def __repr__(self):
        return str(self)

@dataclass
class RoomConfig:
    can_join:bool = True
    

class User:

    def generate_uuid(self):
        self.uuid = uuid.uuid4().bytes

    def __init__(self, remote_location:RemoteLocation, user_config:UserConfig, last_awake:datetime = None, data:dict = None) -> None:

        if last_awake == None:
            last_awake = datetime.now()

        self.generate_uuid()
        self.remote_location = remote_location
        self.user_config = user_config
        self.last_awake = last_awake
        self.data = data

    def __repr__(self) -> str:
        return f'{self.uuid.hex()},{self.remote_location},{self.user_config},{self.last_awake}'


class UserPool:

    def __init__(self, users:dict[bytes,User] = {}):
        self.users = users

    def add_user(self, remote_location:RemoteLocation, user_config:UserConfig):
        new_user = User(remote_location, user_config)

        while new_user.uuid in self.users:
            new_user.generate_uuid()

        self.users[new_user.uuid] = new_user

        return new_user
    
    def del_user_by_uuid(self, uuid:bytes):
        self.users.pop(uuid)
        
    def del_users_after_last_awake(self, expiry_time:datetime):
        for users_key in list(self.users.keys())[:]:
            if self.users[users_key].last_awake <= expiry_time:
                self.del_user_by_uuid(users_key)

    def get_user_by_uuid(self, uuid:bytes):
        return self.users[uuid]
    
    def search_user_by_remote_location(self, remote_location:RemoteLocation):
        for user in self.users.values():
            if user.remote_location == remote_location:
                return user
        return None
    
class Channels:

    def __init__(self, config:dict[str, dict]) -> None:
        self.config = config
        self.channels:dict[str, list] = {}

        self.set_channels()

    def set_channels(self):
        self.channels = {}
        for channel_key in self.config.keys():
            self.channels[channel_key] = []

    def send_data(self, channel_key, sender_key, data):

        if not channel_key in self.channels:
            return None
        
        channel_config = self.config[channel_key]

        if not channel_config["open"]:
            print(1)
            return None
        
        if len(self.channels[channel_key]) >= channel_config["max_length"]:
            print(2)
            return None
        
        if channel_config["whitelist"] ^ (sender_key in channel_config["use_list"]):
            print(3)
            return None

        if (not channel_config["allow_duplicate"]) ^ (sender_key in self.channels[channel_key]):
            print(4)
            return None
        
        sendant = (sender_key, datetime.now(), data)
        self.channels[channel_key].append(sendant)
        return sendant



QA = [
    {
        "question" : "What is Love?",
        "options" : {
            0 : "Baby",
            1 : "Yes",
            2 : "No",
            3 : "Bruh"
        },
        "correct" : [ 0 ,]
    },
    {
        "question" : "2 + 2?",
        "options" : {
            0 : "1",
            1 : "2",
            2 : "3",
            3 : "4"
        },
        "correct" : [ 3 ,]
    },
    {
        "question" : "5 * 5?",
        "options" : {
            0 : "16",
            1 : "25",
            2 : "36",
            3 : "49"
        },
        "correct" : [ 1 ,]
    },
    {
        "question" : "12 / 2?",
        "options" : {
            0 : "2",
            1 : "3",
            2 : "6",
            3 : "12"
        },
        "correct" : [ 2 ,]
    },
]
    
class Room:

    def __init__(self, user_pool:UserPool, room_config:RoomConfig, channels:Channels, room_context:dict = {} ):
        self.user_pool = user_pool
        self.room_config = room_config
        self.room_context = room_context
        self.channels = channels

    def main_loop(self):
        while True:

            _tick = 0.05
            _timer = 0
            for user in self.user_pool.users.values():
                if user.data is None:
                    user.data = {}
                user.data["score"] = 0

            for question in QA:

                while _timer <= 1:

                    self.room_context["default"] = question["question"]

                    _timer += _tick
                    time.sleep(_tick)

                _timer = 0
                while _timer <= 3:

                    self.room_context["default"] = str(question["options"])

                    _timer += _tick
                    time.sleep(_tick)

                _timer = 0
                for response in self.channels.channels["answer"]:

                    if response[2] in question["correct"]:
                        self.user_pool.get_user_by_uuid(response[0]).data["score"] += 100
                        print(self.user_pool.get_user_by_uuid(response[0]).user_config.display_name)

                self.channels.channels["answer"] = []

    def start_loop(self):
        threading.Thread(target=self.main_loop).start()


    


    
