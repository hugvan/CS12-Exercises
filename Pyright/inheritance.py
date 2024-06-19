class A:
    def f(self):
        print("A's f was called")
 
    def g(self):
        print("A's g was called")
 

 
class B(A):
    def f(self):
        print("B's f was called")

    def g(self):
        print("B's g was called")
 
 
class C(B):
    def f(self):
        print("C's f was called")
        b1 = super()
        b2 = B()
        print(b1.__class__)
        print(b2.__class__)
        super().f()

class D():
    def f(self):
        print("D's f was called")

class E(D):
    def f(self):
        print("E's f was called")


b = B()


print('---')
 
c = C()

c.f()

