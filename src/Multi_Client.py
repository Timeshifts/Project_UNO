import socket
import threading
import queue
import pickle

# -----------------------------------------------
# Client 객체, 유저는 Client 객체를 생성해서 그 객체를 통해 서버에 접속
# -----------------------------------------------
class Multi_Client:
    def __init__(self, ip):
        self.ip = ip
        self.msg_queue = queue.Queue()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread_for_receive = 0
    
    
    def send(self, M):
        self.client_socket.send(pickle.dumps(M))
    
    
    def receive(self):
        while True:
            msg = pickle.loads(self.client_socket.recv(1024))
            self.msg_queue.put(msg)
            print(f"서버가 뿌린 메세지 : {msg}")
            
            # "wrong" 받으면 와일문 탈출, 잘못된 패스워드를 입력한 경우이다.
            if msg == "wrong":
                break
            # -----------------------------------------------
            
            # "kicked" 받으면 와일문 탈출, 강퇴당한 경우이다.
            if msg == "kicked":
                self.send("deleted")
            # -----------------------------------------------
    
            
    def client_start(self):
        self.client_socket.connect((self.ip, 12000))
        self.thread_for_receive = threading.Thread(target=self.receive)
        self.thread_for_receive.start()
    
    
    # 서버로부터 소켓 연결 끊기 
    def client_end(self):
        print(f"연결 끊김")
        self.thread_for_receive.join()
        self.client_socket.close()
    # -----------------------------------------------
        
        
    




    
