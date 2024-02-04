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
    
class Room:

    def __init__(self, user_pool:UserPool, room_config:RoomConfig, room_context:dict = {}):
        self.user_pool = user_pool
        self.room_config = room_config
        self.room_context = room_context

    def main_loop(self):
        while True:
            self.room_context["value"] = 2
            time.sleep(1)
            self.room_context["value"] = 10
            time.sleep(1)
        
    def start_loop(self):
        threading.Thread(target=self.main_loop).start()


    


    
