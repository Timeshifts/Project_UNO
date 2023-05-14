import Multi_Server
import Multi_Client
import time
import Multi_GameManager
import pickle


class Multi_Start_Setting:
    def __init__(self):
        self.host_ip = 0
        self.input_ip = 0

    def server(self):
        # 서버 생성후 구동시키고, 서버 생성자의 ip 출력
        # Client에게 이 ip를 알려주면 됨
        self.Server = Multi_Server.Multi_Server()
        self.Server.server_start()
        self.host_ip = self.Server.host_ip
        print(f"당신의 아이피는 {self.host_ip} 입니다")
        # -----------------------------------------------

        # 서버 만든 사람을 클라이언트로 등록시킴,
        # 따로 호스트 처리 안하고 싹다 클라이언트로 간편하게 처리하기 위함
        Client = Multi_Client.Multi_Client(self.host_ip)
        Client.client_start()
        # -----------------------------------------------

    def password(self, pw):
        self.Server.is_password = True
        self.Server.password = pw
        print(self.Server.password)

        # 비밀번호 설정, 1 입력시 비밀번호 설정하고
        # 나머지 입력은 비밀번호 없는 버전
        # 'sleep(1)'은 일단 콘솔상으로 텍스트 정리하기 위해서 딜레이줌, 추후에 삭제하면 됨
        # time.sleep(0.1)
        # print("\n비밀번호 설정을 하려면 1 입력")

        # if int(input()) == 1:
        #     print("비밀번호 1~4자리 입력")
        #     Server.is_password = True
        #     Server.password = input()
        # # -----------------------------------------------

    def start(self):
        print("시작")

    def drop(self):
        print("강퇴")
        # # 1번 입력시 게임 시작
        # # 2번 입력시 강퇴, Server의 Socket 배열의 인덱스를 제거하는 방식
        # print(" 1 : 시작")
        # print(" 2 : 강퇴")

        # while True:
        #     b = int(input())

        #     # 1번 입력하면 와일문을 바로 탈출 한다.
        #     if b == 1:
        #         break

        #     # 2번 입력시 강퇴를 한다.
        #     # 현재 연결된 소켓배열의 크기를 print로 host에게 보여준다.
        #     # 해당 인덱스 입력시, 해당 소켓에 "kicked" 메세지를 보내며
        #     # Server 객체의 socket 배열에서 pop 한다.
        #     elif b == 2:
        #         print("강퇴할 인덱스를 입력하세요")
        #         print(f"현재 최대 인덱스 : {len(Server.socket_array) - 1}")

        #         c = int(input())

        #         print(f" {c}번 인덱스 소켓 강퇴됨 ")

        #         Server.single_send(c, "kicked")
        #         Server.socket_array.pop(c)

        # # 1번 입력시 여기 코드에 도달하게 되며, 서버로 "start" 를 보낸다.
        # Client.send("start")
        # # -----------------------------------------------

        # # 게임 시작 방식을 Client 방식과 통일 시킴
        # # 서버로부터 "start" 받으면 로컬에서 게임매니저 실행
        # while True:
        #     # msg = input()
        #     # Client.send(msg)
        #     if Client.msg_queue.empty() == True:
        #         time.sleep(0.2)
        #     else:
        #         M = Client.msg_queue.get()

        #         if M == "start":
        #             print("게임 시작")
        #             MGM = Multi_GameManager.GameManager()
        #             MGM.game_start()
        #             MGM.turn_start()
        #             MGM.turn_end()
        # -----------------------------------------------

    def client(self, ip):
        # 아이피 입력하면, 해당 아이피의 서버로 접속
        print(f"서버에 접속할 아이피를 입력하세요")

        self.input_ip = ip
        Client = Multi_Client.Multi_Client(self.input_ip)
        connect = Client.client_start()

        if connect:
            # Client는 서버로부터 메세지 받기까지 while문으로 대기한다.
            while True:
                # msg = input()
                # Client.send(msg)

                # Client의 msg_queue가 비어있으면 계속 대기한다.
                if Client.msg_queue.empty() == True:
                    time.sleep(0.2)

                # Client의 msg_queue가 채워져있으면 else 문으로 간다. 이는 서버로부터 메세지를 받았음을 의미
                else:
                    # msg_queue로부터 메세지를 pop해온다.
                    M = Client.msg_queue.get()

                    # "password" 메세지를 받은경우, 패스워드를 입력한다.
                    # 제대로된 패스워드를 입력하면 서버로부터 "authenticated" 를 받는다.
                    if M == "password":
                        print("\n패스워드를 입력하세요")
                        Client.send(input())

                    # "wrong" 메세지는 잘못된 패스워드를 입력한 경우
                    if M == "wrong":
                        print("잘못된 패스워드를 입력함")
                        Client.client_end()
                        break

                    # "kicked"는 서버에 제대로 접속 했지만, 강퇴 당한 경우
                    if M == "kicked":
                        print("강퇴 당함")
                        Client.client_end()
                        break

                    # "start"는 방장이 게임을 시작함
                    if M == "start":
                        print("게임 시작")
                        MGM = Multi_GameManager.GameManager()
                        MGM.game_dic = dic
                        print(MGM.game_dic["players"])
                        print(MGM.game_dic["turn"])
                        MGM.initial_sync()

                        MGM.game_start()
                        MGM.turn_start()
                        MGM.turn_end()
        # -----------------------------------------------

    # # 게임 시작
    # dic = Server.init_game()
    # Server.send()

    # -----------------------------------------------
    # 나중에, 화면에 그리기 코드와 매핑되면 아래 sleep(1) 쓰는 와일문은 삭제
    # -----------------------------------------------

    # while True:
    #     time.sleep(1)
