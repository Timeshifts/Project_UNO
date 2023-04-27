import socket
import threading
import time

name_opponent = "상대"

host_ip = socket.gethostbyname(socket.gethostname())

print(f"{host_ip}")

port = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen(6)

connect_socket, addr = server_socket.accept()

print("연결됨")

def receive():
    msg = connect_socket.recv(1024)
    print(f"{name_opponent} : {msg.decode('utf-8')}")

def send():
    M = input()
    connect_socket.send(M.encode('utf-8'))

thread_for_receive = threading.Thread(target=receive)
thread_for_send = threading.Thread(target=send)

thread_for_receive.start()
thread_for_send.start()

while True:
    time.sleep(1)
    pass
    

