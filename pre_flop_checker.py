from poker import odds_calculator

# Basic idea behind this module: From a 52 card deck, say you deal 2 pairs of cards to two players in a poker table. Say, you deal [['14S', '14D'], ['14C', '14H']]. These are two pairs of aces 
# that each player is holding. This case is rare but it exemplifies the process perfectly.
# Now the players get 5 cards on the table. There is 48 card left on the deck so there are 48C5 combinations of cards possible - about 1.71 million combination of cards. If I write a brute 
# force algorithm to compute all the card combinations and run them through my checkAndScore module to calculate the odds of each of those 1.71 million cards, it will significantly slow down 
# the program. 
# The way my module works is by identifying the card type first - checking if the player's card is a high card or a pair. There are multiple possibilities now - a pair against a pair, a pair 
# against a highcard, a highcard against another highcard. Once the program identifies which one of these the card is, it then goes on to compare each card e.g. a pair of Kings against a pair 
# of Kings is a tie. A pair of 5s against a pair of a higher card has a 19.7% chance of winning. 
# In the first example I took, that of [['14S', '14D'], ['14C', '14H']] (both the players have a pair of Aces), we don't need to run through 1.71 million combinations to see it is a tie. 
# Similarly for most cards, the time-loss from running a brute force algorithm is not worth the slight gain in accuracy. This module works on this hypothesis.

def pre_flop_checker(cards):
    type_of_card = {"pair": [], "highCard": []}
    card_number = []
    
    for card in cards:
        card_number.append([int(i[:-1]) for i in card])

    for card in card_number:
        if len(set(card)) == 1:
            type_of_card["pair"].append(card)
        else:
            card.sort()
            type_of_card["highCard"].append(card)
        
    if len(type_of_card["pair"]) == len(cards):
        type_of_card["pair"].sort()
        higher_pair = type_of_card["pair"][0]
        lower_pair = type_of_card["pair"][1]
        if higher_pair == lower_pair:
            return {0.5001: "".join(type_of_card["pair"][1]), 0.50001: "".join(type_of_card["pair"][0])}
        return ({0.803: higher_pair, 0.197: lower_pair})

    elif len(type_of_card["pair"]) == 1:
        if type_of_card["pair"][0][0] > type_of_card["highCard"][0][1]: 
            return {0.827: type_of_card["pair"][0], 0.173: type_of_card["highCard"][0]}
        elif type_of_card["pair"][0][0] == type_of_card["highCard"][0][0]: 
            return {0.655: type_of_card["pair"][0], 0.345: type_of_card["highCard"][0]}
        elif type_of_card["pair"][0][0] == type_of_card["highCard"][0][1]: 
            return {0.855: type_of_card["pair"][0], 0.145: type_of_card["highCard"][0]}
        elif type_of_card["pair"][0][0] < type_of_card["highCard"][0][0]: 
            return {0.551: type_of_card["pair"][0], 0.449: type_of_card["highCard"][0]}
        elif type_of_card["highCard"][0][1] > type_of_card["pair"][0][0] > type_of_card["highCard"][0][0]: 
            return {0.714: type_of_card["pair"][0], 0.286: type_of_card["highCard"][0]}

    else: 
        type_of_card["highCard"].sort()
        if type_of_card["highCard"][0][1] < type_of_card["highCard"][1][0]:
            return {0.629: type_of_card["highCard"][1], 0.371: type_of_card["highCard"][0]}
        elif type_of_card["highCard"][0][0] < type_of_card["highCard"][1][0] and type_of_card["highCard"][1][1] < type_of_card["highCard"][0][1]:
            return {0.559: type_of_card["highCard"][0], 0.441: type_of_card["highCard"][1]}
        elif type_of_card["highCard"][0][0] < type_of_card["highCard"][1][0] and type_of_card["highCard"][1][1] > type_of_card["highCard"][0][1]:
            return {0.633: type_of_card["highCard"][1], 0.367: type_of_card["highCard"][0]}
        elif type_of_card["highCard"][0][0] < type_of_card["highCard"][1][0] and type_of_card["highCard"][1][0] == type_of_card["highCard"][0][1] and type_of_card["highCard"][1][1] > type_of_card["highCard"][0][1]:
            return {0.733: type_of_card["highCard"][1], 0.267: type_of_card["highCard"][0]}
        elif type_of_card["highCard"][0][1] == type_of_card["highCard"][1][1] and type_of_card["highCard"][0][0] < type_of_card["highCard"][1][0]:
            return {0.711: type_of_card["highCard"][1], 0.289: type_of_card["highCard"][0]}    
        elif type_of_card["highCard"][0][0] == type_of_card["highCard"][1][0] and type_of_card["highCard"][1][1] > type_of_card["highCard"][0][1]:
            return {0.623: type_of_card["highCard"][1], 0.289: type_of_card["highCard"][0]}
        else:
            return {0.5001: type_of_card["highCard"][1], 0.50001: type_of_card["highCard"][0]}

# The pre_flop_helper takes a list of list of integers (the pair of cards that the players are holding) as input, and separates the card number from the suite e.g. [['7', '11'], ['12', '13']] 
# and [['S', 'D'], ['C', 'H']] for [['7S', '11D'], ['12C', '13H']]. When the pre_flop_checker returns the probability for each card combinations, it then matches the probability with the card 
# and returns the odds in order.
def pre_flop_helper(cards):
    res = pre_flop_checker(cards)
    hands = []
    for card in cards:
        hands.append([int(i[:-1]) for i in card])
    p1_card = sorted(hands[0])
    p1_cards = [p1_card, sorted(p1_card, reverse=True)]
    res_keys = list(res.keys())
    odds_1 = odds_calculator(res_keys[0])
    odds_2 = odds_calculator(res_keys[1])
    if res[res_keys[0]] in p1_cards:
        return odds_1, odds_2
    if res[res_keys[1]] in p1_cards:
        return odds_2, odds_1

if __name__ == "__main__":
    print(pre_flop_helper([['6S', '9S'], ['13H', '14C']]))