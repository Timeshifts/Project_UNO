import random
import pygame


class GameManager:
    def __init__(self):
        self.turn = 0  # 지금 누구 턴인지 나타내는 정수 변수
        self.turn_count_down = 0  # 유저의 해당 턴 몇초남았는지 나타낼 정수 변수
        self.game_count_down = 0  # 해당 게임 몇초 남았는지 나태닐 정수 변수
        self.attack_int = 0  # 누가 공격카드 쓰면, 그 값을 받는데 쓸 정수 변수
        self.is_attack = 0  # 턴 시작시, 공격 카드를 썼는지 판별할 불린 변수
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
        self.turn_jump_num = 0  # 누가 턴 건너뛰기를 했으면 여기에 값이 설정되는 정수 변수
        self.is_turn_reversed = False  # 누가 턴 진행방향을 바꿨는지 체크

    # 게임 맨처음 시작시 각종 설정 초기화 해주는 함수
    def game_start(self):
        # 추후에 다중 플레이어 게임을 고려한 코드인데, 추후 수정 가능성 있음
        # 게임 시작전에, 다중 플레이어들의 수를 받고, 미리 플레이어 객체를 생성한걸
        # 받아와서 여기다가 붙혀넣는 것
        # for i in range(len(self.real_player_count)):
        # self.players.append[pre_enrolled_players[i]]

        self.players.append(User(False))

        # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
        for i in range(self.computer_count):
            self.players.append(Computer(True))

        self.player_num = len(self.players)

        random.shuffle(self.players)

        # 덱 초기화
        self.set_deck(self.deck)

        # 덱 셔플
        self.card_shuffle(self.deck)

        # 플레이어들에게 카드 나눠줌
        for i in range(self.start_cards_integer):
            for j in range(len(self.players)):
                self.give_card(j)

        # 덱에서 카드 한장 빼서 세팅해놓음
        self.setting_card(self.deck)

    def game_end(self):
        if self.is_someone_win == True:
            pass
        else:
            min = 100000
            minIndex = 0

            for i in range(self.player_num):
                temp = self.player_score_calculate(i)

                if temp < min:
                    min = temp
                    minIndex = i

    # 턴 시작 함수
    def turn_start(self):
        # 전 턴에 누가 공격 카드 썼는지 판별
        # 누가 공격 카드를 썼다면, attack_int 만큼 카드주고 6초 기다린후 턴종료
        print(f"턴 시작, 현재 {self.turn} 번 유저에게 로직 실행\n")
        print(
            f"현재 묘지의 탑 카드 색깔 = {self.grave_top.color}, 숫자 = {self.grave_top.card_name}\n"
        )

        if self.is_attack == True:
            print("공격 카드 효과 발동\n")
            print(f"{self.turn} 번 유저에게 카드 {self.attack_int} 장 부여\n")
            for i in range(self.attack_int):
                self.give_card(self.turn)

            self.is_attack == False
            self.attack_int = 0

        # 안 썼다면, 해당 플레이어가 컴퓨터인지 유저인지 판별한다.
        else:
            # self.count_down()
            self.give_authority(self.turn)

            if self.players[self.turn].is_computer == True:
                print(f"{self.turn} 번 유저, 컴퓨터 플레이 작동\n")
                self.players[self.turn].computer_play()
            else:
                print(f"{self.turn} 턴 유저, 실제 플레이어 이므로 권한 지급\n")
                self.players[self.turn].play()

        pygame.time.wait(3000)

        self.turn_end()

    # 턴 끝 함수
    def turn_end(self):
        print(f"턴 종료\n\n")
        # 현재 핸드가 0인지 판별
        if self.players[self.turn].hand == 0:
            print(f"{self.turn} 턴 유저 승리\n")
            self.is_someone_win = True
            self.game_end()
        # 아니면 턴 1 증가시키고 다음 턴 스타트
        else:
            if (
                len(self.players[self.turn].hand) == 1
                and self.players[self.turn].is_uno == False
            ):
                print(f"{self.turn} 턴 유저는 핸드 갯수가 1개인데 우노를 안누름, 패널티 적용\n")
                print(f"{self.turn} 턴 유저에게 카드 1장 지급\n")
                self.give_card(self.turn)

            self.turn += 1 + self.turn_jump_num

            self.turn_jump_num = 0

            # 턴값이 플레이어 수를 넘어가면 와일문 돌려서 빼준다.
            while self.turn >= self.player_num:
                self.turn -= self.player_num

            self.players[self.turn].is_authority = False
            self.players[self.turn].is_turn_used = True

            pygame.time.wait(3000)

            self.turn_start()

    def give_card(self, a):
        # a는 해당 번호의 플레이어
        self.players[a].hand.append(self.deck.pop())

    def get_card(self, card):
        self.grave.append(card)
        self.grave_top = self.grave[-1]

        # 이후 기술 카드면 기술카드 함수 실행
        pass

    def player_score_calculate(self, a):
        pass

    def give_authority(self, turn):
        self.players[turn].is_authority = True
        self.players[turn].is_turn_used = False

    def turn_jump(self, jump):
        self.turn_jump_num = jump

    def turn_reverse(self):
        self.players.reverse()
        self.turn = (self.player_num - 1) - self.turn

    def attack(self, a):
        self.attack_int = a
        self.is_attack = True

    def current_game_count_down(self):
        while self.game_count_down > 0 and self.is_someone_win == False:
            self.game_count_down -= 1

    def current_turn_count_down(self):
        while (
            self.turn_count_down > 0 and self.players[self.turn].is_turn_used == False
        ):
            self.turn_count_down -= 1

    # 카드 셔플
    def card_shuffle(self, deck):
        random.shuffle(deck)

    # 게임 시작시 덱에서 카드한장 꺼내기
    def setting_card(self, deck):
        pop_card = deck.pop()
        self.grave.append(pop_card)
        self.grave_top = self.grave[-1]  # grave 의 맨 위의 카드

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
        wcard_name = ["color", "four", "target"]
        for color in card_color:
            if color == "wild":
                for wcn in wcard_name:
                    self.ref_deck.append(Card(wcn, color))
            else:
                for cn in card_name:
                    self.ref_deck.append(Card(cn, color))

    # 카드 셔플
    def card_shuffle(self):
        self.deck = self.ref_deck.copy()
        random.shuffle(self.deck)

    # 게임 시작시 덱에서 카드한장 꺼내기
    def set_card(self):
        pop_card = self.deck.pop()
        self.grave.append(pop_card)
        self.grave_top = self.grave[-1]  # grave 의 맨 위의 카드

    # 낼 수 있는 카드들 판별
    def possible_card(self, grave_top, hand):
        for card in hand:
            if (
                card.color == "wild"
                or card.color == grave_top.color
                or card.name == grave_top.name
            ):
                self.possible_cards.append(card)

    # 카드를 냈을 때 어떤 카드인지 판별
    def choose_card(self, current_card):
        if current_card.color == "wild":
            if current_card.name == "four":
                pass
        elif current_card.name.isdigit() == False:
            if current_card.name == "pick":
                pass
        # 카드 내기
        self.grave.append(self.players[self.turn].current_card)
        self.grave_top = self.grave[-1]


# -------------------------------------------------------------------------------------------------


class Player:
    def __init__(self, is_computer):
        self.is_computer = is_computer
        self.hand = []
        self.possible_cards = []
        self.is_authority = False
        self.is_turn_used = False
        self.is_uno = False

    def press_uno(self):
        if self.is_authority == True and len(self.hand) == 1:
            self.is_uno = True

    def use_card(self, index):
        current_card = self.possible_cards[index]
        self.hand.remove(current_card)
        self.is_turn_used = True
        Gm.get_card(current_card)
        print(f"{Gm.turn} 턴 유저가 낸 카드는 {current_card.color} {current_card.card_name} \n")

    def get_card(self):
        Gm.give_card(Gm.turn)
        self.is_turn_used = True
        print(f"{Gm.turn} 턴 유저는 카드를 받아옴 \n")


class User(Player):
    def __init__(self, is_computer):
        super().__init__(is_computer)

    def play(self):
        self.possible_cards.clear()

        for i in range(len(self.hand)):
            if (
                Gm.grave_top.color == self.hand[i].color
                or Gm.grave_top.card_name == self.hand[i].card_name
            ):
                self.possible_cards.append(self.hand[i])

        print("1 : 보유한 카드들 보기\n")
        print("2 : 낼 수 있는 카드들 보기\n")
        print("3 : 카드 내기\n")
        print("4 : 카드 한장 받아오기\n")

        while True:
            a = int(input())

            if a < 0 or a > 4:
                print("다시 입력하세요\n")

            elif a == 1:
                for i in range(len(self.hand)):
                    print(f"/{self.hand[i].color} {self.hand[i].card_name}")

            elif a == 2:
                if len(self.possible_cards) != 0:
                    for i in range(len(self.possible_cards)):
                        print(
                            f"/{self.possible_cards[i].color} {self.possible_cards[i].card_name}"
                        )
                else:
                    print(f"낼 수 있는 카드가 없습니다.")

            elif a == 3:
                if len(self.possible_cards) != 0:
                    print(f"다음 카드들 중에서 어떤 카드를 낼지 선택하세요")
                    for i in range(len(self.possible_cards)):
                        print(
                            f"/{self.possible_cards[i].color} {self.possible_cards[i].card_name} {i}번"
                        )

                    while True:
                        a = int(input())

                        if a < 0 or a >= len(self.possible_cards):
                            print("다시 입력하세요\n")
                        else:
                            print(f"{a}번 카드 선택")
                            self.use_card(a)
                            break

                    break
                else:
                    print(f"낼 수 있는 카드가 없습니다.")

            else:
                self.get_card()
                print(f"받은 카드는 {self.hand[-1].color} {self.hand[-1].card_name}\n")
                break


# -------------------------------------------------------------------------------------------------


class hand(Player):
    def __init__(self, is_computer):
        super().__init__(is_computer)

    def computer_play(self):
        self.possible_cards.clear()

        for i in range(len(self.hand)):
            if (
                Gm.grave_top.color == self.hand[i].color
                or Gm.grave_top.card_name == self.hand[i].card_name
            ):
                self.possible_cards.append(self.hand[i])

        if len(self.possible_cards) != 0:
            ran = random.randrange(len(self.possible_cards))
            self.use_card(ran)
        else:
            self.get_card()

        if len(self.hand) == 1:
            self.press_uno()


# -------------------------------------------------------------------------------------------------


class Card:
    def __init__(self, id, card_name, color, filename):
        self.id = id
        self.card_name = card_name
        self.color = color
        # self.card_data = pygame.image.load(filename)
        # self.rect = self.card_data.get_rect()               # card_data 의 위치정보를 가져온다
        if self.color == "wild":
            self.score = 50
        elif self.card_name.isdigit():
            self.score = int(card_name)
        else:
            self.score = 20


Gm = GameManager()

Gm.computer_count = 3
Gm.start_cards_integer = 5

Gm.game_start()
Gm.turn_start()
