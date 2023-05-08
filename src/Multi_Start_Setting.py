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
    
    print("시작하려면 아무거나 입력하세요")
    b = int(input())
    dic = Server.init_game()
    Client.send(dic)
            
elif a == 2:
    print(f"서버에 접속할 아이피를 입력하세요")
    
    input_ip = input()
    Client = Multi_Client.Multi_Client(input_ip)
    Client.client_start()
    
    while True:
        if Client.msg_queue.empty() == True:
            time.sleep(0.2)
        else:
            dic = Client.msg_queue.get()
            if dic['game_state'] == True:
                print("게임 시작")
                MGM = Multi_GameManager.GameManager()
                MGM.game_dic = dic
                print(MGM.game_dic['players'])
                print(MGM.game_dic['turn'])
                MGM.initial_sync()

                MGM.game_start()
                MGM.turn_start()

    
# # 게임 시작
# dic = Server.init_game()
# Server.send()




while True:
    time.sleep(1)