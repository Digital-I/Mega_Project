# server.py
import socket
import threading
from random import randint
from certificate import Certificate
from user import User
import hashlib
from vizhiner import encrypt, decrypt


my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 8000
ADDRESS = "0.0.0.0"
broadcast_list = []
my_socket.bind((ADDRESS, PORT))


# создаем корент и модуль для сертификата
root = randint(1, 9)
mod = randint(1, 100)
certificate = Certificate(root, mod)


def accept_loop():
    while True:
        # влючаем сервер
        my_socket.listen()
        client, client_address = my_socket.accept()
        username = client.recv(1024).decode()

        # отправляем данные клиенту для генерации закрытого и общего секретного ключа
        message = str({'root': root, 'mod': mod, 'open_key': certificate.open_key})
        client.send(bytes(message, 'utf-8'))

        # получение открытого ключ от клиента
        certificate.get_connection(client.recv(1024).decode())
        user = User(client, username, hashlib.md5(bytes(str(certificate.shared_secret_key), 'utf-8')).hexdigest())
        broadcast_list.append(user)
        start_listenning_thread(user)


# Осуществляем подключение клиента
def start_listenning_thread(user):
    client_thread = threading.Thread(
        target=listen_thread,
        args=(user,)  # the list of argument for the function
    )
    threading.Thread(target=thread_sending, args=(user, )).start()
    client_thread.start()


# Принимаем смс
def listen_thread(user):
    while True:
        message = user.client.recv(1024).decode()
        if message:
            print(f"Client: {decrypt(message, user.shared_secret_key)}")
        else:
            print(f"client has been disconnected : {user.client}")
            return


# отправляем смс
def thread_sending(user):
    while True:
        message_to_send = input()
        if message_to_send:
            user.client.send(bytes(encrypt(message_to_send, user.shared_secret_key), 'utf-8'))


accept_loop()
