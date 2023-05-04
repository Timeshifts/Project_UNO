import socket
import threading
import time
import queue

class Multi_Server:
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = 12000
        self.msg_queue = queue.Queue()
        self.socket_array = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host_ip, self.port))
        self.server_socket.listen(6)
    
    def receive(self, client_socket):
        while True:
            msg = client_socket.recv(1024)
            print("받음")
            self.msg_queue.put(msg.decode())
    
    def handle_client(self):
        while True:
            connect_socket, addr = self.server_socket.accept()
            
            print(f"{addr} 연결됨")
            
            self.socket_array.append(connect_socket)
            
            thread_receive = threading.Thread(target=self.receive, args=(connect_socket,))
            thread_receive.daemon = True
            thread_receive.start()
    
    def send(self):
        while True:
            if self.msg_queue.empty() == True:
                time.sleep(0.2)
            else:
                M = self.msg_queue.get().encode()
                
                for i in range(len(self.socket_array)):
                    self.socket_array[i].send(M)
    
    def server_start(self):
        thread_handle_client = threading.Thread(target=self.handle_client)
        thread_handle_client.daemon = True
        thread_handle_client.start()
                    
        thread_send = threading.Thread(target=self.send)
        thread_send.daemon = True
        thread_send.start()