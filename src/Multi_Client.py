import socket
import threading
import queue
import pickle

class Multi_Client:
    def __init__(self, ip):
        self.ip = ip
        self.name = 'MY NAME'
        self.msg_queue = queue.Queue()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, 12000))
        print("연결됨")
    
    def receive(self):
        while True:
            msg = pickle.loads(self.client_socket.recv(4096))
            self.msg_queue.put(msg)
            print(f"서버가 뿌린 메세지 : {msg}")

    def send(self, M):
        self.client_socket.send(pickle.dumps(M))
    
    def client_start(self):
        thread_for_receive = threading.Thread(target=self.receive)
        thread_for_receive.start()
    




    
