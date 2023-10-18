# def my_generator():
#     r = 0
#     for i in range(5):
#         r += 1
#         yield i

# def a():
#     yield from my_generator()
#     print(1)

def my_generator():
    r = 0
    for i in range(5):
        r += 1
        yield i
    return r

def a():
    r = yield from my_generator()
    print(r)
    print(1)

for item in a():
    print(item)