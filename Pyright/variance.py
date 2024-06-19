
class A:
    def f(self, x: int | float):
        print(x * 2)
 
class B1(A):
    def f(self, x: int | str | float):
        ...

 
class B3(A):
    def f(self, x: int | float):
        ...

a_obj = A()
b1_obj = B1()

def func(obj: A):
    obj.f(3.5)
