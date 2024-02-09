from base_classes import InputWrapper, OutputWrapper, Room, RoomConfig, UserPool

IWRAP_CONFIG = {

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

OWRAP_CONFIG = {

    "default":{
        "open" : True,
        "whitelist" : False,
        "use_list" : [],
    }

}

class QuizGameRoom(Room):

    def __init__(self, user_pool: UserPool, room_config: RoomConfig, iwrap: InputWrapper, owrap: OutputWrapper):
        super().__init__(user_pool, room_config, InputWrapper(IWRAP_CONFIG), OutputWrapper(OWRAP_CONFIG))

