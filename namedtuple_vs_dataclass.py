import json
from collections import namedtuple
from dataclasses import dataclass
from unittest import TestCase

# If we simply want an object to store data and we don't want mutability,
# better equivalence checking, or custom methods then a namedtuple suffices.
# If we *do* want the above, then we could use a dataclass.
CoolGuy = namedtuple(typename="CoolGuy", field_names=("shades", "cars"))
chirag = CoolGuy(shades=True, cars=("Ferrari", "Lambo"))

print(f"This is a namedtuple object: {chirag}")
print(f"Type of namedtuple: {type(chirag)}")
print(f"JSON dump of namedtuple object: {json.dumps(chirag)}")


# Implementing the same in a dataclass.
@dataclass
class CoolGuyDataClass():
    shades: bool
    cars: tuple


class CoolGuyDataClassEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, CoolGuyDataClass):
            return vars(obj)
        return super().default(obj)


angelica = CoolGuyDataClass(shades=False, cars=("Merc", "BMW", "Ferrari"))
print(f"This is a dataclass object: {angelica}")

print("JSON dump of dataclass object using a custom encoder:"
      f"{json.dumps(angelica, cls=CoolGuyDataClassEncoder)}")

print("This is a JSON dump of the same but with a default callable for json.dumps: "
      f"{json.dumps(angelica, default=lambda obj: vars(obj))}")

# Check that serialization with the default encoder raises TypeError for this custom class object.
with TestCase.assertRaises({}, TypeError):
    json.dumps(angelica)

# Can we simple create  a custom encoder for namedtuples instead of using a dataclass?
class NamedTupleEncoder(json.JSONEncoder):

    def default(self, obj):
        # More on this below.
        print("I am never called unless you do some trickery!")
        if isinstance(obj, CoolGuy):
            # Tuples have no __dict__ attribute
            # so vars() raises an AttributeError.
            # This requires use of a private method
            # which creates a new dict.
            return obj._asdict()
        return super().default(obj)

# If a class inherits from a built-in type, such as tuple,
# JSONEncoder's iterencode (which is called by its encode method, called by json.dumps),
# will end up calling an internal method to serialize the built-in
# type. In the case of a tuple, this is the _iterencode_list method:
# https://github.com/python/cpython/blob/088a15c49d99ecb4c3bef93f8f40dd513c6cae3b/Lib/json/encoder.py#L277
# Therefore, the default method of the custom class will never actually be called.
print("Here's what a custom JSON encoder looks like with a namedtuple: "
      f"{json.dumps(chirag, cls=NamedTupleEncoder)}")

# Just to prove this, we can monkey patch JSONEncoder.iterencode to call `default()` and convert to
# string instead.
json.JSONEncoder.iterencode = lambda self, o, _one_shot: str(NamedTupleEncoder().default(o))
print("This now works by monkey patching: ",
      f"{json.dumps(chirag, cls=NamedTupleEncoder)}")

