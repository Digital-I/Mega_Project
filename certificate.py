import math
from random import randint

class Certificate:
    common_key: int

    def __init__(self, root, mod):
        self.root = int(root)
        self.mod = int(mod)
        self.person_num = randint(1, 9)
        self.open_num = root**self.person_num % self.mod

    def get_connection(self, _open):
        self.common_key = int(_open)**self.person_num % self.mod
