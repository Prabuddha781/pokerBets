


def finalScore():
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card += cardsOnTable
    player2Card += cardsOnTable
    print(hole_cards)
    print(cardsOnTable)
    p1, p2, cards1, cards2 = scoreCards(player1Card, player2Card)
    if p1 > p2:
        return "Player 1 Wins"
    elif p2 > p1:
        return "Player 2 Wins"
    else:
        "It's a draw" 
