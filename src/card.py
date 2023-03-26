import random
import pygame



# 맨 처음에 덱에 카드넣기
def set_deck(self,deck):       
    card_color = ["blue","green","red","yellow","wild"]
    card_name = ["0","1","2","3","4","5","6","7","8","9","again","defence","pick","reverse","skip","back"]
    wcard_name = ["color","four","target"]
    id_cnt = 0
    for color in card_color:
        if color == "wild":
            for wcn in wcard_name:
                id_cnt += 1
                filename = "파일명/"+color +"_"+ wcn+".png"
                deck.append(Card(id_cnt,wcn,color,filename))
        else:
            for cn in card_name:
                id_cnt += 1
                filename = "파일명/"+color +"_"+ cn+".png"
                deck.append(Card(id_cnt,cn,color,filename))
        
                    
# 카드 셔플
def card_shuffle(self,deck):
    random.shuffle(deck)

# 게임 시작시 덱에서 카드한장 꺼내기
def setting_card(self,deck):
    pop_card = deck.pop()                 
    self.grave.append(pop_card)
    grave_top = self.grave[-1]      # grave 의 맨 위의 카드


class Card:
    def __init__(self,id,card_name,color,filename):
        self.id = id
        self.card_name = card_name
        self.color = color
        self.card_data = pygame.image.load(filename)
        self.rect = self.card_data.get_rect()               # card_data 의 위치정보를 가져온다
        if color == "wild":
            self.score = 50
        elif card_name.isdigit():
            self.score = int(card_name)
        else:
            self.score = 20



# 판별
def decision(grave_top,current_card):
    if current_card.color == "wild":
        if current_card.name == "four":
            four()
    elif current_card.color == grave_top.color:
        if current_card.name.isdigit() == False:
            if current_card.name == "pick":
                pick()
        else:
            print("컬러같음 : 일반")
            pass
    elif current_card.name == grave_top.name:
        print("숫자같음 : 일반")
        pass
    else:
        return print("no")        # 숫자랑 색 둘다 안맞을 때는 그냥 return

    # 카드 내기
    self.grave.append(self.players[self.turn].current_card)
    self.grave_top = self.grave[len(self.grave) - 1]
