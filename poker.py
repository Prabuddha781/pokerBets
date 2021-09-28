from random import randrange
from checkAndScore import score_cards
from timeit import default_timer as timer

suites = ["D", "H", "C", "S"]
cards = [i for i in range(2,15)]

def deck_builder():
    """This function builds a deck of cards
    :rtype : list of str
    """
    deck = []
    for number in cards:
        for suite in suites:
            deck.append(str(number) + suite)
    return deck

book_of_cards = deck_builder() 
cards_on_table = [] #this stores the cards that are on the table i.e. the flop, turn and river

def deal_cards(number_of_cards):
    """This function deals cards and removes the card from the deck.
    :type number_of_cards: int
    :rtype: list of str
    """
    dealt_cards = []
    for _ in range(number_of_cards):
        dealt_card = book_of_cards[randrange(0,len(book_of_cards))]
        book_of_cards.remove(dealt_card)
        dealt_cards.append(dealt_card)
    return dealt_cards

def deal_hole_cards(number_of_players):
    """This function deals the initial two cards (hole cards)
    :type number_of_cards: int
    :rtype: list of str
    """
    if len(book_of_cards) == 52:
        number_of_cards = number_of_players * 2
        dealt_cards = deal_cards(number_of_cards)
        cards = []
        for i in range(0, number_of_cards, 2):
            cards.append([dealt_cards[i], dealt_cards[i+1]])
        return cards

def deal_flop():
    """This function deals the flop (3 cards) and adds the cards to the cards_on_table
    :rtype: list of str
    """
    if len(book_of_cards) ==48:
        flop = deal_cards(3)
        cards_on_table.extend(flop)
        return flop

def dealRiver():
    """This function deals the river card (1 card) and adds the cards to the cards_on_table
    :rtype: list of str
    """
    if len(book_of_cards) == 44:
        river = deal_cards(1)
        cards_on_table.extend(river)
        return river

def dealTurn():
    """This function deals the Turn card (1 card) 
    and adds the cards to the cards_on_table
    :rtype: list of str
    """
    if len(book_of_cards) == 45:
        turn = deal_cards(1)
        cards_on_table.extend(turn)
        return turn

dealTurn()

def simulateRiverAndTurn():
    """
    This function returns all the possible river and turn cards 
    :possible from the deck after the flop has been dealt
    """
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cards_on_table
    player2Card = player2Card + cards_on_table
    possibleRiverAndTurn = []
    for turn in range(len(book_of_cards) - 1):
        for river in range(turn + 1, len(book_of_cards)):
            possibleRiverAndTurn.append([book_of_cards[river], book_of_cards[turn]])
    playerAllPossibleCards = []
    for possiblePostFlop in possibleRiverAndTurn:
        playerAllPossibleCards.append([player1Card + possiblePostFlop, player2Card + possiblePostFlop])
    return playerAllPossibleCards

def simulateRiver():
    """
    This function returns all the possible river cards once 
    :the turn card has been dealt
    """
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cards_on_table
    player2Card = player2Card + cards_on_table
    playerAllPossibleCards = []
    for river in book_of_cards:
        playerAllPossibleCards.append([player1Card + [river], player2Card + [river]])
    return playerAllPossibleCards


def checkOddsCalc(simulationStage, numOfIterations):
    """
    This function returns the odds of player 1 and player 2 at different 
    :stages in the game. This function takes in as input all possible cards.
    :(e.g. river and turn when the flop has been dealt) and passes 
    :these cards to the score_hands() function. The scores are then tallied
    :and the odds of each player winning or the odds of a tie are calculated
    :type simulationStage: function object
    :type numOfIterations: int
    :rtype: tuple of floats
    """
    simulatedCards = simulationStage()
    p1win, p2win = 0, 0
    tie = 0
    for cardSets in simulatedCards:
        p1score, p2score, card1_score, cards_score = score_cards(cardSets[0], cardSets[1])
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

def post_flop_odds_calc(hole_card):
    """This function passes the simulateRiverAndTurn function object to the checkOddsCalc 
    function to return the odds of players winning post-flop.
    """
    global hole_cards
    hole_cards = hole_card
    return checkOddsCalc(simulateRiverAndTurn, 990)

def check_river_odds_calc():
    """This function passes the simulateRiver function object to the checkOddsCalc 
    function to return the odds of players after the turn has been dealt.
    """
    return checkOddsCalc(simulateRiver, 44)


score_card_dict = {
                  1:"Highcard", 2:"Pair", 3:"Two Pair", 4:"Three of a kind", 6:"Straight", 
                  7:"Flush", 8:"Full House", 9:"Four of a kind", 10: "Straight Flush"
                  } #this dictionary is accessed by the finalScore() function to return the rank of the card 


def finalScore():
    """This funciton is called after the river has been dealt and it returns which player 
    :wins based on the cards they have. The function also returns the rank of the card
    :e.g. High Card or Flush
    :rtype: str, str
    """
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cards_on_table
    player2Card = player2Card + cards_on_table
    p1, p2, card1_score, card2_score = score_cards(player1Card, player2Card)
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
    """This function takes in as input the probability of a player's chances 
    of winning and converts that to odds. The function manipulates the odds to
    give the player or the house an edge e.g. if the true odds are 1 to 4, the function 
    manipulates it in the range of 3.94-4.04.
    :type probability: float
    :rtype odds: float
    """
    if probability == 0:
        odds = 100
    elif probability != 1:
        odds_manipulator = (randrange(-6,4))/100
        odds = round(1/(probability/(1-probability)),1) + odds_manipulator
        if odds <= 0:
            return 0.02
    else:
        odds = 0.02
    return odds


def reset_cards():
    """This function is called when one round of play has been completed. It resets the
    cards on the table and the deck (the deck goes back to 52 cards)."""
    cards_on_table.clear()
    book_of_cards.clear()
    book_of_cards.extend(deck_builder())
