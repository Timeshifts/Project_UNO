import random
import unittest
import GameManager as GM
from setting_menu import Setting_UI
from card import Card


class Test(unittest.TestCase):


    def test_card_distribution(self):
        self.test_deck = []
        self.start_cards_integer = 1000

        def set_deck():
            card_color = ["blue", "wild"]
            card_name = [
                "0",
                "1",
                "again",
            ]
            for color in card_color:
                if color == "wild":
                    for i in range(1000):
                        self.test_deck.append(Card("color", color))
                else:
                    for cn in card_name:
                        for k in range(1000):
                            self.test_deck.append(Card(cn, color))

        def card_shuffle():
            random.shuffle(self.test_deck)
        
        def roulette_wheel_selection(weights):
            hand = []
            card_num = [0, 0]  # 일반, 기술카드 구분위한 리스트
            for i in range(self.start_cards_integer):
                
                if weights == 0:
                    hand.append(self.test_deck.pop())
                else:
                    r = random.randint(1, 200 + weights)
                
                    if r < 100:
                        card_num[0] += 1
                    else:
                        card_num[1] += 1

                    for card in self.test_deck:
                        if card.name.isdigit() and card_num[0] != 0:
                            index = self.test_deck.index(card)
                            hand.append(self.test_deck.pop(index))
                            card_num[0] -= 1
                        elif not card.name.isdigit() and card_num[1] != 0:
                            index = self.test_deck.index(card)
                            hand.append(self.test_deck.pop(index))
                            card_num[1] -= 1
            for n in card_num:
                if n != 0:
                    for j in range(n):
                        hand.append(self.deck.pop())
            return hand

        set_deck()
        card_shuffle()

        count = [0, 0]
        for x in self.test_deck:
            if x.name.isdigit():
                count[0] += 1
            else:
                count[1] += 1

        print("Nomal : {0}, Ability: {1}".format(count[0], count[1]))

        a_hand = []
        b_hand = []
        a_count = [0, 0]
        b_count = [0, 0]
        a_weight = 50
        b_weight = 0

        a_hand = roulette_wheel_selection(a_weight)
        b_hand = roulette_wheel_selection(b_weight)

        for x in a_hand:
            if x.name.isdigit():
                a_count[0] += 1
            else:
                a_count[1] += 1
        for x in b_hand:
            if x.name.isdigit():
                b_count[0] += 1
            else:
                b_count[1] += 1

        print("A 플레이어 선택횟수 - 일반카드:{0}, 기술카드:{1}".format(a_count[0], a_count[1]))
        print("B 플레이어 선택횟수 - 일반카드:{0}, 기술카드:{1}".format(b_count[0], b_count[1]))
        a_nor = a_count[0] / (a_count[0] + a_count[1])
        a_abil = a_count[1] / (a_count[0] + a_count[1])
        b_nor = b_count[0] / (b_count[0] + b_count[1])
        b_abil = b_count[1] / (b_count[0] + b_count[1])
        print(
            "A 플레이어 확률 :{0} 기술카드:{1}  ({2} : {3})".format(
                a_nor, a_abil, int(a_nor * 100), int(a_abil * 100)
            )
        )
        print(
            "B 플레이어 확률 :{0} 기술카드:{1}  ({2} : {3})".format(
                b_nor, b_abil, int(b_nor * 100), int(b_abil * 100)
            )
        )

        self.assertAlmostEqual(a_nor, 0.4, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(a_abil, 0.6, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_nor, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_abil, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)

    def test_card_distribution_real(self):
        gm = GM.GameManager()
        gm.game_start()
        gm.start_cards_integer = 20
        a_count = [0, 0]
        b_count = [0, 0]
        a_weight = 50
        b_weight = 0
        a_hand = gm.roulette_wheel_selection(a_weight)
        b_hand = gm.roulette_wheel_selection(b_weight)

        for x in a_hand:
            if x.name.isdigit():
                a_count[0] += 1
            else:
                a_count[1] += 1
        for x in b_hand:
            if x.name.isdigit():
                b_count[0] += 1
            else:
                b_count[1] += 1

        print("A 플레이어 선택횟수 - 일반카드:{0}, 기술카드:{1}".format(a_count[0], a_count[1]))
        print("B 플레이어 선택횟수 - 일반카드:{0}, 기술카드:{1}".format(b_count[0], b_count[1]))
        a_nor = a_count[0] / (a_count[0] + a_count[1])
        a_abil = a_count[1] / (a_count[0] + a_count[1])
        b_nor = b_count[0] / (b_count[0] + b_count[1])
        b_abil = b_count[1] / (b_count[0] + b_count[1])
        print(
            "A 플레이어 확률 :{0} 기술카드:{1}  ({2} : {3})".format(
                a_nor, a_abil, int(a_nor * 100), int(a_abil * 100)
            )
        )
        print(
            "B 플레이어 확률 :{0} 기술카드:{1}  ({2} : {3})".format(
                b_nor, b_abil, int(b_nor * 100), int(b_abil * 100)
            )
        )

        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

        self.assertAlmostEqual(a_nor, 0.4, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(a_abil, 0.6, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_nor, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_abil, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)
    
    def test_game_start(self):
        self.gm = GM.Gm
        self.gm.start_cards_integer = 30
        self.gm.computer_count = 1
        decision_cards = []
        self.gm.game_start()


        # 모든 플레이어들이 정한 수만큼 카드를 가져갔는지 확인
        for i in range(len(self.gm.players)):
            self.assertEqual(len(self.gm.players[i].hand),self.gm.start_cards_integer)    
        print("OK")
        
        # 가능한 카드의 판별이 맞는지 확인
        print(f"grave_top 의 이름 : {self.gm.grave_top.name} 색 : {self.gm.grave_top_color} ")

        self.gm.turn_start()
        self.gm.players[0].play()
        for i in range(len(self.gm.players[0].possible_cards_num)):
            print(f"가능한 카드의 이름 :{self.gm.players[0].possible_cards[i].name} 색: {self.gm.players[0].possible_cards[i].color} ")


        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        for i in range(len(self.gm.players[0].possible_cards_num)):
            if self.gm.players[0].possible_cards[i].color == "wild":
                print(f"가능한 카드의 이름 :{self.gm.players[0].possible_cards[i].name} 색: {self.gm.players[0].possible_cards[i].color} ")
                decision_cards.append(self.gm.players[0].possible_cards[i])
            else:
                if self.gm.players[0].possible_cards[i].name != self.gm.grave_top.name:
                    self.assertEqual(self.gm.grave_top_color,self.gm.players[0].possible_cards[i].color)
                    print(f"가능한 카드의 이름 :{self.gm.players[0].possible_cards[i].name} 색: {self.gm.players[0].possible_cards[i].color} ")
                    decision_cards.append(self.gm.players[0].possible_cards[i])
                else:
                    self.assertEqual(self.gm.grave_top.name,self.gm.players[0].possible_cards[i].name)
                    print(f"가능한 카드의 이름 :{self.gm.players[0].possible_cards[i].name} 색: {self.gm.players[0].possible_cards[i].color} ")
                    decision_cards.append(self.gm.players[0].possible_cards[i])
        self.assertEqual(self.gm.players[0].possible_cards,decision_cards)
        
        
        print("OK")
        


    def test_story_a(self):
        self.gm = GM.Gm
        self.gm.start_cards_integer = 10
        self.gm.story_A_computer_count = 1
        self.gm.game_start()
        cnt = [0,0]
        self.before_turn_check = 0
        self.after_turn_check = 0
        turn_check = 1
        self.is_combo = False
        for i in range(30):
            print(f"{self.gm.turn} 번 유저 턴")
            self.gm.turn_start()
            self.before_turn_check = self.gm.turn
            if isinstance(self.gm.players[self.gm.turn],GM.StoryA_User):
                self.gm.players[self.gm.turn].computer_play()
                print(f"컴퓨터 플레이어, {self.gm.turn_count}번째 턴 종료")

            else:

                self.gm.players[self.gm.turn].play()
                print(f"유저 플레이어, {self.gm.turn_count}번째 턴 종료")
            self.gm.turn_end()
            self.after_turn_check= self.gm.turn
            if isinstance(self.gm.players[self.gm.turn],GM.StoryA_User):
                for j in range(len(self.gm.players[self.gm.turn].hand)):
                    if self.gm.players[self.gm.turn].hand[j].name == "skip":
                        cnt[0] +=1
                    elif self.gm.players[self.gm.turn].hand[j].name == "again":
                        cnt[1] +=1
                print(f"컴퓨터가 가지고 있는 skip의 수: {cnt[0]}, again의 수: {cnt[1]}")
            cnt = [0,0]
            print(f"grave_top : {self.gm.grave_top.name}, : {self.gm.grave_top.color}")

            if self.before_turn_check == self.after_turn_check:
                turn_check +=1
                self.is_combo = True
            elif self.gm.turn == 0:
                if self.is_combo == True:
                    self.assertNotEqual(turn_check,1)
                    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    print(f"컴퓨터 플레이어가 사용한 콤보 턴 횟수 :{turn_check} ")
                    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                else:
                    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    print(f"컴퓨터 플레이어가 한번에 사용한 턴 횟수 :{turn_check} ")
                    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                turn_check = 1
                self.is_combo = False


    def test_story_b(self):
        self.gm = GM.Gm
        self.gm.computer_count = 3
        self.gm.start_cards_integer = int(63 / (self.gm.computer_count+1))
        self.gm.game_start()
        
        for i in range(len(self.gm.players)):
            self.assertEqual(len(self.gm.players[i].hand),self.gm.start_cards_integer)
            print(f"{i}번 플레이어가 가진 카드의 수 : {len(self.gm.players[i].hand)}")
        print("OK")

    

    def test_story_c(self):
        self.gm = GM.Gm
        self.gm.start_cards_integer = 10
        self.gm.computer_count = 2
        self.gm.top_card_change_num = 5
        self.gm.is_top_card_change = True
        self.grave_top_four = ""
        self.gm.game_start()

        for j in range(20):
            self.gm.turn_start()
            if self.gm.turn_count % self.gm.top_card_change_num == 0:
                print("----------------------------------")
                print(f"바뀌기전의 grave_top 색 : {self.grave_top_four}")
                print(f"바뀐 후의 grave_top 색 : {self.gm.grave_top_color}")
                print("----------------------------------")
                self.assertNotEqual(self.gm.grave_top_color,self.grave_top_four)
            if isinstance(self.gm.players[self.gm.turn],GM.Computer):
                self.gm.players[self.gm.turn].computer_play()
            else:
                self.gm.players[self.gm.turn].play()
            print(f"{self.gm.turn}번 플레이어, {self.gm.turn_count}번째 턴")
            self.gm.turn_end()
            if self.gm.turn_count % self.gm.top_card_change_num == (self.gm.top_card_change_num-1):
                self.grave_top_four = self.gm.grave_top_color




    def test_story_d(self):
        self.gm = GM.Gm
        self.gm.start_cards_integer = 10
        self.gm.computer_count = 3
        self.gm.is_hand_change = True
        self.gm.hand_change_num = 20
        before_hand = []
        after_hand = []
        self.gm.game_start()

        for j in range(20):
            self.gm.turn_start()
            if self.gm.turn_count % self.gm.hand_change_num == 0:
                for a in range(len(self.gm.players)):
                    after_hand.append(len(self.gm.players[a].hand))
        
                print("----------------------------------")
                print(f"바뀌기 전 모든 플레이어 카드 수 : {before_hand}")
                print(f"바뀐 후 플레이어 카드 수 : {after_hand}")
                print("----------------------------------")
                self.assertNotEqual(before_hand,after_hand)
                before_hand = []
                after_hand = []
            if isinstance(self.gm.players[self.gm.turn],GM.Computer):
                self.gm.players[self.gm.turn].computer_play()
            else:
                self.gm.players[self.gm.turn].play()
            print(f"{self.gm.turn}번 플레이어, {self.gm.turn_count}번째 턴")
            self.gm.turn_end()
            if self.gm.turn_count % self.gm.hand_change_num == (self.gm.hand_change_num-1):
                for a in range(len(self.gm.players)):
                    before_hand.append(len(self.gm.players[a].hand))





        


if __name__ == "__main__":
    test_method = ['test_card_distribution','test_card_distribution_real','test_game_start','test_story_a','test_story_b','test_story_c','test_story_d']
    a = int(input("테스트할 함수 : "))
    suite = unittest.TestLoader().loadTestsFromName(test_method[a], Test)
    unittest.TextTestRunner().run(suite)

