import random

def roulette_wheel_selection(weights):
    card_num = [0, 0]  # card_num[0] 은 일반 카드 갯수, card_num[1] 은 기술 카드 갯수
    for i in range( (int)(len(deck)/2) ):
        
        if weights == 0:
            if deck.pop() == 0:
                card_num[0] += 1
            else:
                card_num[1] += 1
        else:
            r = random.randint(1, 200 + weights)
            
            if r < 100:
                card_num[0] += 1
            else:
                card_num[1] += 1
    
    print(f"일반 카드 {card_num[0]} 개 / 기술 카드 {card_num[1]} 개\n")

deck = [0] * 1000 + [1] * 1000
random.shuffle(deck)

roulette_wheel_selection(0)

deck = [0] * 1000 + [1] * 1000
random.shuffle(deck)

roulette_wheel_selection(50)
