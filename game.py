import time, threading

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

channel_config = {

    "control" : {

        "open" : True,
        "blacklist" : True,
        "use_list" : [],
        "max_length" : 10,
        "allow_duplicate" : True

    },

    "answer" : {

        "open" : True,
        "blacklist" : True,
        "use_list" : [],
        "max_length" : 10,
        "allow_duplicate" : True
        
    }

}


class Channels:

    def __init__(self, config:dict[str, dict]) -> None:
        self.config = config
        self.channels:dict[str, list] = {}

        self.set_channels()

    def set_channels(self):
        self.channels = {}
        for channel_key in channel_config.keys():
            self.channels[channel_key] = []

    def send_data(self, channel_key, sender_key, data):

        if not channel_key in self.channels:
            return None
        
        channel_config = self.config[channel_key]

        if not channel_config["open"]:
            return None
        
        if len(self.channels[channel_key]) >= channel_config["max_length"]:
            return None
        
        if channel_config["blacklist"] ^ (sender_key in channel_config["use_list"]):
            return None

        if channel_config["allow_duplicate"] ^ (sender_key in self.channels[channel_key]):
            return None
        
        sendant = (sender_key, data)
        self.channels[channel_key].append(sendant)
        return sendant


class SimpleGame:

    def main_loop(self):

        while True:

            _timer = 0
            _tick = 0.05

            while _timer <= 10:

                print(f'Time Left : {_timer:.2f}, Received Answers : {QA[1]["question"]}')

                _timer += _tick
                time.sleep(_tick)
            
            while _timer <= 20:

                print(f'Time Left : {_timer:.2f}, Received Answers : {QA[1]["options"]}')

                _timer += _tick
                time.sleep(_tick)
            
            while _timer <= 10:
                pass

    def __init__(self, channels=dict[str, ]):
        pass


