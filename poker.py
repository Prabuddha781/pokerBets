from random import randrange
from checkAndScore import score_cards
from timeit import default_timer as timer

suites = ["D", "H", "C", "S"]
cards = [i for i in range(2,15)]

# function to build the deck
def deck_builder():
    deck = []
    for number in cards:
        for suite in suites:
            deck.append(str(number) + suite)
    return deck

# card_on_table stores the cards that are on the table i.e. flop, turn and river
book_of_cards = deck_builder()
cards_on_table = []

# deal a certain number of cards and remove those cards from the deck
def deal_cards(number_of_cards):
    dealt_cards = []
    for _ in range(number_of_cards):
        dealt_card = book_of_cards[randrange(0,len(book_of_cards))]
        book_of_cards.remove(dealt_card)
        dealt_cards.append(dealt_card)
    return dealt_cards

# deal the initial two cards to each player
def deal_hole_cards(number_of_players):
    if len(book_of_cards) == 52:
        number_of_cards = number_of_players * 2
        dealt_cards = deal_cards(number_of_cards)
        cards = []
        for i in range(0, number_of_cards, 2):
            cards.append([dealt_cards[i], dealt_cards[i+1]])
        return cards

# deal the flop
def deal_flop():
    if len(book_of_cards) ==48:
        flop = deal_cards(3)
        cards_on_table.extend(flop)
        return flop

# deal the river
def dealRiver():
    if len(book_of_cards) == 44:
        river = deal_cards(1)
        cards_on_table.extend(river)
        return river

# deal the turn 
def dealTurn():
    if len(book_of_cards) == 45:
        turn = deal_cards(1)
        cards_on_table.extend(turn)
        return turn

# when flop has been dealt, this function returns all the possible river and turn combinations added to the players cards to return a total of all possible 7 cards possible
def simulateRiverAndTurn():
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

# when the flop and turn has been dealt, this returns all the possible river added to the players cards to return a total of all possible 7 cards possible
def simulateRiver():
    player1Card, player2Card = hole_cards[0], hole_cards[1]
    player1Card = player1Card + cards_on_table
    player2Card = player2Card + cards_on_table
    playerAllPossibleCards = []
    for river in book_of_cards:
        playerAllPossibleCards.append([player1Card + [river], player2Card + [river]])
    return playerAllPossibleCards

# take all the card combinations possible from the last two function and pass them to the score_cards() fucntion 
# to calculate which card (player 1's or player 2's) wins. For e.g. when hole_cards and flop has been dealt, each 
# player has 5 cards that they can see plus the river and turn that are not visible yet. There are 990 possible 
# river and turn combinations. For each river and turn combination, this function sees which player wins, tallies them and returns the odds
def checkOddsCalc(simulationStage, numOfIterations):
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

# use the check_odds_calc() function to calculate player's chances post-flop
def post_flop_odds_calc(hole_card):
    global hole_cards
    hole_cards = hole_card
    return checkOddsCalc(simulateRiverAndTurn, 990)

# use the check_odds_calc() function to calculate player's chances before the river
def check_river_odds_calc():
    return checkOddsCalc(simulateRiver, 44)

# the score_cards module returns which player wins plus their card's score. For e.g. if the player has a high_card, their score is 100 vs 1000 for a straight flush
score_card_dict = {1:"Highcard", 2:"Pair", 3:"Two Pair", 4:"Three of a kind", 6:"Straight", 7:"Flush", 8:"Full House", 9:"Four of a kind", 10: "Straight Flush"}

# check which player wins after the turn is dealt. Also returns what card rank the winner was holding
def finalScore():
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

# this function takes in a proability and alters it by a random float between -0.06 and 0.04 to return a manipulated odds.
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

# once a hand is over, this function calls the deck_builder() function to build a new deck and clears the cards on 
# the table
def reset_cards():
    cards_on_table.clear()
    book_of_cards.clear()
    book_of_cards.extend(deck_builder())
