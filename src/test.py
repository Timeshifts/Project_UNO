import random
import unittest
import GameManager
from setting import Settings
from card import roulette_wheel_selection, Card


class Test(unittest.TestCase):
    # 게임시작 전에 색맹 on/off시 파일 바뀌는지 확인
    def test_colorblind(self):
        gm = GameManager.GameManager()
        gm.game_start()
        settings = Settings()
        settings.is_blind(True, gm.ref_deck)
        gm.game_start()
        self.assertEqual(
            gm.ref_deck[0].filename,
            "card_colorblind/"
            + gm.ref_deck[0].color
            + "_"
            + gm.ref_deck[0].name
            + ".png",
        )

    def test_colorblind_off(self):
        gm = GameManager.GameManager()
        gm.game_start()
        settings = Settings()
        settings.is_blind(False, gm.ref_deck)
        gm.game_start()
        self.assertEqual(
            gm.ref_deck[0].filename,
            "card/" + gm.ref_deck[0].color + "_" + gm.ref_deck[0].name + ".png",
        )

    # 게임시작 후에 색맹 on/off시 파일 바뀌는지 확인
    def test_colorblind_ingame(self):
        gm = GameManager.GameManager()
        gm.game_start()
        settings = Settings()
        settings.is_blind(False, gm.ref_deck)
        gm.game_start()
        hand1 = []
        hand2 = []
        hand1.append(gm.deck.pop())
        hand1.append(gm.deck.pop())
        hand2.append(gm.deck.pop())
        hand2.append(gm.deck.pop())

        settings.is_blind(True, gm.ref_deck)  # 색맹 on
        for card in hand1:
            self.assertEqual(
                card.filename,
                "card_colorblind/" + card.color + "_" + card.name + ".png",
            )

        settings.is_blind(False, gm.ref_deck)  # 색맹 off

        for card in hand2:
            self.assertEqual(
                card.filename, "card/" + card.color + "_" + card.name + ".png"
            )

    # # 낼 수 있는 카드들 선택
    # def test_possible_card(self):
    #     gm = GameManager.GameManager()
    #     gm.game_start()

    #     hand1 = []
    #     for i in range(30):
    #         hand1.append(gm.deck.pop())

    #     print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    #     print("grave_name:{0} grave_color: {1} ".format(gm.grave_top.name,gm.grave_top.color))
    #     gm.possible_card(gm.grave_top,hand1)

    #     print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    #     for cd in gm.possible_cards:
    #         print(cd)

    def test_card_distribution(self):
        self.test_deck = []

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

        set_deck()
        card_shuffle()

        count = [0, 0]
        for x in self.test_deck:
            if x.name.isdigit():
                count[0] += 1
            else:
                count[1] += 1

        print("Nomal : {0}, Ability: {1}".format(count[0], count[1]))

        a_cards = []
        b_cards = []
        a_count = [0, 0]
        b_count = [0, 0]
        a_weight = [0.5, 0.5]
        b_weight = [0.4, 0.6]

        a_cards = roulette_wheel_selection(1000, self.test_deck, a_weight)
        b_cards = roulette_wheel_selection(1000, self.test_deck, b_weight)

        for x in a_cards:
            if x.name.isdigit():
                a_count[0] += 1
            else:
                a_count[1] += 1
        for x in b_cards:
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

        self.assertAlmostEqual(a_nor, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(a_abil, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_nor, 0.4, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_abil, 0.6, msg="오차범위를 벗어났습니다.", delta=0.05)

    def test_card_distribution_real(self):
        gm = GameManager.GameManager()
        gm.game_start()
        a_cards = []
        b_cards = []
        a_count = [0, 0]
        b_count = [0, 0]
        a_weight = [0.5, 0.5]
        b_weight = [0.4, 0.6]

        a_cards = roulette_wheel_selection(20, gm.deck, a_weight)
        b_cards = roulette_wheel_selection(20, gm.deck, b_weight)

        print("A에 있는 카드")
        for x in a_cards:
            print(x.name, end=", ")
            if x.name.isdigit():
                a_count[0] += 1
            else:
                a_count[1] += 1
        print()
        print("B에 있는 카드")
        for x in b_cards:
            print(x.name, end=", ")
            if x.name.isdigit():
                b_count[0] += 1
            else:
                b_count[1] += 1

        print()
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

        self.assertAlmostEqual(a_nor, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(a_abil, 0.5, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_nor, 0.4, msg="오차범위를 벗어났습니다.", delta=0.05)
        self.assertAlmostEqual(b_abil, 0.6, msg="오차범위를 벗어났습니다.", delta=0.05)


if __name__ == "__main__":
    unittest.main()
