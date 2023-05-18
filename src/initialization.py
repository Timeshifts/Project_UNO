import Multi_GameManager
import random

client = None
MGM = Multi_GameManager.Multi_GameManager(client)
game_dic = {}


def init_game(clients, card_count, computer_count, storyA_count):
    MGM.start_cards_integer = card_count
    MGM.set_deck()
    MGM.card_shuffle()
    for client in clients:
        MGM.players.append(Multi_GameManager.MultiUser(False, client.getpeername()))

    # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
    for i in range(computer_count):
        MGM.players.append(Multi_GameManager.MultiComputer(True))

    for i in range(storyA_count):
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

    game_dic["ref_deck"] = MGM.ref_deck
    game_dic["deck"] = MGM.deck
    game_dic["players"] = MGM.players
    game_dic["turn"] = MGM.turn
    return game_dic
