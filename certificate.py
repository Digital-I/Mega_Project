from random import randint


class Certificate:
    shared_secret_key: int

    def __init__(self, root, mod):
        self.root = int(root)
        self.mod = int(mod)
        self.private_key = randint(1, 9)
        self.open_key = root**self.private_key % self.mod

    def get_connection(self, _open):
        self.shared_secret_key = int(_open)**self.private_key % self.mod
