import socket
import threading
import time
import queue

name_opponent = "상대"

host_ip = socket.gethostbyname(socket.gethostname())

print(f"{host_ip}")

port = 12000

msg_queue = queue.Queue()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen(6)

connect_socket, addr = server_socket.accept()

print("연결됨")

def receive():
    while True:
        msg = connect_socket.recv(1024)
        msg_queue.put(msg.decode())

def send():
    while True:
        if msg_queue.empty() == True:
            time.sleep(0.2)
        else:
            connect_socket.send(msg_queue.get().encode())
        
thread_for_receive = threading.Thread(target=receive)
thread_for_send = threading.Thread(target=send)

thread_for_receive.start()
thread_for_send.start()

while True:
    time.sleep(1)
    pass
    

