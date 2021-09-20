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
    if len(bookOfCards) == 52:
        numberOfCards = numberOfPlayers * 2
        dealtCards = dealCards(numberOfCards)
        cards = []
        for i in range(0, numberOfCards, 2):
            cards.append([dealtCards[i], dealtCards[i+1]])
        return cards

def dealFlop():
    if len(bookOfCards) ==48:
        flop = dealCards(3)
        cardsOnTable.extend(flop)
        return flop

def dealRiver():
    if len(bookOfCards) == 44:
        river = dealCards(1)
        cardsOnTable.extend(river)
        return river

def dealTurn():
    if len(bookOfCards) == 45:
        turn = dealCards(1)
        cardsOnTable.extend(turn)
        return turn

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
    for river in bookOfCards:
        playerAllPossibleCards.append([player1Card + [river], player2Card + [river]])
    return playerAllPossibleCards


def checkOddsCalc(simulationStage, numOfIterations):
    simulatedCards = simulationStage()
    p1win, p2win = 0, 0
    tie = 0
    for cardSets in simulatedCards:
        p1score, p2score, card1_score, cards_score = scoreCards(cardSets[0], cardSets[1])
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
    global hole_cards
    hole_cards = hole_card
    return checkOddsCalc(simulateRiverAndTurn, 990)

def checkRiverOddsCalc():
    return checkOddsCalc(simulateRiver, 44)

score_card_dict = {1:"Highcard", 2:"Pair", 3:"Two Pair", 4:"Three of a kind", 6:"Straight", 7:"Flush", 8:"Full House", 9:"Four of a kind", 10: "Straight Flush"}

def finalScore():
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cardsOnTable
    player2Card = player2Card + cardsOnTable
    p1, p2, card1_score, card2_score = scoreCards(player1Card, player2Card)
    if p1 > p2:
        card_rank = score_card_dict[card1_score//100]
        return "Player 1 Wins", card_rank
    elif p2 > p1:
        card_rank = score_card_dict[card2_score//100]
        return "Player 2 Wins", card_rank
    else:
        card_rank = score_card_dict[card1_score//100]
        return "It's a draw", card_rank 

def odds_calculator(probability):
    if probability == 0:
        odds = 100
    elif probability != 1:
        odds_manipulator = (randrange(-6,4))/100
        odds = round(1/(probability/(1-probability)),1) + odds_manipulator
        if odds < 0:
            return 0.02
    else:
        odds = 0.02
    return odds

def reset_cards():
    cardsOnTable.clear()
    bookOfCards.clear()
    bookOfCards.extend(deckBuilder())
