# Why we shouldn't use mutable containers as default arguments.

def list_names(names=[]):
    """Function to print a list of names."""
    print("About to print some names:")
    print(*names, sep=" ", end="\n")

names = ["Chirag", "Angelica"]

list_names(names)
# Default argument is not affected.
list_names()

def list_names(names=[]):
    """Function to print names but also add a stranger to the list."""
    print("About to print some names:")
    names.append("Spooky Stranger")
    print(*names, sep=" ", end="\n")


list_names(names)
# Spooky Stranger lingers after the fact!
list_names()
