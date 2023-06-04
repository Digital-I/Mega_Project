# client.py
import socket
import threading
import vizhiner
from certificate import Certificate


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

# TODO сделать сохраненеие в файле, а там и авторизацию можно подогнать в отдельном скрипте
shared_secret_key = certificate.shared_secret_key


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
