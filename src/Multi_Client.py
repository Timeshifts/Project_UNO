import socket
import threading
import queue

class Multi_Client:
    def __init__(self, ip):
        self.ip = ip
        self.msg_queue = queue.Queue()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, 12000))
        print("연결됨")
    
    def receive(self):
        while True:
            msg = self.client_socket.recv(1024)
            self.msg_queue.put(msg)
            print(f"서버가 뿌린 메세지 : {msg.decode()}")

    def send(self, M):
        self.client_socket.send(M.encode())
    
    def client_start(self):
        thread_for_receive = threading.Thread(target=self.receive)
        thread_for_receive.start()
    




    
