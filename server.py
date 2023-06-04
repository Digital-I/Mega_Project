# server.py
import pickle, socket, threading, hashlib
from random import randint
from certificate import Certificate
from user import User
from vizhiner import encrypt, decrypt

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
PORT = 8000
ADDRESS = "0.0.0.0"
broadcast_list = []
my_socket.bind((ADDRESS, PORT))

root = randint(1, 9)
mod = 100000
certificate = Certificate(root, mod)

def accept_loop():
    while True:
        my_socket.listen()
        client, client_address = my_socket.accept()
        username = client.recv(1024).decode()

        # отправка данных для получения ключа
        message = {'root': root, 'mod': mod, 'open_num': certificate.open_num}
        message = pickle.dumps(message)
        client.send(message)

        # получение открытого ключа
        certificate.get_connection(client.recv(1024).decode())

        hash_key = hashlib.sha256(str(certificate.common_key).encode('utf-8')).digest()
        user = User(client, username, hash_key)
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
            print(f"Received message : {message}")
            broadcast(message)
        else:
            print(f"client has been disconnected : {client}")
            return


def broadcast(message):
    for user in broadcast_list:
        try:
            message = encrypt(message, user.key)
            user.client.send(message.encode())
        except Exception(e):
            broadcast_list.remove(user)
            print(f"Client removed : {user.user_name}, {e}")

def thread_sending():
    while True:
        message_to_send = input()
        if message_to_send:
            broadcast('SERVER' + " : " + message_to_send)

threading.Thread(target=thread_sending).start()
accept_loop()