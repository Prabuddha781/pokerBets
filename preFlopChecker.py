from poker import dealHoleCards, odds_calculator


def preFlopChecker(cards):
    typeOfCard = {"pair": [], "highCard": []}
    cardNumber = []
    
    for card in cards:
        cardNumber.append([int(i[:-1]) for i in card])

    for card in cardNumber:
        if len(set(card)) == 1:
            typeOfCard["pair"].append(card)
        else:
            card.sort()
            typeOfCard["highCard"].append(card)
        
    if len(typeOfCard["pair"]) == len(cards):
        typeOfCard["pair"].sort()
        higherPair = typeOfCard["pair"][0]
        lowerPair = typeOfCard["pair"][1]
        if higherPair == lowerPair:
            return {0.5001: "".join(typeOfCard["pair"][1]), 0.50001: "".join(typeOfCard["pair"][0])}
        return ({0.803: higherPair, 0.197: lowerPair})

    elif len(typeOfCard["pair"]) == 1:
        if typeOfCard["pair"][0][0] > typeOfCard["highCard"][0][1]: 
            return {0.827: typeOfCard["pair"][0], 0.173: typeOfCard["highCard"][0]}
        elif typeOfCard["pair"][0][0] == typeOfCard["highCard"][0][0]: 
            return {0.655: typeOfCard["pair"][0], 0.345: typeOfCard["highCard"][0]}
        elif typeOfCard["pair"][0][0] == typeOfCard["highCard"][0][1]: 
            return {0.855: typeOfCard["pair"][0], 0.145: typeOfCard["highCard"][0]}
        elif typeOfCard["pair"][0][0] < typeOfCard["highCard"][0][0]: 
            return {0.551: typeOfCard["pair"][0], 0.449: typeOfCard["highCard"][0]}
        elif typeOfCard["highCard"][0][1] > typeOfCard["pair"][0][0] > typeOfCard["highCard"][0][0]: 
            return {0.714: typeOfCard["pair"][0], 0.286: typeOfCard["highCard"][0]}

    else: 
        typeOfCard["highCard"].sort()
        if typeOfCard["highCard"][0][1] < typeOfCard["highCard"][1][0]:
            return {0.629: typeOfCard["highCard"][1], 0.371: typeOfCard["highCard"][0]}
        elif typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][1] < typeOfCard["highCard"][0][1]:
            return {0.559: typeOfCard["highCard"][0], 0.441: typeOfCard["highCard"][1]}
        elif typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][1] > typeOfCard["highCard"][0][1]:
            return {0.633: typeOfCard["highCard"][1], 0.367: typeOfCard["highCard"][0]}
        elif typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][0] == typeOfCard["highCard"][0][1] and typeOfCard["highCard"][1][1] > typeOfCard["highCard"][0][1]:
            return {0.733: typeOfCard["highCard"][1], 0.267: typeOfCard["highCard"][0]}
        elif typeOfCard["highCard"][0][1] == typeOfCard["highCard"][1][1] and typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0]:
            return {0.711: typeOfCard["highCard"][1], 0.289: typeOfCard["highCard"][0]}    
        elif typeOfCard["highCard"][0][0] == typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][1] > typeOfCard["highCard"][0][1]:
            return {0.623: typeOfCard["highCard"][1], 0.289: typeOfCard["highCard"][0]}
        else:
            return {0.5001: typeOfCard["highCard"][1], 0.50001: typeOfCard["highCard"][0]}

def preFlopHelper(cards):
    res = preFlopChecker(cards)
    hands = []
    for card in cards:
        hands.append([int(i[:-1]) for i in card])
    p1_card = sorted(hands[0])
    p1_cards = [p1_card, sorted(p1_card, reverse=True)]
    resKeys = list(res.keys())
    odds_1 = odds_calculator(resKeys[0])
    odds_2 = odds_calculator(resKeys[1])
    if res[resKeys[0]] in p1_cards:
        return odds_1, odds_2
    if res[resKeys[1]] in p1_cards:
        return odds_2, odds_1

if __name__ == "__main__":
    print(preFlopHelper([['6S', '9S'], ['13H', '14C']]))