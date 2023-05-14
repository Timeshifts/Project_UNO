import Multi_GameManager
import random

class Multi:
    def __init__(
        self, pos=(0, 0), size=(150, 50), computer_count=0, story_A_computer_count=0, player_count=1, name="ME",
    ):
        self.computer_count = computer_count
        self.story_A_computer_count = story_A_computer_count
        self.player_count = player_count
        self.name = name

        client = None
        self.MGM = Multi_GameManager.GameManager(client)
        self.game_dic = {}

        self.game_start()

    def game_start(self, clients):
        self.MGM.set_deck()
        self.MGM.card_shuffle()
        for client in clients:
            self.MGM.players.append(Multi_GameManager.MultiUser(False,client.getpeername()))

        # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
        for i in range(self.MGM.computer_count):
            self.MGM.players.append(Multi_GameManager.MultiComputer(True))

        for i in range(self.MGM.story_A_computer_count):
            self.MGM.players.append(Multi_GameManager.StoryA_User(True))

        # 총 플레이어의 수
        self.MGM.player_num = len(self.MGM.players)

        # 턴 선택
        self.MGM.turn = random.randint(0, self.MGM.player_num - 1)

        # 플레이어들에게 카드 나눠줌
        for i in range(len(self.MGM.players)):
            self.MGM.players[i].hand = self.MGM.roulette_wheel_selection(
                self.MGM.players[i].skill_card_weight
            )

        self.game_dic['shuffle_deck'] = self.MGM.deck
        self.game_dic['players'] = self.MGM.players
        self.game_dic['turn'] = 1
        return self.game_dic