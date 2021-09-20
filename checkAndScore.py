# takes as input a list of card numbers not card and suites combined
def check_four_of_a_kind(card):
    set_card = set(card)
    if len(set_card) <= 4: 
        for i in card:
            if card.count(i) == 4:
                set_card.remove(i)
                return 900 + i + (max(set_card)/100)
    return 0

# takes as input a list of card numbers not card and suites combined
def check_full_house(card):
    card.sort(reverse=True)
    score = 800
    set_card = set(card)
    if len(set_card) <= 4: 
        for i in card:
            if card.count(i) == 3:
                set_card.remove(i)
                if len(set_card) <= 3:
                    list_card = list(set_card)
                    list_card.sort(reverse=True)
                    for j in list_card:
                        if card.count(j) >= 2:
                            score += i + j/100
                    return score
    return 0

def check_flush(card, suites):
    score = 700
    possible_flushes = []
    for i, j in enumerate(suites):
        if suites.count(j) >= 5:
            possible_flushes.append(card[i])
    if possible_flushes:
        possible_flushes.sort(reverse=True)
        highest_possible_flushes = possible_flushes[:5]
        for k in range(5):
            score += max(highest_possible_flushes)/10**k
            highest_possible_flushes.remove(max(highest_possible_flushes))
        return score, possible_flushes 
    return 0, 0

def check_straight(card):
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
def check_three_of_a_kind(card): 
    score = 400
    set_card =  set(card)
    if len(set_card) <= 5: 
        for i in card:
            if card.count(i) == 3:
                score += i
                set_card.remove(i)
                second_highest = max(set_card)
                score += second_highest/100
                set_card.remove(second_highest)
                third_highest = max(set_card)
                score += third_highest/1000
                return score
    return 0

def check_two_pair(card):
    score = 300
    card_no_dup = list(set(card))
    card_no_dup.sort(reverse=True)
    set_card_2 = set(card)
    try:
        if len(card_no_dup) == 4 or len(card_no_dup) == 5:
            pairs = []
            for i in card_no_dup:
                if len(pairs) < 2:
                    if card.count(i) == 2:
                        pairs.append(i)
                        set_card_2.remove(i)
                else: 
                    break
            pairs.sort(reverse=True)
            score += pairs[0] + pairs[1]/100  + max(set_card_2)/10000
            return score
    except IndexError:
        pass
    return 0

def check_pair(card):
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

def check_high_card(card):
    score = 100
    card.sort(reverse=True)
    for i in range(5):
        score += max(card)/15**i
        card.remove(max(card))
    return score

def check_straight_flush(card, suites):
    if check_flush(card, suites) != 0:
        score, cards = check_flush(card, suites)
        if score > 0:
            res = check_straight(cards)
            if res > 0:
                return res + 400
            return 0
    return 0

def score_cards(cards1, cards2):
    card1, card2 = [], []
    suites1, suites2 = [], []
    for i in cards1: 
        card1.append(int(i[:-1]))
        suites1.append(i[-1])
    for j in cards2:
        card2.append(int(j[:-1]))
        suites2.append(j[-1])
    p1_score, p2_score = 0, 0
    p1_score = check_straight_flush(card1,suites1)
    p2_score = check_straight_flush(card2, suites2)
    if p1_score == 0 and p2_score == 0:
        p1_score = check_four_of_a_kind(card1)
        p2_score = check_four_of_a_kind(card2) 
        if p1_score == 0 and p2_score == 0:
            p1_score = check_full_house(card1)
            p2_score = check_full_house(card2) 
            if p1_score == 0 and p2_score == 0:
                p1_score, possible_flushes = check_flush(card1, suites1)
                p2_score, possible_flushes = check_flush(card2, suites2)             
                if p1_score == 0 and p2_score == 0:
                    p1_score = check_straight(card1)
                    p2_score =  check_straight(card2)                      
                    if p1_score == 0 and p2_score == 0:
                        p1_score = check_three_of_a_kind(card1)
                        p2_score =  check_three_of_a_kind(card2)                        
                        if p1_score == 0 and p2_score == 0:
                            p1_score = check_two_pair(card1)
                            p2_score =  check_two_pair(card2)    
                            if p1_score == 0 and p2_score == 0:
                                p1_score = check_pair(card1)
                                p2_score =  check_pair(card2)    
                                if p1_score == 0 and p2_score == 0:
                                    p1_score = check_high_card(card1)
                                    p2_score =  check_high_card(card2)
    if p1_score > p2_score:
        return 1, 0, p1_score, p2_score
    elif p2_score > p1_score:
        return 0, 1, p1_score, p2_score
    else:
        return 0, 0, p1_score, p2_score

if __name__ == "__main__":
    print(score_cards(['5D', '2H', '7D', '4H', '5S', '8H', '6H'], ['6S', '2H', '7D', '4H', '5S', '8H', '6H']))