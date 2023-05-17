import socket
import threading
import queue
import pickle
import pygame
from constant import *


# -----------------------------------------------
# Client 객체, 유저는 Client 객체를 생성해서 그 객체를 통해 서버에 접속
# -----------------------------------------------
class Multi_Client:
    def __init__(self, ip):
        self.ip = ip
        self.name = "MY NAME"
        self.msg_queue = queue.Queue()
        self.uno_queue = queue.Queue()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread_for_receive = 0

    def send(self, M):
        self.client_socket.send(pickle.dumps(M))

    def receive(self):
        try:
            while True:
                msg = pickle.loads(self.client_socket.recv(4096))
                if isinstance(msg,dict):
                    self.msg_queue.put(msg)
                else:
                    if msg[0:3] == "uno":
                        self.uno_queue.put(msg)
                    else:
                        self.msg_queue.put(msg)

                # "wrong" 받으면 와일문 탈출, 잘못된 패스워드를 입력한 경우이다.
                # if msg == "wrong":
                #     break
                # -----------------------------------------------

                # "kicked" 받으면 와일문 탈출, 강퇴당한 경우이다.
                if msg == "kicked":
                    self.send("deleted")

                # -----------------------------------------------
        except:
            print("서버: 원격 호스트에 의해 강제로 끊김")
            pygame.event.post(pygame.event.Event(EVENT_MAIN))  # 메인메뉴로 돌아가기

    def client_start(self):
        try:  # 해당하는 ip가 없는 경우 에러 예외 처리
            self.client_socket.settimeout(3)  # 타임아웃을 5초로 설정
            self.client_socket.connect((self.ip, 12000))  # int 넣으면 에러 발생
            self.client_socket.settimeout(None) # 연결이 완료되면 timeout 없앰
            self.thread_for_receive = threading.Thread(target=self.receive)
            self.thread_for_receive.start()
            return True
        except:
            print("에러: 해당하는 방 없음")
            return False

    # 서버로부터 소켓 연결 끊기
    def client_end(self):
        print(f"연결 끊김")
        self.thread_for_receive.join()
        self.client_socket.close()

    # -----------------------------------------------
