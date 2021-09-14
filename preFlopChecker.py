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