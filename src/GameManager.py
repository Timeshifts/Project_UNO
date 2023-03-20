class GameManager:
    def __init__(self):
        self.turn = 1 # 지금 누구 턴인지 나타내는 정수 변수
        self.turn_count_down # 유저의 해당 턴 몇초남았는지 나타낼 정수 변수
        self.game_count_down # 해당 게임 몇초 남았는지 나태닐 정수 변수
        self.attack_int # 누가 공격카드 쓰면, 그 값을 받는데 쓸 정수 변수
        self.is_attack # 턴 시작시, 공격 카드를 썼는지 판별할 불린 변수
        self.players = [] # 플레이어 객체들을 담을 배열
        self.player_count # 실제 플레이어 수가 몇 인지 나타낼 정수 변수
        self.computer_count # 컴퓨터의 수가 몇인지 나타낼 정수 변수
        self.start_cards_integer # 카드 몇장가지고 시작할건지 나타낼 정수 변수
        self.is_turn_used # 해당 턴에 행동을 했는지 판별할 불린 변수
        self.deck = [] # 덱
        self.grave = [] # 묘지, Top 부분은 플레이어들에게 색과 숫자가 보인다.
        self.grave_top # 묘지의 탑을 참조하는 Card 타입 변수
    
    
    # 게임 맨처음 시작시 각종 설정 초기화 해주는 함수    
    def game_start(self):
        # 1~4인덱스 참조 할꺼라서 0번 인덱스 아무거나 집어넣음
        self.players.append[0]
        
        # 추후에 다중 플레이어 게임을 고려한 코드인데, 추후 수정 가능성 있음
        # 게임 시작전에, 다중 플레이어들의 수를 받고, 미리 플레이어 객체를 생성한걸
        # 받아와서 여기다가 붙혀넣는 것
        for i in range(len(self.player_count)):
            self.players.append[pre_enrolled_players[i]]
        
        # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
        for i in range(len(self.computer_count)):
            self.players.append[Computer(true)]
        
        # 덱 초기화    
        self.set_deck()
        # 덱 셔플
        self.card_shuffle()
        
        # 플레이어들에게 카드 나눠줌
        for i in range(self.start_cards_integer):
            for j in range(len(self.players)):
                self.give_card(j+1)
        
        # 덱에서 카드 한장 빼서 세팅해놓음
        self.set_card()

    # 턴 시작 함수
    def turn_start(self):
        # 전 턴에 누가 공격 카드 썼는지 판별
        # 누가 공격 카드를 썼다면, attack_int 만큼 카드주고 6초 기다린후 턴종료
        if self.is_attack == True:
            
            for i in range(self.attack_int):
                self.give_card()
            
            pygame.time.wait(6000)
            self.turn_end()
        # 안 썼다면, 해당 플레이어가 컴퓨터인지 유저인지 판별한다.
        else:
            if players[turn].is_computer == True:
                players[turn].computer_play
            else:
                self.give_authority(turn)
                self.count_down()
    
    # 턴 끝 함수
    def turn_end(self):
        is_zero = False
        
        # 현재 핸드가 0개인 플레이어가 있는지 판별
        for i in range(len(self.players)):
            if len(self.players[i].hand) == 0:
                is_zero = True
        
        # 핸드가 0인 플레이어가 있으면 게임이 끝남
        if  is_zero == True:
            self.game_end()
        # 아니면 턴 1 증가시키고 다음 턴 스타트
        else:
            self.turn += 1
            
            # 턴값이 5를 넘어가면 와일문 돌려서 4씩 빼준다.
            while turn > 4:
                turn -= 4
                
            pygame.time.wait(5000)
            self.turn_start()
    
    def give_card(self):
        players[turn].hand.append(self.deck.pop())
