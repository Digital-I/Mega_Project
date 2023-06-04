# client.py
import socket
import threading
from certificate import Certificate
from vizhiner import encrypt, decrypt
import hashlib


# TODO добавить проверку на коллизию
nickname = input("Введите свой ник : ").strip()
while not nickname:
    nickname = input("Ник не должен быть пустым : ").strip()

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"  # "127.0.1.1"
port = 8000
my_socket.connect((host, port))
my_socket.send(nickname.encode('utf-8'))


# обмен ключами
root_mod_openkey = eval(my_socket.recv(1024).decode('utf-8'))
certificate = Certificate(root_mod_openkey['root'], root_mod_openkey['mod'])
certificate.get_connection(root_mod_openkey['open_key'])
my_socket.send(str(certificate.open_key).encode())
# на основе общего секретного ключа генерируем md5 для шифрование Вижинера
shared_secret_key = hashlib.md5(bytes(str(certificate.shared_secret_key), 'utf-8')).hexdigest()


# поток на отправку смс
def thread_sending():
    while True:
        message_to_send = input()
        if message_to_send:
            my_socket.send(encrypt(message_to_send, shared_secret_key).encode())


# поток на получение смс
def thread_receiving():
    while True:
        message = my_socket.recv(1024).decode()
        print(f"Server: {decrypt(message, shared_secret_key)}")


# создаем 2 потока на отправку и получение смс
thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
# запускаем 2 потока на отправку и получение смс
thread_send.start()
thread_receive.start()
