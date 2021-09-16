from random import randrange
from checkAndScore import scoreCards
from timeit import default_timer as timer

suites = ["D", "H", "C", "S"]
cards = [i for i in range(2,15)]

def deckBuilder():
    deck = []
    for number in cards:
        for suite in suites:
            deck.append(str(number) + suite)
    return deck

bookOfCards = deckBuilder()
cardsOnTable = []

def dealCards(numberOfCards):
    dealtCards = []
    for _ in range(numberOfCards):
        dealtCard = bookOfCards[randrange(0,len(bookOfCards))]
        bookOfCards.remove(dealtCard)
        dealtCards.append(dealtCard)
    return dealtCards

def dealHoleCards(numberOfPlayers):
    numberOfCards = numberOfPlayers * 2
    dealtCards = dealCards(numberOfCards)
    cards = []
    for i in range(0, numberOfCards, 2):
        cards.append([dealtCards[i], dealtCards[i+1]])
    return cards

def dealFlop():
    flop = dealCards(3)
    cardsOnTable.extend(flop)
    return flop

def dealRiver():
    river = dealCards(1)
    cardsOnTable.extend(river)
    return river

def dealTurn():
    turn = dealCards(1)
    cardsOnTable.extend(turn)
    return dealCards(1)

def simulateRiverAndTurn():
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cardsOnTable
    player2Card = player2Card + cardsOnTable
    possibleRiverAndTurn = []
    for turn in range(len(bookOfCards) - 1):
        for river in range(turn + 1, len(bookOfCards)):
            possibleRiverAndTurn.append([bookOfCards[river], bookOfCards[turn]])
    playerAllPossibleCards = []
    for possiblePostFlop in possibleRiverAndTurn:
        playerAllPossibleCards.append([player1Card + possiblePostFlop, player2Card + possiblePostFlop])
    return playerAllPossibleCards

def simulateRiver():
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cardsOnTable
    player2Card = player2Card + cardsOnTable
    playerAllPossibleCards = []
    for turn in bookOfCards:
        playerAllPossibleCards.append([player1Card + [turn], player2Card + [turn]])
    return playerAllPossibleCards


def checkOddsCalc(simulationStage, numOfIterations):
    simulatedCards = simulationStage()
    p1win, p2win = 0, 0
    tie = 0
    for cardSets in simulatedCards:
        p1score, p2score, cards1, cards2 = scoreCards(cardSets[0], cardSets[1])
        if p1score == 1 or p2score == 1:
            p1win += p1score
            p2win += p2score
        else:
            tie += 1
    p1WinOdds = p1win/numOfIterations
    p2WinOdds = p2win/numOfIterations
    tieOdds = tie/numOfIterations
    p1_win_odds = odds_calculator(p1WinOdds)
    p2_win_odds = odds_calculator(p2WinOdds)
    tie_odds = odds_calculator(tieOdds)
    return(p1_win_odds, p2_win_odds, tie_odds)

def postFlopOddsCalc(hole_card):
    print(cardsOnTable, "postFlopOddsCheck")
    global hole_cards
    hole_cards = hole_card
    return checkOddsCalc(simulateRiverAndTurn, 990)

def checkRiverOddsCalc():
    return checkOddsCalc(simulateRiver, 44)

def finalScore():
    print(hole_cards, "hole cards")
    print(cardsOnTable, "cards On table")
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cardsOnTable
    player2Card = player2Card + cardsOnTable
    print(hole_cards, "hole cards")
    print(cardsOnTable, "cards On table")
    p1, p2, cards1, cards2 = scoreCards(player1Card, player2Card)
    if p1 > p2:
        return "Player 1 Wins"
    elif p2 > p1:
        return "Player 2 Wins"
    else:
        "It's a draw" 

def odds_calculator(probability):
    if probability != 0:
        odds_manipulator = (randrange(-6,4))/100
        odds = round(1/(probability/(1-probability)),1) + odds_manipulator
        if odds < 0:
            return 0.02
    else:
        odds = 100
    return odds

if __name__ == "__main__":
    print(odds_calculator(0.99))
