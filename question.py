from dataclasses import dataclass

@dataclass
class Poll:
    ask_duration:int = 10
    answer_duration:int = 30

    question:str = "How much is a dozen?"

    choices:dict = {
        0 : "10",
        1 : "11",
        2 : "12",
        3 : "13"
    }

    
