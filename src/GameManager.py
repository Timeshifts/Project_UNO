import random
import pygame


class GameManager:
    def __init__(self):
        self.turn = 0  # 지금 누구 턴인지 나타내는 정수 변수
        self.turn_count_down = 0  # 유저의 해당 턴 몇초남았는지 나타낼 정수 변수
        self.game_count_down = 0  # 해당 게임 몇초 남았는지 나태닐 정수 변수
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
        self.grave_top_color = ""

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

        # 일단 임시로 주석처리리
        # random.shuffle(self.players)
        
        self.turn = random.randint(0, self.player_num - 1)

        # 덱 초기화
        self.set_deck()

        # 덱 셔플
        self.card_shuffle()

        # 플레이어들에게 카드 나눠줌
        for i in range(self.start_cards_integer):
            for j in range(len(self.players)):
                self.give_card(j)

        # 덱에서 카드 한장 빼서 세팅해놓음
        self.setting_card(self.deck)
        
        pygame.time.wait(2000)
        
        self.turn_start()

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
            f"현재 묘지의 탑 카드 색깔 = {self.grave_top_color}, 이름 = {self.grave_top.name}\n"
        )

        if self.players[self.turn].is_attacked == True:
            print("공격 카드 효과 발동\n")
            print(f"{self.turn} 번 유저에게 카드 {self.players[self.turn].attacked_int} 장 부여\n")
            for i in range(self.players[self.turn].attacked_int):
                self.give_card(self.turn)

            self.players[self.turn].is_attacked = False
            self.attacked_int = 0

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

            # 턴값이 플레이어 수를 넘어가면 와일문 돌려서 빼준다.

            pygame.time.wait(3000)

            self.turn_start()

    def give_card(self, a):
        # a는 해당 번호의 플레이어
        self.players[a].hand.append(self.deck.pop())

    def get_card(self, card):
        self.grave.append(card)
        self.grave_top = self.grave[-1]
        self.grave_top_color = self.grave_top.color

        if card.name.isdigit() == False:
            
            if card.name == "color":
                self.wild_color()
            
            elif card.name == "four":
                print("다음 턴 유저에게, 카드 4장 공격\n")
                if self.is_turn_reversed == False:
                    target = self.turn + 1
                    if target >= self.player_num:
                        target -= self.player_num
                else:
                    target = self.turn - 1
                    if target < 0:
                        target += self.player_num
                
                self.attack(4, target)
            
            elif card.name == "target":
                self.target_attack()
   
            elif card.name == "again":
                print("추가 턴 획득 작동함\n")
                self.turn_jump(-1)
                
            elif card.name == "defense":
                pass
                
            elif card.name == "pick":
                print("다음 턴 유저에게, 카드 2장 공격\n")
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
                print("턴 진행 방향 변경 작동함\n")
                self.turn_reverse()
                
            elif card.name == "skip":
                print("턴 건너뛰기 작동함\n")
                self.turn_jump(1)    
                


    def player_score_calculate(self):
        min = 100000
        winner = 0
        for i in range(self.player_num):
            temp = 0
            for j in range(len(self.players[j].hand)):
                temp += self.players[i].hand[j].score
            
            if temp < min:
                min = temp
                winner = i
        
        return winner
            

    def give_authority(self, turn):
        self.players[turn].is_authority = True
        self.players[turn].is_turn_used = False

    

    '''
    예전 방식의 턴 리버스, 일단 주석처리
    def turn_reverse(self):
        self.players.reverse()
        self.turn = (self.player_num - 1) - self.turn
        '''

    def current_game_count_down(self):
        while self.game_count_down > 0 and self.is_someone_win == False:
            self.game_count_down -= 1

    def current_turn_count_down(self):
        while (
            self.turn_count_down > 0 and self.players[self.turn].is_turn_used == False
        ):
            self.turn_count_down -= 1

    # 카드 셔플
    #def card_shuffle(self, deck):
        #random.shuffle(deck)

    # 게임 시작시 덱에서 카드한장 꺼내기
    def setting_card(self, deck):
        pop_card = deck.pop()
        self.grave.append(pop_card)
        self.grave_top = self.grave[-1]  # grave 의 맨 위의 카드
        self.grave_top_color = self.grave_top.color

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
                    self.ref_deck.append(Card(0, color, wcn, 0))
            else:
                for cn in card_name:
                    self.ref_deck.append(Card(0, color, cn, 0))

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
    
    
    # 여기 아래 부터는 기술 카드 효과들임
    
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
    
    def wild_color(self):
        card_color = ["blue", "green", "red", "yellow"]
        
        if self.players[self.turn].is_computer == True:
            ran = random.randint(0,3)
            self.grave_top_color = card_color[ran]
        else:
            print(f"색을 선택하세요")
            for i in range(len(card_color)):
                print(
                    f"/{card_color[i]} {i}번"
                )
            
            while True:
                a = int(input())

                if a < 0 or a >= len(card_color):
                    print("다시 입력하세요\n")
                else:
                    self.grave_top_color = card_color[a]
                    break
        
        print(f"묘지 탑 색깔 {self.grave_top_color} 로 설정")
    
    def target_attack(self):
        target = 0
        if self.players[self.turn].is_computer == True:
            target = random.randint(0, self.player_num - 1)
        else:
            print(f"플레이어를 선택하세요")
            for i in range(self.player_num):
                print(
                    f"/ {i}번 플레이어"
                )
            while True:
                a = int(input())

                if a < 0 or a >= self.player_num:
                    print("다시 입력하세요\n")
                else:
                    target = a
                    break
                
        self.attack(2, target)
        print(f"{target}번 유저에게, 카드 2장 공격\n")
        

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

    def press_uno(self):
        if self.is_authority == True and len(self.hand) == 1:
            self.is_uno = True

    def use_card(self, index):
        current_card = self.possible_cards[index]
        self.hand.remove(current_card)
        self.is_turn_used = True
        Gm.get_card(current_card)
        print(f"{Gm.turn} 턴 유저가 낸 카드는 {current_card.color} {current_card.name} \n")

    def get_card(self):
        Gm.give_card(Gm.turn)
        self.is_turn_used = True
        print(f"{Gm.turn} 턴 유저는 카드를 받아옴 \n")
        
    def judge_possible_cards(self):
        for i in range(len(self.hand)):
            if (
                self.hand[i].color == "wild"
                or Gm.grave_top_color == "wild"
                or Gm.grave_top_color == self.hand[i].color
                or Gm.grave_top.name == self.hand[i].name
            ):
                self.possible_cards.append(self.hand[i])

# -------------------------------------------------------------------------------------------------

class User(Player):
    def __init__(self, is_computer):
        super().__init__(is_computer)

    def play(self):
        self.possible_cards.clear()
        self.judge_possible_cards()

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
                    print(f"/{self.hand[i].color} {self.hand[i].name}")

            elif a == 2:
                if len(self.possible_cards) != 0:
                    for i in range(len(self.possible_cards)):
                        print(
                            f"/{self.possible_cards[i].color} {self.possible_cards[i].name}"
                        )
                else:
                    print(f"낼 수 있는 카드가 없습니다.")

            elif a == 3:
                if len(self.possible_cards) != 0:
                    print(f"다음 카드들 중에서 어떤 카드를 낼지 선택하세요")
                    for i in range(len(self.possible_cards)):
                        print(
                            f"/{self.possible_cards[i].color} {self.possible_cards[i].name} {i}번"
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
                print(f"받은 카드는 {self.hand[-1].color} {self.hand[-1].name}\n")
                break


# -------------------------------------------------------------------------------------------------


class Computer(Player):
    def __init__(self, is_computer):
        super().__init__(is_computer)

    def computer_play(self):
        self.possible_cards.clear()
        self.judge_possible_cards()

        if len(self.possible_cards) != 0:
            ran = random.randrange(len(self.possible_cards))
            self.use_card(ran)
        else:
            self.get_card()

        if len(self.hand) == 1:
            self.press_uno()


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

Gm.computer_count = 3
Gm.start_cards_integer = 5

Gm.game_start()
