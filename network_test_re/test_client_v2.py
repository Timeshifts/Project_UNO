import socket
import threading
import time
import queue

name_opponent = "상대"

host_ip = socket.gethostbyname(socket.gethostname())

print(f"{host_ip}")

port = 12000

msg_queue = queue.Queue()
socket_array = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen(6)

def receive(client_socket):
    while True:
        msg = client_socket.recv(1024)
        print("받음")
        msg_queue.put(msg.decode())

def handle_client():
    while True:
        connect_socket, addr = server_socket.accept()
        
        print(f"{addr} 연결됨")
        
        socket_array.append(connect_socket)
        
        thread_receive = threading.Thread(target=receive, args=(connect_socket,))
        thread_receive.daemon = True
        thread_receive.start()

def send():
    while True:
        if msg_queue.empty() == True:
            time.sleep(0.2)
        else:
            M = msg_queue.get().encode()
            
            for i in range(len(socket_array)):
                socket_array[i].send(M)

thread_handle_client = threading.Thread(target=handle_client)
thread_handle_client.daemon = True
thread_handle_client.start()
            
thread_send = threading.Thread(target=send)
thread_send.daemon = True
thread_send.start()

while True:
    time.sleep(1)
    pass