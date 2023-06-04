# server.py
import socket
import threading
from random import randint
from certificate import Certificate
from user import User

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 8000
ADDRESS = "0.0.0.0"
broadcast_list = []
my_socket.bind((ADDRESS, PORT))

root = randint(1, 9)
mod = randint(1, 100)
certificate = Certificate(root, mod)


def accept_loop():
    while True:
        my_socket.listen()
        client, client_address = my_socket.accept()
        username = client.recv(1024).decode()

        # отправка данных для получения ключа
        message = str({'root': root, 'mod': mod, 'open_key': certificate.open_key})
        client.send(bytes(message, 'utf-8'))

        # получение открытого ключа
        certificate.get_connection(client.recv(1024).decode())

        user = User(client, username, certificate.shared_secret_key)
        broadcast_list.append(user)
        start_listenning_thread(user)
        # TODO вынести в отдельны поток регестрацию


# Осуществляем подключение клиента
def start_listenning_thread(user):
    client_thread = threading.Thread(
        target=listen_thread,
        args=(user,)  # the list of argument for the function
    )
    client_thread.start()


def listen_thread(user):
    while True:
        message = user.client.recv(1024).decode()
        if message:
            print(message)
            broadcast(message)
        else:
            print(f"client has been disconnected : {user.client}")
            return


def broadcast(message):
    for user in broadcast_list:
        try:
            user.client.send(message.encode())
        except Exception:
            broadcast_list.remove(user)
            print(f"Client removed : {user.user_name}")


def thread_sending():
    while True:
        message_to_send = input()
        if message_to_send:
            broadcast('SERVER' + " : " + message_to_send)


threading.Thread(target=thread_sending).start()
accept_loop()
