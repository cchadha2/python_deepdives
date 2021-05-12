# Quick demo of when/how to use __new__ vs __init__.
class MyClass:
    def __str__(self):
        return str(self.__dict__)


# Check that class is created correctly.
print(MyClass)
obj = MyClass()
print(obj)


# Extend the class and add a parameter to __new__ and add an __init__.
class ExtensionClass(MyClass):
    def __new__(cls, param, *args, **kwargs):
        instance = super().__new__(cls)
        instance.children = [None] * param
        return instance

    def __init__(self, first_child, *args, **kwargs):
        self.children[0] = first_child

obj = ExtensionClass(param=5, first_child=3)
print(obj)


# Make sure that extending this works correctly.
class ExtendAgain(ExtensionClass):
    def __init__(self, second_child, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children[1] = second_child


# Uses 7 for param and second_child because any arguments to __new__ after cls are passed to __init__
# after object is instantiated (i.e. __new__ is called with param=7 and then __init__ is called
# with second_child=7 and first_child=2 if positional arguments are used like below).
# See more here:
# https://docs.python.org/3/reference/datamodel.html#basic-customization
obj = ExtendAgain(7, 2)
print(obj)

# We can also use keyword arguments to differentiate between the arguments used by __new__
# and __init__.
print(ExtendAgain(first_child=1, second_child=4, param=9))


# However, defining the children list in init makes more sense since we don't have to worry
# about the above behaviour.
class OtherExtensionClass(MyClass):
    def __init__(self, param, first_child, second_child):
        self.children = [None] * param
        self.children[0] = first_child
        self.children[1] = second_child

obj = OtherExtensionClass(5, "hey", "hi")
print(obj)

# We might want to use __new__ when we want to customise behaviour of immutable types such as int
# or str. We could also use it where we wanted our objects to be initialized with an empty list
# and we didn't want to rely on any subclasses calling __init__ to create that list.
# Another common application is in custom metaclasses to customize instance creation.
# Usually though, it makes sense simply to use __init__.
