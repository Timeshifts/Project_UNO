import Multi_GameManager
import random

client = None

game_dic = {}
GM = Multi_GameManager.GameManager(client, game_dic)


def init_game(clients, card_count, computer_count, storyA_count):
    GM.start_cards_integer = card_count
    GM.set_deck()
    GM.card_shuffle()
    for client in clients:
        GM.players.append(Multi_GameManager.MultiUser(False, client.getpeername()))

    # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
    for i in range(computer_count):
        GM.players.append(Multi_GameManager.MultiComputer(True))

    for i in range(storyA_count):
        GM.players.append(Multi_GameManager.StoryA_User(True))

    # 총 플레이어의 수
    GM.player_num = len(GM.players)

    # 턴 선택
    GM.turn = random.randint(0, GM.player_num - 1)

    # 플레이어들에게 카드 나눠줌
    for i in range(len(GM.players)):
        GM.players[i].hand = GM.roulette_wheel_selection(
            GM.players[i].skill_card_weight
        )
        
    game_dic['ref_deck'] = GM.ref_deck
    game_dic['deck'] = GM.deck
    game_dic['players'] = GM.players
    game_dic['turn'] = GM.turn
    game_dic['computer_count'] = computer_count
    game_dic['story_A_computer_count'] = storyA_count
    return game_dic
