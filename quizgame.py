from base_classes import InputWrapper, OutputWrapper, Room, RoomConfig, UserPool
import time, threading
from enum import Enum
import json
from datetime import datetime, timedelta

class Perm(Enum):
    HOST = 1 << 1
    ADMIN = 1 << 2

def lerp (a, b, t):
    return a + (b-a) * t

def clamp (s, f, v):
    if v < s: return s
    if v > f: return f
    return v

IWRAP_CONFIG = {

    "control" : {

        "open" : True,
        "whitelist" : False,
        "use_list" : [],
        "max_length" : 1,
        "allow_duplicate" : True

    },

    "answer" : {

        "open" : True,
        "whitelist" : False,
        "use_list" : [],
        "max_length" : 10,
        "allow_duplicate" : False
        
    }

}

OWRAP_CONFIG = {

    "default":{
        "open" : True,
        "whitelist" : False,
        "use_list" : [],
    }

}

USERSTAT_CONFIG = {

    "score":{
        "visible_self": True,
        "default": 0
    },

    "streak":{
        "visible_self": True,
        "default" : 0
    },

    "perm":{
        "visible_self" : True,
        "default": 0
    }

}

class QuizGameRoom(Room):

    def __init__(self, room_config: RoomConfig, game_config: dict):
        super().__init__(UserPool(USERSTAT_CONFIG), room_config, InputWrapper(IWRAP_CONFIG), OutputWrapper(OWRAP_CONFIG))
        self.game_config = game_config

    def main_loop(self):

        _timer = 0
        _tick = 0.05

        while True:

            while True:

                if len(self.iwrap.channels["control"]) > 0:
                    if self.iwrap.channels["control"].pop(0)[2] == "start":
                        break

                display = {

                    "title" : self.game_config["general"]["title"],
                    "author" : self.game_config["general"]["author"],    
                    "page" : "lobby",
                    "playerlist" : [ 
                        {
                            "name" : user.user_config.display_name,
                            "score" : user.stats["score"]
                        }

                        for user in self.user_pool.users.values()
                    ]
                }

                self.owrap.set_output("default", display)
                _timer += _tick
                time.sleep(_tick)

            slides = self.game_config["slides"][:]

            while len(slides) > 0:

                slide = slides.pop(0)

                _timer = 0

                while _timer < slide["title_card_duration"]:
                    
                    display = {

                    "page" : "q_card",
                    "q_label" : slide["q_label"],
                    "q_img" : slide["q_img"],
                    "timer" : _timer,
                    "timer_end" : slide["title_card_duration"]

                    }

                    self.owrap.set_output("default", display)
                    _timer += _tick
                    time.sleep(_tick)

                _timer = 0
                self.iwrap.channels["answer"].clear()
                start_time = datetime.now()

                while _timer < slide["question_duration"] and len(self.iwrap.channels["answer"]) < len(self.user_pool.users):
                    
                    display = {

                    "page" : "q_card",
                    "q_label" : slide["q_label"],
                    "q_img" : slide["q_img"],
                    "options" : [ option for option in slide["options"] ],
                    "response_no" : len(self.iwrap.channels["answer"]),
                    "timer" : _timer,
                    "timer_end" : slide["question_duration"]

                    }

                    print(display)

                    self.owrap.set_output("default", display)
                    _timer += _tick
                    time.sleep(_tick)

                for answer in self.iwrap.channels["answer"][:]:
                    if answer[2] in slide["option_sets"]["correct"]:
                        print(clamp(0, 1, (answer[1] - start_time) / timedelta(seconds=slide["question_duration"])))
                        player = self.user_pool.get_user_by_uuid(answer[0])
                        score_added = lerp(self.game_config["gameplay"]["speed_score_multi"][0], self.game_config["gameplay"]["speed_score_multi"][1], clamp(0, 1, (answer[1] - start_time) / timedelta(seconds=slide["question_duration"]))) * self.game_config["gameplay"]["base_score"]

                        player.stats["score"] += score_added
                        player.stats["streak"] += 1

                    else:

                        player = self.user_pool.get_user_by_uuid(answer)
                        player.stats["streak"] = 0





                _timer = 0
                while _timer < 20:

                    display = {

                    "page" : "a_card",
                    "q_label" : slide["q_label"],
                    "q_img" : slide["q_img"],
                    "options" : [ option for option in slide["options"] ],
                    "correct" : slide["option_sets"]["correct"],
                    "response_no" : len(self.iwrap.channels["answer"]),
                    "timer" : _timer,
                    "timer_end" : slide["question_duration"]

                    }

                    self.owrap.set_output("default", display)
                    _timer += _tick
                    time.sleep(_tick)



            
        return super().main_loop()
    

