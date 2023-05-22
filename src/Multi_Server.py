import socket
import threading
import time
import queue
import pickle
import initialization
import pygame
from constant import *


class Multi_Server:
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = 12000
        self.msg_queue = queue.Queue()
        self.socket_array = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # 방금 사용하고 close한 port를 즉시 다시 사용할 수 있다.
        self.server_socket.bind((self.host_ip, self.port))
        self.server_socket.listen(6)
        self.is_password = False
        self.password = ""
        self.random_request = False
        self.addr = 0
        self.ip = 0
        self.name = 0


    def single_send(self, index, msg):
        try:
            self.socket_array[index].send(pickle.dumps(msg))
        except:
            print("현재 연결은 원격 호스트에 의해 강제로 끊겼습니다")

    def multi_send(self):
        while True:
            if self.msg_queue.empty() == True:
                time.sleep(0.2)
            else:
                M = self.msg_queue.get()

                for i in range(len(self.socket_array)):
                    if isinstance(M, dict):
                        M["index"] = i
                    self.socket_array[i].send(pickle.dumps(M))

    def multi_sendto(self, msg):
        for i in range(len(self.socket_array)):
            self.single_send(i, msg)
        print("각 클라이언트에게 전송")

    def receive(self, client_socket):
        try:
            while True:
                msg = pickle.loads(client_socket.recv(4096))
                if isinstance(msg, dict):
                    self.msg_queue.put(msg)
                elif isinstance(msg, list):
                    initialization.init_game(self.socket_array, msg[0], msg[1], msg[2])
                    dic = initialization.game_dic
                    self.msg_queue.put(dic)
                    break
                else:
                    if msg == "deleted":
                        break
                    elif msg[0:6] == "random":
                        if self.random_request == False:
                            self.random_request = True
                            num = int(msg[15:])
                    elif msg == "start":
                        self.msg_queue.put(msg)      
                    elif msg[1] == "out":
                        self.disconnect_client(msg[0])
                        self.multi_sendto(msg[2])
                    elif type(msg) == tuple:  # 새로운 이름인 경우
                        self.ip = msg[0]
                        self.name = msg[1]
                        pygame.event.post(pygame.event.Event(EVENT_UPDATE_CHK_SERVER))
                    else:
                        self.msg_queue.put(msg)
        except:
            print("서버: 원격 호스트에 의해 강제로 끊김!")

    def handle_client(self):
        while True:
            try:
                connect_socket, addr = self.server_socket.accept()
                self.addr = addr
                if self.is_password == True:
                    connect_socket.send(pickle.dumps("password"))
                    thread = threading.Thread(
                        target=self.password_receive,
                        args=(
                            connect_socket,
                            addr,
                        ),
                    )
                    thread.daemon = True
                    thread.start()
                else:
                    self.authenticated_client(connect_socket, addr)
            except ConnectionAbortedError as e:     # 서버가 방 나갈 시에 예외처리
                print(str(e))
                break
            except OSError as e:     # 서버가 방 나갈 시에 예외처리
                print(str(e))
                break

    def password_receive(self, connect_socket, addr):
        while True:
            try:
                msg = pickle.loads(connect_socket.recv(1024))

                if msg == self.password:
                    self.authenticated_client(connect_socket, addr)
                else:
                    connect_socket.send(pickle.dumps("wrong"))
            except:
                print("원격 호스트에 의해 강제로 끊김")

    def authenticated_client(self, connect_socket, addr):
        print(f"{addr} 연결됨")
        connect_socket.send(pickle.dumps("authenticated"))

        self.socket_array.append(connect_socket)

        thread_receive = threading.Thread(target=self.receive, args=(connect_socket,))
        thread_receive.daemon = True
        thread_receive.start()
        pygame.event.post(pygame.event.Event(EVENT_UPDATE_CHK))

    def server_start(self):
        thread_handle_client = threading.Thread(target=self.handle_client)
        thread_handle_client.daemon = True
        thread_handle_client.start()

        thread_send = threading.Thread(target=self.multi_send)
        thread_send.daemon = True
        thread_send.start()

    def disconnect_client(self, ip):
        for i, client_socket in enumerate(self.socket_array):
            client_addr = client_socket.getpeername()
            if client_addr[0] == ip:
                client_socket.close()
                self.socket_array.pop(i)
                print(f"클라이언트 {client_addr}의 연결이 끊어졌습니다.")
                break

    def disconnect_server(self):
        for i in range(len(self.socket_array)):
            self.socket_array[i].close()
        self.server_socket.close()
