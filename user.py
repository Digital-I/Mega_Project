import socket


class User:
    client: socket
    user_name: str
    key: int

    def __init__(self, client, user_name, shared_secret_key):
        self.client = client
        self.user_name = user_name
        self.shared_secret_key = shared_secret_key
