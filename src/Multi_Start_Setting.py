import Multi_Server
import Multi_Client
import time
import Multi_GameManager
import pickle
import threading
import pygame
from constant import *


class Multi_Start_Setting:
    def __init__(self):
        self.host_ip = 0
        self.input_ip = 0
        self.Server = 0
        self.Client = 0
        # self.server_name = 0
        self.chk = [0, 0, 0, 0, 0]
        self.ip_name = {}

    def server(self):
        # 서버 생성후 구동시키고, 서버 생성자의 ip 출력
        # Client에게 이 ip를 알려주면 됨
        self.Server = Multi_Server.Multi_Server()
        self.Server.server_start()
        self.host_ip = self.Server.host_ip
        print(f"당신의 아이피는 {self.host_ip} 입니다")
        # 서버 만든 사람을 클라이언트로 등록시킴,
        # 따로 호스트 처리 안하고 싹다 클라이언트로 간편하게 처리하기 위함
        self.Client = Multi_Client.Multi_Client(self.host_ip)
        self.Client.client_start()

    def player_index(self, chk, ip, name):
        # 다른 클라이언트에게 전달할 동기화 메시지 생성
        print("리스트 받기")
        if ip in self.ip_name:
            del self.ip_name[ip]
        self.ip_name[ip] = name
        sync_msg = {"type": "player_index", "chk": chk, "name": self.ip_name}
        # 동기화 메시지를 모든 클라이언트에 전송
        print("서버로 리스트 전송")
        print(f"메시지 : {sync_msg}")
        a = self.Server.socket_array
        print(a)
        self.Server.multi_sendto(sync_msg)

    def password(self, pw):
        # 서버 패스워드 설정
        self.Server.is_password = True
        self.Server.password = pw
        print(self.Server.password)

    def start(self):
        # 게임 시작
        print("게임 시작")
        self.Client.send("start")
        self.Client.send([5, 1, 0])

    def drop(self):
        # 게임 강퇴
        print("강퇴")
        #     # 강퇴, Server의 Socket 배열의 인덱스를 제거하는 방식
        #     # 현재 연결된 소켓배열의 크기를 print로 host에게 보여준다.
        #     # 해당 인덱스 입력시, 해당 소켓에 "kicked" 메세지를 보내며
        #     # Server 객체의 socket 배열에서 pop 한다.
        #     elif b == 2:
        #         print("강퇴할 인덱스를 입력하세요")
        #         print(f"현재 최대 인덱스 : {len(Server.socket_array) - 1}")

    # "start"는 방장이 게임을 시작함
    # if M == "start":
    #    print("게임 시작")
    #    MGM = Multi_GameManager.Gm
    #    MGM.client = Client

    # if isinstance(M ,dict):
    #    MGM.deck = M['ref_deck']
    #    MGM.deck = M['deck']
    #    MGM.deck = M['players']
    #    MGM.deck = M['turn']

    #         c = int(input())
    #         print(f" {c}번 인덱스 소켓 강퇴됨 ")
    #         Server.single_send(c, "kicked")
    #         Server.socket_array.pop(c)

    def client(self, ip):
        # 아이피 입력하면, 해당 아이피의 서버로 접속
        self.input_ip = ip
        print(f"{self.input_ip} 서버에 접속 중")
        self.Client = Multi_Client.Multi_Client(self.input_ip)
        connect = self.Client.client_start()
        # connect: 성공하면 True, 실패하면 False
        if connect:  # 연결 성공
            # Client는 서버로부터 메세지 받기까지 while문으로 대기한다.
            while True:
                # msg = input()
                # Client.send(msg)

                # Client의 msg_queue가 비어있으면 계속 대기한다.
                if self.Client.msg_queue.empty() == True:
                    time.sleep(0.2)

                # Client의 msg_queue가 채워져있으면 else 문으로 간다. 이는 서버로부터 메세지를 받았음을 의미
                else:
                    # msg_queue로부터 메세지를 pop해온다.
                    M = self.Client.msg_queue.get()
                    return M
        else:  # 연결 실패
            return "fail"

    def password_client(self, pw):
        # 클라이언트 비밀번호 확인
        print("비밀번호 확인 중")
        self.Client.send(pw)
        # Client는 서버로부터 메세지 받기까지 while문으로 대기한다.
        while True:
            # Client의 msg_queue가 비어있으면 계속 대기한다.
            if self.Client.msg_queue.empty() == True:
                time.sleep(0.2)
            # Client의 msg_queue가 채워져있으면 else 문으로 간다. 이는 서버로부터 메세지를 받았음을 의미
            else:
                # msg_queue로부터 메세지를 pop해온다.
                M = self.Client.msg_queue.get()
                return M

    def connect(self):  # 클라이언트 연결시
        # 메시지 수신을 위한 스레드 생성
        receiver_thread = threading.Thread(target=self.receive_messages)
        receiver_thread.start()

    def receive_messages(self):
        while True:
            # Client의 msg_queue가 비어있으면 계속 대기한다.
            if self.Client.msg_queue.empty() == True:
                time.sleep(0.2)
            # Client의 msg_queue가 채워져있으면 else 문으로 간다. 이는 서버로부터 메세지를 받았음을 의미
            else:
                # msg_queue로부터 메세지를 pop해온다.
                msg = self.Client.msg_queue.get()
                self.chk = msg["chk"]
                self.ip_name = msg["name"]
                print(self.ip_name)
                pygame.event.post(pygame.event.Event(EVENT_UPDATE))  # 화면 업데이트 이벤트

    def kicked(self):  # 스스로 "돌아가기" 버튼을 통해 방을 나갈때
        print("강퇴")
        self.Client.client_end()

    # # 게임 시작
    # dic = Server.init_game()
    # Server.send()

    # -----------------------------------------------
    # 나중에, 화면에 그리기 코드와 매핑되면 아래 sleep(1) 쓰는 와일문은 삭제
    # -----------------------------------------------

    # while True:
    #     time.sleep(1)
