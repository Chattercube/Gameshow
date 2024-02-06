for x in (False, True):
    for y in (False, True):
        print(x, y, x & y)


x = ['a', 'b', 'c']
print(False ^ ('a' in x))