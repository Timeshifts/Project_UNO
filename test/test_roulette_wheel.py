import random, unittest, card

class RouletteTest(unittest.TestCase):
    def test_roulette(self):
        deck = [card.Card("1", "blue")] * 1000 + [card.Card("again", "blue")] * 1000
        random.shuffle(deck)

        # story_a는 다른 곳에서 테스트하므로,
        # 이쪽 test에서는 delta를 높게 잡았습니다.
        self.assertAlmostEqual(len(card.roulette_wheel_selection(1000, deck, (50, 50))), 500, delta=500*0.2)

        deck = [card.Card("1", "blue")] * 1000 + [card.Card("again", "blue")] * 1000
        random.shuffle(deck)

        self.assertAlmostEqual(len(card.roulette_wheel_selection(1000, deck, (40, 60)))[0], 400, delta=400*0.2)

if __name__ == "__main__":
    unittest.main()