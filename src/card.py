import random


class GameManager:
    def __init__(self):
        self.deck = []
        self.grave = []
        self.grave_top = None
    
    def game_start(self):
        self.set_deck()
        self.card_shuffle()
        self.setting_card()

    def set_deck(self):         # 맨 처음에 덱에 카드넣기
        color = ["red","green","blue","yellow","white"]
        values = list(range(0,10))+["reverse","change_color","draw_two"] + ["reverse2","change_color2","draw_two2"]
        for i in color:
            if i == "white":
                for j in values[13:16]:
                    self.deck.append(AbilityCard(j,i))
            else:
                for j in values[0:10]:
                    self.deck.append(Card(j,i))
                for j in values[10:13]:
                    self.deck.append(AbilityCard(j,i))

    def card_shuffle(self):
        random.shuffle(self.deck)
    
    def setting_card(self):                 # 게임 시작시 덱에서 카드한장 꺼내기
        self.grave_top = self.deck.pop()
        self.grave.append(self.grave_top)




class Card:

    def __init__(self,card_name,color):
        self.id = id
        self.card_name = card_name
        self.color = color
        self.score = card_name

    def __str__(self):
        return "NomalCard = name : {0}, color : {1}, score : {2}".format(self.card_name,self.color,self.score)


class AbilityCard(Card):
    def __init__(self,card_name,color):
        super().__init__(card_name,color)
        if self.color == "white":
            self.score = 50
        else:
            self.score = 20
    
    def __str__(self):
        return "AbilityCard = name : {0}, color : {1}, score : {2}".format(self.card_name,self.color,self.score)

    def reverse(self):
        pass

    def change_color(self):
        pass
    
    def draw_two(self):
        pass
