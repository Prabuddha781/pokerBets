def cardNumbers(card):
    res = []
    for i in card:
        res.append(i[:-1])
    return res

# takes as input a list of card numbers not card and suites combined
def checkFourOfAKind(card):
    setCard = set(card)
    if len(setCard) <= 4: 
        for i in card:
            if card.count(i) == 4:
                setCard.remove(i)
                return 900 + i + (max(setCard)/100)
    return 0

# takes as input a list of card numbers not card and suites combined
def checkFullHouse(card):
    card.sort(reverse=True)
    score = 800
    setCard = set(card)
    if len(setCard) <= 4: 
        for i in card:
            if card.count(i) == 3:
                setCard.remove(i)
                if len(setCard) <= 3:
                    listCard = list(setCard)
                    listCard.sort(reverse=True)
                    for j in listCard:
                        if card.count(j) >= 2:
                            score += i + j/100
                    return score
    return 0

def checkFlush(card, suites):
    score = 700
    possibleFlushes = []
    setSuites = set(suites)
    for i, j in enumerate(suites):
        if suites.count(j) >= 5:
            possibleFlushes.append(card[i])
    if possibleFlushes:
        possibleFlushes.sort(reverse=True)
        highestPossibleFlushes = possibleFlushes[:5]
        for k in range(5):
            score += max(highestPossibleFlushes)/10**k
            highestPossibleFlushes.remove(max(highestPossibleFlushes))
        return score, possibleFlushes 
    return 0, 0

def checkStraight(card):
    card = list(set(card))
    card.sort(reverse=True)
    for i in range(len(card)-4):
        try:
            if card[i] == card[i+4] + 4:
                return 600 + card[i]
        except IndexError:
            return 0
    try:
        if 14 in card:
            if card[-4] == 5:
                return 601  
    except IndexError:
        return 0
    return 0

# takes as input a list of card numbers not card and suites combined
def checkThreeOfAKind(card): 
    score = 400
    setCard =  set(card)
    if len(setCard) <= 5: 
        for i in card:
            if card.count(i) == 3:
                score += i
                setCard.remove(i)
                secondHighest = max(setCard)
                score += secondHighest/100
                setCard.remove(secondHighest)
                thirdHighest = max(setCard)
                score += thirdHighest/1000
                return score
    return 0

def checkTwoPair(card):
    score = 300
    card_no_dup = list(set(card))
    card_no_dup.sort(reverse=True)
    setCard2 = set(card)
    if len(card_no_dup) == 4 or len(card_no_dup) == 5:
        pairs = []
        for i in card_no_dup:
            if len(pairs) < 2:
                if card.count(i) == 2:
                    pairs.append(i)
                    setCard2.remove(i)
            else: 
                break
        pairs.sort(reverse=True)
        score += pairs[0] + pairs[1]/100  + max(setCard2)/10000
        return score
    return 0

def checkPair(card):
    score = 200
    if len(set(card)) == 6:
        for i in card:
            if card.count(i) == 2:
               score += i
               card.remove(i)
        card.sort(reverse=True)
        score += card[0]/15 + card[1]/225 + card[2]/3375 + card[3]/50625
        return score
    return 0

def checkHighCard(card):
    score = 100
    card.sort(reverse=True)
    for i in range(5):
        score += max(card)/15**i
        card.remove(max(card))
    return score

def checkStraightFlush(card, suites):
    if checkFlush(card, suites) != 0:
        score, cards = checkFlush(card, suites)
        if score > 0:
            res = checkStraight(cards)
            if res > 0:
                return res + 400
            return 0
    return 0

def scoreCards(cards1, cards2):
    card1, card2 = [], []
    suites1, suites2 = [], []
    for i in cards1: 
        card1.append(int(i[:-1]))
        suites1.append(i[-1])
    for j in cards2:
        card2.append(int(j[:-1]))
        suites2.append(j[-1])
    p1score, p2score = 0, 0
    p1score = checkStraightFlush(card1,suites1)
    p2score = checkStraightFlush(card2, suites2)
    if p1score == 0 and p2score == 0:
        p1score = checkFourOfAKind(card1)
        p2score = checkFourOfAKind(card2) 
        if p1score == 0 and p2score == 0:
            p1score = checkFullHouse(card1)
            p2score = checkFullHouse(card2) 
            if p1score == 0 and p2score == 0:
                p1score, possibleFlushes = checkFlush(card1, suites1)
                p2score, PossibleFlushes = checkFlush(card2, suites2)             
                if p1score == 0 and p2score == 0:
                    p1score = checkStraight(card1)
                    p2score =  checkStraight(card2)                      
                    if p1score == 0 and p2score == 0:
                        p1score = checkThreeOfAKind(card1)
                        p2score =  checkThreeOfAKind(card2)                        
                        if p1score == 0 and p2score == 0:
                            p1score = checkTwoPair(card1)
                            p2score =  checkTwoPair(card2)    
                            if p1score == 0 and p2score == 0:
                                p1score = checkPair(card1)
                                p2score =  checkPair(card2)    
                                if p1score == 0 and p2score == 0:
                                    p1score = checkHighCard(card1)
                                    p2score =  checkHighCard(card2)
    if p1score > p2score:
        return 1, 0, cards1, cards2
    elif p2score > p1score:
        return 0, 1, cards1, cards2
    else:
        print("not found", cards1, cards2)
        return 0, 0, cards1, cards2

if __name__ == "__main__":
    print(scoreCards(['6C', '6H', '12D', '11S', '6S', '11C', '10S'],['11D', '10H', '12D', '11S', '6S', '11C', '10S']))