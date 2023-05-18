import random, unittest, card

def roulette_wheel_selection(deck, weights):
    card_num = [0, 0]  # card_num[0] 은 일반 카드 갯수, card_num[1] 은 기술 카드 갯수
    for i in range( (int)(len(deck)/2) ):
        
        if weights == 0:
            if deck.pop() == 0:
                card_num[0] += 1
            else:
                card_num[1] += 1
        else:
            r = random.randint(1, 200 + weights)
            
            if r <= 100:
                card_num[0] += 1
            else:
                card_num[1] += 1
    
    print(f"일반 카드 {card_num[0]} 개 / 기술 카드 {card_num[1]} 개\n")
    return (card_num[0], card_num[1])


class RouletteTest(unittest.TestCase):
    def test_roulette(self):
        deck = [0] * 1000 + [1] * 1000
        random.shuffle(deck)

        # story_a는 다른 곳에서 테스트하므로,
        # 이쪽 test에서는 delta를 높게 잡았습니다.
        self.assertAlmostEqual(card.roulette_wheel_selection(1000, deck, (50, 50))[0], 500, delta=500*0.2)

        deck = [0] * 1000 + [1] * 1000
        random.shuffle(deck)

        self.assertAlmostEqual(card.roulette_wheel_selection(1000, deck, (40, 60))[0], 400, delta=400*0.2)

if __name__ == "__main__":
    unittest.main()