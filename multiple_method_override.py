"""
                    object
                    /   \
                Base    Unexpected
                /  \   /
           Child    Other
             \      /
              SubChild

"""
class BaseClass:

    def method(self):
        print('base class')


class ChildClass(BaseClass):

    def method(self):
        print('child class')

class UnexpectedClass:

    def method(self):
        print("I was unexpected")

class OtherChildClass(BaseClass, UnexpectedClass):

    def method(self):
        print('Other child class')


class SubChildClass(ChildClass, OtherChildClass):
    pass


obj = SubChildClass()
# This will call ChildClass's method.
obj.method()

print(SubChildClass.mro())
SubChildClass.mro = lambda: [OtherChildClass]

# The mro will have changed.
print(SubChildClass.mro())

# But the method call will still be the same.
# This is because the mro is read-only.
# We must override the mro method in a metaclass.
obj.method()

