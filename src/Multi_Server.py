import socket
import threading
import time
import queue
import pickle
import Multi_GameManager
import random

class Multi_Server:
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = 12000
        self.msg_queue = queue.Queue()
        self.socket_array = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       # 방금 사용하고 close한 port를 즉시 다시 사용할 수 있다.
        self.server_socket.bind((self.host_ip, self.port))
        self.server_socket.listen(6)
        self.MGM = Multi_GameManager.GameManager()
        self.init_bool = True      # 게임 시작시 초기화를 위한 변수
        self.game_dic = {}
    
    def receive(self, client_socket):
        while True:
            msg = pickle.loads(client_socket.recv(1024))
            print("받음")
            self.msg_queue.put(msg)
    
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
            if self.init_bool == False:
                for i in range(len(self.socket_array)):
                    self.socket_array[i].send(pickle.dumps(self.MGM.game_dic))
                self.init_bool = True
            else:
                M = self.msg_queue.get()
                for i in range(len(self.socket_array)):
                    self.socket_array[i].send(pickle.dumps(M))


    
    def server_start(self):
        thread_handle_client = threading.Thread(target=self.handle_client)
        thread_handle_client.daemon = True
        thread_handle_client.start()
                    
        thread_send = threading.Thread(target=self.send)
        thread_send.daemon = True
        thread_send.start()


    def init_game(self):
        self.MGM.card_shuffle()
        for i in range(len(self.socket_array)):
            self.MGM.players.append(self.MGM.User(False))

        # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
        for i in range(self.MGM.computer_count):
            self.MGM.players.append(self.MGM.Computer(True))

        for i in range(self.MGM.story_A_computer_count):
            self.MGM.players.append(self.MGM.StoryA_User(True))

        # 총 플레이어의 수
        self.MGM.player_num = len(self.MGM.players)

        # 턴 선택
        self.MGM.turn = random.randint(0, self.MGM.player_num - 1)

        # 플레이어들에게 카드 나눠줌
        for i in range(len(self.MGM.players)):
            self.MGM.players[i].hand = self.MGM.roulette_wheel_selection(
                self.MGM.players[i].skill_card_weight
            )

        self.game_dic['shuffle_deck'] = self.MGM.deck
        self.game_dic['players'] = self.MGM.players
        self.game_dic['players_num'] = self.MGM.player_num
        self.game_dic['computer_count'] = self.MGM.computer_count
        self.game_dic['turn'] = self.MGM.turn
