def counter():
    x = 0
 
    def incr():
        nonlocal x  # What will happen if the line
        x += 1      # `nonlocal x` is removed?
        return x
 
    return incr
 
f = counter()
print(f())
print(f())
print(f())
print(counter()())
print(counter()())
