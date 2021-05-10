"""Investigate garbage collection for object attributes."""
import gc
import weakref


class Node:

    def __repr__(self):
        return f"Node({vars(self)}, {id(self)})"


# Make sure node class works as expected.
obj = Node()
obj.left = 45
print("Check that Node object is created correctly: ", obj, end="\n\n")

del obj.left

# Create references to other Node objects in obj.
obj.child = Node()
child_one = weakref.ref(obj.child)

obj.child.child = Node()

# Confirms that children are new objects (different memory addresses).
print("Check references to objects in module namespace: ", vars(), end="\n\n")

# Check references to objects.
print("Parent node object holds a reference to first child as `child` attribute: ", gc.get_referrers(obj.child))


# Remove reference to middle child.
print("Weak reference to first child resolves: ", child_one())
print("Setting child of parent node to be child of child instead.")
obj.child = obj.child.child
print("Weak reference to first child now resolves to None as it has been garbage collected: ", child_one())

