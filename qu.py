import time, threading

_tick = 0.05
_timer = 0

_answers = []


def foo_loop():
    while True:
        _answers.append("X")
        time.sleep(2)

threading.Thread(target=foo_loop).start()

while _timer <= 10:

    print(f"Time Left : {_timer:.2f}, Received Answers : {len(_answers)}")

    _timer += _tick
    time.sleep(_tick)

