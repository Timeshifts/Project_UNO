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
        MGM = Multi_GameManager.GameManager(client)
        game_dic = {}

        self.game_start()

    def game_start(self, clients):
        MGM.set_deck()
        MGM.card_shuffle()
        for client in clients:
            MGM.players.append(Multi_GameManager.MultiUser(False,client.getpeername()))

        # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
        for i in range(MGM.computer_count):
            MGM.players.append(Multi_GameManager.MultiComputer(True))

        for i in range(MGM.story_A_computer_count):
            MGM.players.append(Multi_GameManager.StoryA_User(True))

        # 총 플레이어의 수
        MGM.player_num = len(MGM.players)

        # 턴 선택
        MGM.turn = random.randint(0, MGM.player_num - 1)

        # 플레이어들에게 카드 나눠줌
        for i in range(len(MGM.players)):
            MGM.players[i].hand = MGM.roulette_wheel_selection(
                MGM.players[i].skill_card_weight
            )

        game_dic['shuffle_deck'] = MGM.deck
        game_dic['players'] = MGM.players
        game_dic['turn'] = 1
        return game_dic