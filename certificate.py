import math
from random import randint

class Person:
    connetion_key: int
    common_key: int

    def __init__(self, root, mod):
        self.root = root
        self.mod = mod
        self.person_num = randint(1, 9)
        self.open_num = root**self.person_num % self.mod

    def get_connection(self, _open):
        self.connetion_key = _open
        self.common_key = self.connetion_key**self.person_num % self.mod

range = 50

root = randint(1, range)
mod = randint(1, range)

first = Person(root, mod)
second = Person(root, mod)

first.get_connection(second.open_num)
second.get_connection(first.open_num)

print(first.common_key == second.common_key)