def computer_play():
    for i in range(len(hand)):
        if (
            GraveTop.getColor == hand[i].getColor
            or GraveTop.getCardNum == hand[i].getCardNum
        ):
            possible_cards.append[hand[i]]

    if len(possible_cards) != 0:
        ran = random.randrange(possible_cards)
        give_card(hand[ran])

        if len(hand) == 1:
            uno()
    else:
        get_card()
