from typing import Any


def print_object_id(object: Any):
    print(id(object))


a = 12
print(id(a))
print_object_id(a)