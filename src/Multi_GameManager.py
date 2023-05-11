import random
import pygame
import threading
import time
import Multi_Server
import Multi_Client
from constant import EVENT_END_GAME, EVENT_TURN_END

class GameManager:
    # 모든 업적이 승리와 관련되어 있으므로,
    # 이번에 달성할 수 있는 업적인지를 한번에 나타낼 수 있습니다.
    # 단, 단순 승리 업적은 원래 위치에서 처리하도록 하겠습니다.
    achi_flag = [5, 6, 9]

    def __init__(self, client):
        self.turn = 0  # 지금 누구 턴인지 나타내는 정수 변수
        self.turn_count = 0  # 총 몇번의 턴이 진행되었는지
        self.players = []  # 플레이어 객체들을 담을 배열
        self.real_player_count = 0  # 실제 플레이어 수가 몇 인지 나타낼 정수 변수
        self.player_num = 0  # 전체 플레이어 수
        self.computer_count = 0  # 컴퓨터의 수가 몇인지 나타낼 정수 변수
        self.start_cards_integer = 0  # 카드 몇장가지고 시작할건지 나타낼 정수 변수
        self.deck = []  # 덱
        self.ref_deck = []  # 참조덱
        self.grave = []  # 묘지, Top 부분은 플레이어들에게 색과 숫자가 보인다.
        self.grave_top = 0  # 묘지의 탑을 참조하는 Card 타입 변수
        self.is_someone_win = 0  # 누가 핸드 갯수가 0이 되서 우승한 건지 판별하는 불린변수
        self.winner_index = 0  # 누가 우승자인지 값을 담는 정수변수
        self.turn_jump_num = 0  # 누가 턴 건너뛰기를 했으면 여기에 값이 설정되는 정수 변수
        self.is_turn_reversed = False  # 누가 턴 진행방향을 바꿨는지 체크
        self.grave_top_color = ""  # 묘지의 top 카드 색깔
        self.game_timer_end = False  # 게임 타이머 다 되면 True 되는 불린변수
        self.turn_timer_end = False  # 턴 타이머 다 되거나, 유저 행동하면 True 되는 불린변수
        self.game_timer_integer = 0  # 게임 타이머 체크할 정수변수
        self.turn_timer_integer = 0  # 턴 타이머 체크할 정수변수
        self.is_setting = False  # 맨 처음 덱세팅 후에 카드 한장 빼서 놓을 때 쓰는 불린변수
        self.is_top_card_change = False  # 스토리모드 지역 C 특성 쓸껀지 불린변수
        self.top_card_change_num = 100  # 스토리모드 지역 C 특성, 몇 턴마다 바뀔껀지
        self.is_hand_change = False  # 스토리모드 지역 D 특성 쓸껀지 불린변수
        self.hand_change_num = 100  # 스토리모드 지역 D 특성, 몇턴마다 바뀔껀지
        self.story_A_computer_count = 0  # story A 특성 유저를 얼마나? 넣을지
        self.end = 0  # 게임 종료 여부
        self.game_timer_thread = 0
        self.turn_timer_thread = 0
        self.turn_end_thread = None
        self.timer_zero = False
        self.wild = False
        self.no_act = False
        self.paused = False  # 일시 정지 중 타이머 정지를 위한 불린변수
        self.player_score = []  # 점수 저장
        self.story = -1  # 몇 번 스토리 모드? (-1이면 일반 게임)
        self.wild_card = 0
        self.set_uno = False
        self.achi_flag = [5, 6, 9]
        self.client = client

    # 특정 업적 달성을 위한 제약 조건 달성 시 True,
    # 특정 업적 달성을 위한 제약 조건을 위반했을 때 False
    # 예: 기술 카드 사용 -> 기술 카드 사용 금지 업적에 False
    @staticmethod
    def toggle_achi(num, state):
        if state:
            if num-1 not in GameManager.achi_flag:
                GameManager.achi_flag.append(num-1)
        else:
            if num-1 in GameManager.achi_flag:
                GameManager.achi_flag.remove(num-1)

    # 게임 맨처음 시작시 각종 설정 초기화 해주는 함수
    def game_start(self):

        self.game_timer_end = False
        self.game_count_down()
        
        # self.game_dic['game_state'] = True
        self.game_dic['shuffle_deck'] = self.MGM.deck
        self.game_dic['players'] = self.MGM.players
        # self.game_dic['players_num'] = self.MGM.player_num
        self.game_dic['computer_count'] = self.MGM.computer_count
        self.game_dic['story_A_computer_count'] = self.MGM.story_A_computer_count
        self.game_dic['turn'] = self.MGM.turn
        
        
        a = 0
        while True:
            if self.client.msg_queue.empty() == False:
                a += 1
                
                if a == 1:
                    self.ref_deck = self.client.msg_queue.get()
                    self.deck = self.ref_deck
                
                if a == 2:
                    self.players = self.client.msg_queue.get()
                
                if a == 3:
                    self.computer_count = self.client.msg_queue.get()
                
                if a == 4:
                    self.story_A_computer_count = self.client.msg_queue.get()
                
                if a == 5:
                    self.turn = self.client.msg_queue.get()
                    break
                

        if self.story == 0:
            print("스토리 A 특성 적용")
            # self.story_A_computer_count = 1
            # self.computer_count = 0
        elif self.story == 1:
            print("스토리 B 특성 적용")
            self.start_cards_integer = 15
        elif self.story == 2:
            print("스토리 C 특성 적용")
            self.is_top_card_change = True
            self.top_card_change_num = 5
        elif self.story == 3:
            print("스토리 D 특성 적용")
            self.is_hand_change = True
            self.hand_change_num = 20

        self.player_num = len(self.players)

        # 플레이어 수
        print(f"총 플레이어 : {self.player_num}")
        print(f"일반 컴퓨터 : {self.computer_count}")
        print(f"A 컴퓨터 : {self.story_A_computer_count}")

        # 덱에서 카드 한장 빼서 세팅해놓음
        self.setting_card(self.deck)

    def game_end(self):
        self.game_timer_end = True
        scored = False

        if self.is_someone_win == True:
            self.winner_index = self.turn
        else:
            scored = True
            self.winner_index = self.player_score_calculate()

        print(f"{self.winner_index} 번 유저 승리!!")
        self.end = 1

        # (직접 조작하는) 플레이어가 승리하였는가?
        player_win = self.winner_index == 0

        if player_win and scored:
            # 점수 판단으로 승리 - 11번 업적(전략가) 달성 가능
            self.toggle_achi(11, True)

        pygame.event.post(
            pygame.event.Event(
                EVENT_END_GAME,
                {
                    "player_win": player_win,
                    "story_map": self.story + 1,
                },
            )
        )

        # 전체 타이머 종료 추가

    # 턴 시작 함수
    def turn_start(self):
        self.turn_count += 1
        # 10턴 초과: 6번 업적(압도) 달성 불가능
        if self.turn_count > 10: self.toggle_achi(6, False)

        if self.is_top_card_change == True:
            self.top_card_change()

        if self.is_hand_change == True:
            self.hand_change()

        self.turn_timer_end = False  # 턴 타이머 동작 가능
        self.turn_count_down()  # 턴 타이머 동작 시작

        # 전 턴에 누가 공격 카드 썼는지 판별
        # 누가 공격 카드를 썼다면, attack_int 만큼 카드주고 6초 기다린후 턴종료
        # print(f"턴 시작, 현재 {self.turn} 번 유저에게 로직 실행\n")
        # print(f"현재 묘지의 탑 카드 색깔 = {self.grave_top_color}, 이름 = {self.grave_top.name}\n")

        if self.players[self.turn].is_attacked == True:
            print("공격 카드 효과 발동")

            if self.players[self.turn].defence_int > 0:
                print("방어발동")
                self.players[self.turn].defence_int = 0
            else:
                for i in range(self.players[self.turn].attacked_int):
                    self.give_card(self.turn)

        # 안 썼다면, 해당 플레이어가 컴퓨터인지 유저인지 판별한다.
        else:
            self.give_authority(self.turn)

            # if self.players[self.turn].is_computer == True:
            #     print(f"{self.turn} 번 유저, 컴퓨터 플레이 작동\n")
            #     self.players[self.turn].computer_play()
            # else:
            #     print(f"{self.turn} 턴 유저, 실제 플레이어 이므로 권한 지급\n")
            #     self.players[self.turn].play()

        #  pygame.time.wait(2000)

        # self.turn_end()

    # 턴 끝 함수
    def turn_end(self, option=0):
        if self.no_act:
            return
        self.no_act = True
        print("턴 종료")

        self.players[self.turn].is_attacked = False
        self.players[self.turn].attacked_int = 0
        self.turn_timer_end = True

        print(f"{option} {self.turn_end_thread}")
        if self.turn_end_thread is None:
            self.turn_end_thread = threading.Thread(
                target=self.computer_wait, args=(option,)
            )
            self.turn_end_thread.start()

    def computer_wait(self, option=0):
        time.sleep(0.25)
        pygame.event.post(pygame.event.Event(EVENT_TURN_END, {"option": option}))

    def turn_end_act(self):
        # print("비동기 동작")
        self.turn_end_thread = None
        self.turn_timer_integer = 15

        # 현재 핸드가 0인지 판별
        if len(self.players[self.turn].hand) == 0:
            print(f"{self.turn} 턴 유저 승리")
            self.is_someone_win = True
            self.game_end()

        elif self.game_timer_integer == 0:
            print(f"시간 다 됐으므로 게임 종료")
            self.game_end()

        else:
            if (
                len(self.players[self.turn].hand) == 1
                and self.players[self.turn].is_uno == False
            ):
                print(f"{self.turn} 턴 유저는 핸드 갯수가 1개인데 우노를 안누름, 패널티 적용")
                self.give_card(self.turn)

            self.players[self.turn].is_authority = False
            self.players[self.turn].is_turn_used = True

            if self.is_turn_reversed == False:
                self.turn += 1 + self.turn_jump_num

                while self.turn >= self.player_num:
                    self.turn -= self.player_num
            else:
                self.turn -= 1 + self.turn_jump_num

                while self.turn < 0:
                    self.turn += self.player_num

            self.turn_jump_num = 0

            # pygame.time.wait(3000)

            # self.turn_start()

    def give_card(self, a):
        if len(self.deck) == 0:
            self.set_deck_from_grave()
        self.players[a].is_uno = False
        self.set_uno = False
        self.players[a].hand.append(self.deck.pop())

    def get_card(self, card):
        self.grave.append(card)
        self.grave_top = self.grave[-1]
        self.grave_top_color = self.grave_top.color

        if card.name.isdigit() == False:
            # 기술 카드 사용: 7번 업적(수학자) 달성 불가능
            if self.turn == 0: self.toggle_achi(7, False)
                
            if card.name == "color":
                # 와일드 카드 사용: 10번 업적(순수) 달성 불가능
                if self.turn == 0: self.toggle_achi(10, False)
                self.wild_color()
                if self.turn == 0:
                    self.turn_jump(-1)

            elif card.name == "four":
                # 와일드 카드 사용: 10번 업적(순수) 달성 불가능
                if self.turn == 0: self.toggle_achi(10, False)
                print("다음 턴 유저에게, 카드 4장 공격")
                self.wild_four()
                if self.turn == 0:
                    self.turn_jump(-1)

            # elif card.name == "target":
            #     self.wild_target()

            elif card.name == "again":
                print("추가 턴 획득 작동함")
                self.turn_jump(-1)

            elif card.name == "defence":
                print("방어 카드 효과 발동, 방어도 2 증가")
                self.defence()

            elif card.name == "pick":
                print("다음 턴 유저에게, 카드 2장 공격")
                target = 0
                if self.is_turn_reversed == False:
                    target = self.turn + 1
                    if target >= self.player_num:
                        target -= self.player_num
                else:
                    target = self.turn - 1
                    if target < 0:
                        target += self.player_num

                self.attack(2, target)

            elif card.name == "reverse":
                print("턴 진행 방향 변경 작동함")
                self.turn_reverse()

            elif card.name == "skip":
                print("턴 건너뛰기 작동함")
                self.turn_jump(1)

    def player_score_calculate(self):
        min = 100000
        winner = 0
        for i in range(self.player_num):
            temp = 0
            for j in range(len(self.players[i].hand)):
                temp += self.players[i].hand[j].score
            self.player_score.append(temp)
            # print(f"{i} 번 유저의 점수는 {temp} 점")

            if temp < min:
                min = temp
                winner = i

        return winner

    def give_authority(self, turn):
        self.players[turn].is_authority = True
        self.players[turn].is_turn_used = False

    """
    예전 방식의 턴 리버스, 일단 주석처리
    def turn_reverse(self):
        self.players.reverse()
        self.turn = (self.player_num - 1) - self.turn
        """

    # 카드 셔플
    # def card_shuffle(self, deck):
    # random.shuffle(deck)

    # 게임 시작시 덱에서 카드한장 꺼내기
    def setting_card(self, deck):
        self.is_setting = True
        pop_card = deck.pop()
        self.get_card(pop_card)
        self.is_setting = False

    # 맨 처음에 덱에 카드넣기
    def set_deck(self):
        card_color = ["blue", "green", "red", "yellow", "wild"]
        card_name = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "again",
            "defence",
            "pick",
            "reverse",
            "skip",
        ]
        # wcard_name = ["color", "four", "target"]
        wcard_name = ["color", "four"]
        for color in card_color:
            if color == "wild":
                for wcn in wcard_name:
                    self.ref_deck.append(Card(0, color, wcn, 0))
            else:
                for cn in card_name:
                    self.ref_deck.append(Card(0, color, cn, 0))

    # 덱 사이즈 0되면 묘지에 있는거 top 빼고 deck에 넣어서 랜덤 돌리기
    def set_deck_from_grave(self):
        for i in range(len(self.grave) - 1):
            self.deck.append(self.grave.pop(0))

        random.shuffle(self.deck)

    # 카드 셔플
    def card_shuffle(self):
        self.deck = self.ref_deck.copy()
        random.shuffle(self.deck)

    # 게임 시작시 덱에서 카드한장 꺼내기
    def set_card(self):
        pop_card = self.deck.pop()
        self.grave.append(pop_card)
        self.grave_top = self.grave[-1]  # grave 의 맨 위의 카드
        self.grave_top_color = self.grave_top.color

    # 타이머
    def game_timer(self, count):
        start_time = time.time()
        while True:
            # 일시 정지 중에 타이머 동작 방지
            if self.paused:
                time_elapsed = time.time() - start_time
                while self.paused:
                    time.sleep(0.1)
                start_time = time.time() - time_elapsed
            self.game_timer_integer = count - (int)(time.time() - start_time)
            if self.game_timer_integer <= 0:
                self.turn_timer_integer = 0
                # print("game time end")
                break
            elif self.game_timer_end == True:
                break

            # print(f"game time: {self.game_timer_integer} seconds")
            time.sleep(1)

    def turn_timer(self, count):
        self.timer_zero = False
        start_time = time.time()
        while True:
            # 일시 정지 중에 타이머 동작 방지
            if self.paused:
                time_elapsed = time.time() - start_time
                while self.paused:
                    time.sleep(0.1)
                start_time = time.time() - time_elapsed
            self.turn_timer_integer = count - (int)(time.time() - start_time)
            if self.turn_timer_integer <= 0:
                # print("turn time end")
                self.timer_zero = True
                break
            elif self.turn_timer_end == True:
                break

            # print(f"turn time: {self.turn_timer_integer} seconds")
            time.sleep(0.2)

    def game_count_down(self):  # 전체 시간
        self.game_timer_thread = threading.Thread(target=self.game_timer, args=(100,))
        self.game_timer_thread.start()

    def turn_count_down(self):  # 턴 시간
        self.turn_timer_thread = threading.Thread(target=self.turn_timer, args=(15,))
        self.turn_timer_thread.start()

    def top_card_change(self):
        if self.turn_count % self.top_card_change_num == 0:
            random_color = ["blue", "green", "red", "yellow"]
            self.grave_top_color = random.choice(random_color)

    def hand_change(self):
        if self.turn_count % self.hand_change_num == 0:
            hands = []
            for i in range(self.player_num):
                hands.append(self.players[i].hand)

            random.shuffle(hands)

            for j in range(self.player_num):
                self.players[j].hand = hands.pop()

    def roulette_wheel_selection(self, weights):
        hand = []
        card_num = [0, 0]  # 일반, 기술카드 구분위한 리스트
        for i in range(self.start_cards_integer):
            if weights == 0:
                hand.append(self.deck.pop())
            else:
                r = random.randint(1, 200 + weights)

                if r <= 100:
                    card_num[0] += 1
                else:
                    card_num[1] += 1

                for card in self.deck:
                    if card.name.isdigit() and card_num[0] != 0:
                        index = self.deck.index(card)
                        hand.append(self.deck.pop(index))
                        card_num[0] -= 1
                    elif not card.name.isdigit() and card_num[1] != 0:
                        index = self.deck.index(card)
                        hand.append(self.deck.pop(index))
                        card_num[1] -= 1

        for n in card_num:
            if n != 0:
                for j in range(n):
                    hand.append(self.deck.pop())
        return hand

    # 기술 카드 효과
    def turn_reverse(self):
        if self.is_turn_reversed == False:
            self.is_turn_reversed = True
        else:
            self.is_turn_reversed = False

    def turn_jump(self, jump):
        self.turn_jump_num = jump

    def attack(self, num, target):
        self.players[target].attacked_int += num
        self.players[target].is_attacked = True

    def card_color_selection(self):
        card_color = ["blue", "green", "red", "yellow"]

        if self.players[self.turn].is_computer == True:
            self.grave_top_color = random.choice(card_color)
        else:
            self.wild = True

    def wild_four(self):
        self.card_color_selection()
        self.wild_card = "wild_four"
        if self.players[self.turn].is_computer == True:
            target = 0
            if self.is_turn_reversed == False:
                target = (self.turn + 1) % self.player_num
            else:
                target = (self.turn - 1) % self.player_num
            self.attack(4, target)

    def wild_color(self):
        self.card_color_selection()

    # def wild_target(self):
    #     target = random.randint(0, self.player_num - 1)
    #     if self.is_setting == False:
    #         if self.players[self.turn].is_computer == True:
    #             target = random.randint(0, self.player_num - 1)
    #             while target == self.turn:
    #                 target = random.randint(0, self.player_num - 1)
    #         else:
    #             self.wild = True
    #             print(f"플레이어를 선택하세요")
    #             for i in range(self.player_num):
    #                 print(f"/ {i}번 플레이어")
    #             while True:
    #                 a = int(input())
    #                 if a < 0 or a >= self.player_num:
    #                     print("다시 입력하세요")
    #                 else:
    #                     target = a
    #                     break
    #     self.attack(2, target)
    #     print(f"{target}번 유저에게, 카드 2장 공격")
    #     self.card_color_selection()

    def defence(self):
        self.players[self.turn].defence_int += 1


# -------------------------------------------------------------------------------------------------


class Player:
    def __init__(self, is_computer):
        self.is_computer = is_computer
        self.hand = []
        self.possible_cards = []
        self.is_authority = False
        self.is_turn_used = False
        self.is_uno = False
        self.is_attacked = False
        self.attacked_int = 0
        self.defence_int = 0
        self.possible_cards_num = []
        self.skill_card_weight = 0

    def press_uno(self):
        if self.is_authority == True and len(self.hand) == 2:
            if Gm.set_uno == False:
                self.is_uno = True
                print("우노 성공")
        if self.is_authority == False and len(self.hand) == 2:  # 남의 턴에 우노 버튼 클릭
            Gm.set_uno = True
            print("우노 방해")

    def use_card(self, index):
        self.client.send(index)
        
        while True:
            if self.client.msg_queue.empty() == False:
                break
        self.current_card = self.hand[index]
        self.hand.remove(self.current_card)
        self.is_turn_used = True
        Gm.get_card(self.current_card)

    def get_card(self):
        Gm.give_card(Gm.turn)
        self.is_turn_used = True
        print(f"{Gm.turn} 턴 유저는 카드를 받아옴")

    def judge_possible_cards(self):
        for i in range(len(self.hand)):
            if (
                self.hand[i].color == "wild"
                or Gm.grave_top_color == "wild"
                or Gm.grave_top_color == self.hand[i].color
                or Gm.grave_top.name == self.hand[i].name
            ):
                self.possible_cards.append(self.hand[i])
                self.possible_cards_num.append(i)


# -------------------------------------------------------------------------------------------------


class User(Player):
    def __init__(self, is_computer):
        super().__init__(is_computer)

    def play(self):
        self.possible_cards.clear()
        self.possible_cards_num.clear()
        self.judge_possible_cards()

        return self.possible_cards_num


# -------------------------------------------------------------------------------------------------


class Computer(Player):
    def __init__(self, is_computer):
        super().__init__(is_computer)

    def computer_play(self):
        self.possible_cards.clear()
        self.possible_cards_num.clear()
        self.judge_possible_cards()

        if Gm.set_uno == False and len(self.hand) == 2:
            # 컴퓨터의 우노 사용 - 8번 업적(사냥꾼) 획득 가능
            GameManager.toggle_achi(8, True)
            self.press_uno()

        if len(self.possible_cards_num) != 0:
            ran = random.choice(self.possible_cards_num)
            self.use_card(ran)
            return_value = f"{self.current_card.color}_{self.current_card.name}"
            self.current_card = 0
        else:
            self.get_card()
            return_value = "get"

        return return_value


# -------------------------------------------------------------------------------------------------


class StoryA_User(Player):
    def __init__(self, is_computer):
        super().__init__(is_computer)
        self.skill_card_weight = 50

    def computer_play(self):
        self.possible_cards.clear()
        self.possible_cards_num.clear()
        self.judge_possible_cards()
        is_combo = False

        if Gm.set_uno == False and len(self.hand) == 2:
            self.press_uno()
        
        for i in range(len(self.possible_cards_num)):
            print(f"{self.possible_cards_num[i]} : {self.possible_cards[i].color}_{self.possible_cards[i].name}")

        if len(self.possible_cards_num) != 0:
            for i in range(len(self.possible_cards_num)):
                if (
                    self.possible_cards[i].name == "again"
                    or self.possible_cards[i].name == "skip"
                ):
                    print("--------콤보 공격--------")
                    self.use_card(self.possible_cards_num[i])
                    return_value = f"{self.current_card.color}_{self.current_card.name}"
                    self.current_card = 0
                    is_combo = True
                    break
            if is_combo == False:
                ran = random.choice(self.possible_cards_num)
                self.use_card(ran)
                return_value = f"{self.current_card.color}_{self.current_card.name}"
                self.current_card = 0
        else:
            self.get_card()
            return_value = "get"

        return return_value

# -------------------------------------------------------------------------------------------------


class Card:
    def __init__(self, id, color, name, filename):
        self.id = id
        self.color = color
        self.name = name
        # self.card_data = pygame.image.load(filename)
        # self.rect = self.card_data.get_rect()               # card_data 의 위치정보를 가져온다
        if self.color == "wild":
            self.score = 50
        elif self.name.isdigit():
            self.score = int(name)
        else:
            self.score = 20


Gm = GameManager()
