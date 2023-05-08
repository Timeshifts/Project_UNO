import Multi_Server
import Multi_Client
import time
import Multi_GameManager
import pickle

print("\n숫자를 입력하세요")
print("1 : 서버생성")
print("2 : 아이피 입력")

a = int(input())

if a == 1:
    Server = Multi_Server.Multi_Server()
    
    print(f"당신의 아이피는 {Server.host_ip} 입니다")
    
    Server.server_start()
    Client = Multi_Client.Multi_Client(Server.host_ip)
    Client.client_start()
    
    print("시작하려면 1을 입력하세요")
    msg = int(input())
    print("게임 시작")
            
    
elif a == 2:
    print(f"서버에 접속할 아이피를 입력하세요")
    
    input_ip = input()
    Client = Multi_Client.Multi_Client(input_ip)
    Client.client_start()


    
# 게임 시작
Server.MGM.init_game()
Server.init_bool = False
Server.send( )
while True:
    msg = input()
    Client.send(msg)
    if Client.msg_queue.empty() == True:
        time.sleep(0.2)
    else:
        M = Client.msg_queue.get()
        
        if M == "start":
            print("게임 시작")
            MGM = Multi_GameManager.GameManager()
            MGM.game_start()
            MGM.turn_start()



while True:
    time.sleep(1)