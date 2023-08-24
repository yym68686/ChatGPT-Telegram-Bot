name = 'Alice'

def example():
    global name
    # ⛔️ UnboundLocalError: local variable 'name' referenced before assignment
    print(name)

    name = 'Bob' # 👈️ this makes the variable local

def example1():
    global name
    # ⛔️ UnboundLocalError: local variable 'name' referenced before assignment
    print(name)

    name = 'Bob' # 👈️ this makes the variable local


example()
example1()
