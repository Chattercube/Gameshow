from datetime import datetime, timedelta
import asyncio

for x in (False, True):
    for y in (False, True):
        print(x, y, x & y)


x = ['a', 'b', 'c']
print(False ^ ('a' in x))

print(timedelta(seconds=30) / timedelta(seconds=2))

async def fun1():
    print("Hello World")
    await asyncio.sleep(1)
    print("Not Hello World")

async def fun2():
    print("Hello World2")
    await asyncio.sleep(1)
    print("Not Hello World2")
        

asyncio.run(fun1())
asyncio.run(fun2())

