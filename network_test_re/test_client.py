import socket
import threading
import time

name_opponent = "상대"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"접속할 ip 주소를 입력하세요")

ip = input()

client_socket.connect((ip, 12000))

print("연결됨")

def receive():
    msg = client_socket.recv(1024)
    print(f"{name_opponent} : {msg.decode('utf-8')}")

def send():
    M = input()
    client_socket.send(M.encode('utf-8'))
    
thread_for_receive = threading.Thread(target=receive)
thread_for_send = threading.Thread(target=send)

thread_for_receive.start()
thread_for_send.start()

while True:
    time.sleep(1)
    pass