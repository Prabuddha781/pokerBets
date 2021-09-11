from random import randrange


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
    return dealCards(1)

def dealTurn():
    turn = dealCards(1)
    cardsOnTable.extend(turn)
    return dealCards(1)

def preFlopChecker(cards):
    typeOfCard = {"pair": [], "highCard": []}
    cardNumber = []
    cardDict = {}
    
    for card in cards:
        cardNumber.append([int(i[:-1]) for i in card])
        cardDict[card] = [i[-1] for i in card]

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
            return {"50%": typeOfCard["pair"][1], "50%": typeOfCard["pair"][0]}
        return ({"80.3%": higherPair, "19.7%": lowerPair})

    elif len(typeOfCard["pair"]) == 1:
        if typeOfCard["pair"][0][0] > typeOfCard["highCard"][0][1]: 
            return {"82.7%": typeOfCard["pair"][0], "17.3%": typeOfCard["highCard"]}
        elif typeOfCard["pair"][0][0] == typeOfCard["highCard"][0][0]: 
            return {"65.5%": typeOfCard["pair"][0], "34.5%": typeOfCard["highCard"]}
        elif typeOfCard["pair"][0][0] == typeOfCard["highCard"][0][1]: 
            return {"85.5%": typeOfCard["pair"][0], "14.5%": typeOfCard["highCard"]}
        elif typeOfCard["pair"][0][0] < typeOfCard["highCard"][0][0]: 
            return {"55.1%": typeOfCard["pair"][0], "44.9%": typeOfCard["highCard"]}
        elif typeOfCard["highCard"][0][1] > typeOfCard["pair"][0][0] > typeOfCard["highCard"][0][0]: 
            return {"71.4%": typeOfCard["pair"][0], "28.6%": typeOfCard["highCard"]}

    else: 
        typeOfCard["highCard"].sort()
        if typeOfCard["highCard"][0][1] < typeOfCard["highCard"][1][0]:
            return {"62.9%": typeOfCard["highCard"][1], "37.1%": typeOfCard["highCard"]}
        elif typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][1] < typeOfCard["highCard"][0][1]:
            return {"55.9%": typeOfCard["highCard"][0], "44.1%": typeOfCard["highCard"][1]}
        elif typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][1] > typeOfCard["highCard"][0][1]:
            return {"63.3%": typeOfCard["highCard"][1], "36.7%": typeOfCard["highCard"][0]}
        elif typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][0] == typeOfCard["highCard"][0][1] and typeOfCard["highCard"][1][1] > typeOfCard["highCard"][0][1]:
            return {"73.3%": typeOfCard["highCard"][1], "26.7%": typeOfCard["highCard"][0]}
        elif typeOfCard["highCard"][0][1] == typeOfCard["highCard"][1][1] and typeOfCard["highCard"][0][0] < typeOfCard["highCard"][1][0]:
            return {"71.1%": typeOfCard["highCard"][1], "28.9%": typeOfCard["highCard"][0]}    
        elif typeOfCard["highCard"][0][0] == typeOfCard["highCard"][1][0] and typeOfCard["highCard"][1][1] > typeOfCard["highCard"][0][1]:
            return {"62.3%": typeOfCard["highCard"][1], "28.9%": typeOfCard["highCard"][0]}
        else:
            return {"50%": typeOfCard["highCard"][1], "50%": typeOfCard["highCard"][0]}

def players():
    def simulateRiverAndTurn():
        possibleRiverAndTurn = []
        for turn in range(len(bookOfCards) - 1):
            for river in range(len(bookOfCards)):
                possibleRiverAndTurn.append([bookOfCards[river], bookOfCards[turn]])
        return possibleRiverAndTurn
    card = dealHoleCards(2)
    player1Card, player2Card = card[0], card[1]
    print(player1Card, player2Card)
    print(cardsOnTable)
    player1Card.extend(cardsOnTable), player2Card.extend(cardsOnTable)
    possibleRiverAndTurn = simulateRiverAndTurn()
    player1AllPossibleCards = []
    player2AllPossibleCards = []
    for possiblePostFlop in possibleRiverAndTurn:
        player1AllPossibleCards.append(player1Card + possiblePostFlop)
        player2AllPossibleCards.append(player2Card + possiblePostFlop)
    # player1CardNums, player2CardNums = [i[:-1] for i in player1AllCard], [i[-1] for i in player2AllCard]
    return player1AllPossibleCards

dealFlop()
print(players())

def check_four_of_a_kind(handNum):
    for i in handNum:
        if handNum.count(i) == 4:
            four = i
        elif numbers.count(i) == 1:
            card = i
    score = 105 + four + card/100
    return score

def check_full_house(hand,letters,numbers,rnum,rlet):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    score = 90 + full + p/100  
    return score

def check_three_of_a_kind(hand,letters,numbers,rnum,rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else: 
            cards.append(i)
    score = 45 + three + max(cards) + min(cards)/1000
    return score

def check_two_pair(hand,letters,numbers,rnum,rlet):
    pairs = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pairs.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 30 + max(pairs) + min(pairs)/100 + cards[0]/1000
    return score

def check_pair(hand,letters,numbers,rnum,rlet):    
    pair = []
    cards  = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:    
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 15 + pair[0] + cards[0]/100 + cards[1]/1000 + cards[2]/10000
    return score