def gen(i:int):
    for item in range(20):
        yield gen(item)