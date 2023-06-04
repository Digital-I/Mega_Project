# client.py
import socket
import threading
import vizhiner
from certificate import Certificate
import pickle

# TODO добавить проверку на коллизию
nickname = input("Choose your nickname : ").strip()
while not nickname:
    nickname = input("Your nickname should not be empty : ").strip()

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"  # "127.0.1.1"
port = 8000
my_socket.connect((host, port))

my_socket.send(nickname.encode())

# обмен ключами
rmo = pickle.loads(my_socket.recv(1024))
certificate = Certificate(rmo['root'], rmo['mod'])
certificate.get_connection(rmo['open_num'])
my_socket.send(str(certificate.open_num).encode())

# TODO сделать сохраненеие в файле, а там и авторизацию можно подогнать в отдельном скрипте
common_key = certificate.common_key

# отправляем сообщение
def thread_sending():
    while True:
        message_to_send = input()
        if message_to_send:
            message_with_nickname = nickname + " : " + message_to_send
            my_socket.send(message_with_nickname.encode())


# принемаем сообщение
def thread_receiving():
    while True:
        message = my_socket.recv(1024).decode()
        print(message)


thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
thread_send.start()
thread_receive.start()