from datetime import datetime, timedelta
for x in (False, True):
    for y in (False, True):
        print(x, y, x & y)


x = ['a', 'b', 'c']
print(False ^ ('a' in x))

print(timedelta(seconds=30) / timedelta(seconds=2))