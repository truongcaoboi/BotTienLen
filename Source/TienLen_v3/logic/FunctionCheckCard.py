import numpy as np
from logic.Function import Function

function = Function()
def checkCardA(iCard):
    numCard = function.getNumCardByCardId(iCard)
    if(numCard == 14):
        return function.getSuitCardByCardId(iCard)
    else:
        return -1
def checkCardTwo(iCard):
    numCard = function.getNumCardByCardId(iCard)
    if(numCard == 2):
        return function.getSuitCardByCardId(iCard)
    else:
        return -1

def checkInPair(iCard, cards):
    arrIds = []
    numCard = function.getNumCardByCardId(iCard)
    for num in cards:
        if(function.getNumCardByCardId(num) == numCard):
            arrIds.append(num)
    if(len(arrIds) >= 2):
        return True
    return False

def checkInThreeOfKind(iCard, cards):
    arrIds = []
    numCard = function.getNumCardByCardId(iCard)
    for num in cards:
        if(function.getNumCardByCardId(num) == numCard):
            arrIds.append(num)
    if(len(arrIds) >= 3):
        return True
    return False

def checkInFourOfKind(iCard, cards):
    arrIds = []
    numCard = function.getNumCardByCardId(iCard)
    for num in cards:
        if(function.getNumCardByCardId(num) == numCard):
            arrIds.append(num)
    if(len(arrIds) == 4):
        return True
    return False

def checkInTwoPairStraight(iCard, cards):
    start = 0
    end = 0
    result = []
    numCard = function.getNumCardByCardId(iCard)
    if(numCard <= 2):
        return False
    for i in range(15):
        if(i > 2):
            if checkInPair(i - 1,cards):
                if start == 0:
                    start = i
                else:
                    end = i
            else:
                if start != 0 and end != 0 and (end - start)>=1:
                    result.append([start, end])
                start = 0
                end = 0
    if start != 0 and end != 0 and (end - start)>=1:
        result.append([start, end])
    for arr in result:
        if(numCard >= arr[0] and numCard <= arr[1]):
            return True
    return False

def checkInThreePairStraight(iCard, cards):
    start = 0
    end = 0
    result = []
    numCard = function.getNumCardByCardId(iCard)
    if(numCard <= 2):
        return False
    for i in range(15):
        if(i > 2):
            if checkInPair(i - 1,cards):
                if start == 0:
                    start = i
                else:
                    end = i
            else:
                if start != 0 and end != 0 and (end - start) >= 2:
                    result.append([start, end])
                start = 0
                end = 0
    if start != 0 and end != 0 and (end - start)>=2:
        result.append([start, end])
    for arr in result:
        if(numCard >= arr[0] and numCard <= arr[1]):
            return True
    return False

def checkInFourPariStraight(iCard, cards):
    start = 0
    end = 0
    result = []
    numCard = function.getNumCardByCardId(iCard)
    if(numCard <= 2):
        return False
    for i in range(15):
        if(i > 2):
            if checkInPair(i - 1,cards):
                if start == 0:
                    start = i
                else:
                    end = i
            else:
                if start != 0 and end != 0 and (end - start) >= 3:
                    result.append([start, end])
                start = 0
                end = 0
    if start != 0 and end != 0 and (end - start)>=3:
        result.append([start, end])
    for arr in result:
        if(numCard >= arr[0] and numCard <= arr[1]):
            return True
    return False

def checkInFivePariStraight(iCard, cards):
    start = 0
    end = 0
    result = []
    numCard = function.getNumCardByCardId(iCard)
    if(numCard <= 2):
        return False
    for i in range(15):
        if(i > 2):
            if checkInPair(i - 1,cards):
                if start == 0:
                    start = i
                else:
                    end = i
            else:
                if start != 0 and end != 0 and (end - start) >= 4:
                    result.append([start, end])
                start = 0
                end = 0
    if start != 0 and end != 0 and (end - start)>=4:
        result.append([start, end])
    for arr in result:
        if(numCard >= arr[0] and numCard <= arr[1]):
            return True
    return False


def checkInStraight(iCard, cards):
    maxLength = 0
    start = 0
    end = 0
    result = []
    numCard = function.getNumCardByCardId(iCard)
    if(numCard <= 2):
        return maxLength
    for i in range(15):
        if(i > 2):
            count = 0
            for num in cards:
                if function.getNumCardByCardId(num) == i:
                    count = 1
                    break
            if(count == 1):
                if start == 0:
                    start = i
                else:
                    end = i
            else:
                if start != 0 and end != 0 and (end - start) >= 2:
                    result.append([start, end])
                start = 0
                end = 0
    if start != 0 and end != 0 and (end - start)>=2:
        result.append([start, end])
    for arr in result:
        if(numCard >= arr[0] and numCard <= arr[1]):
            lenStraight = arr[1] - arr[0] + 1
            if(lenStraight > maxLength):
                maxLength = lenStraight
    return maxLength

def checkInStraightFlush(iCard, cards):
    maxLength = 0
    start = 0
    end = 0
    result = []
    numCard = function.getNumCardByCardId(iCard)
    suitCard = function.getSuitCardByCardId(iCard)
    if numCard <= 2:
        return maxLength
    for i in range(15):
        if(i > 2):
            count = 0
            for num in cards:
                if function.getNumCardByCardId(num) == i and function.getSuitCardByCardId(num) == suitCard:
                    count = 1
                    break
            if(count == 1):
                if start == 0:
                    start = i
                else:
                    end = i
            else:
                if start != 0 and end != 0 and (end - start) >= 2:
                    result.append([start, end])
                start = 0
                end = 0
    if start != 0 and end != 0 and (end - start)>=2:
        result.append([start, end])
    for arr in result:
        if(numCard >= arr[0] and numCard <= arr[1]):
            lenStraight = arr[1] - arr[0] + 1
            if(lenStraight > maxLength):
                maxLength = lenStraight
    return maxLength

def arrCardHasFourCardTwo(cards):
    iCard = 1
    return checkInFourOfKind(iCard, cards)

def arrCardHasFullStraight(cards):
    iCard = 2
    return  checkInStraight(iCard, cards) == 12
    
def arrCardHasSixPair(cards):
    countPair = 0
    for i in range(14):
        if(i>0):
            if(checkInPair(i, cards)):
                countPair += 1
    if(countPair == 6):
        return True
    return False

def arrCardHasFourThreeOfKind(cards):
    countThreeOfKind = 0
    for i in range(14):
        if(i > 0):
            if(checkInThreeOfKind(i, cards)):
                countThreeOfKind += 1
    if(countThreeOfKind == 4):
        return True
    return False

def arrCardHasFivePairStraight(cards):
    for i in range(10):
        if(i>1):
            if(checkInFivePariStraight(i,cards)):
                return True
    return False

def arrCardHasGroupThreeSpiderBiggerThanCardTwo(cards):
    iCard = 2
    if iCard in cards:
        if(checkInFourOfKind(iCard, cards)):
            return True
        if(checkInThreePairStraight(iCard, cards)):
            return True
        if(checkInFourPariStraight(iCard, cards)):
            return True
    return False

def checkFastWin(cardsOrigin, isInitGame):
    cards = function.sortCard(cardsOrigin)
    if(arrCardHasFourCardTwo(cards)):
        return 10
    if(arrCardHasFullStraight(cards)):
        return 9
    if(arrCardHasSixPair(cards)):
        return 8
    if(arrCardHasFourThreeOfKind(cards)):
        return 7
    if(arrCardHasFivePairStraight(cards)):
        return 6
    if(arrCardHasGroupThreeSpiderBiggerThanCardTwo(cards) and isInitGame):
        return 5
    return -1

# ham bo sung
def arrCardHasFourOfKind(arrCard):
    for i in range(14):
        if(i > 0):
            if(checkInFourOfKind(i, arrCard)):
                return True
    return False

def arrCardHasThreePairStraight(arrCard):
    for i in range(14):
        if(i > 1):
            if(checkInThreePairStraight(i, arrCard)):
                return True
    return False

def arrCardHasFourPairStraight(arrCard):
    for i in range(14):
        if(i > 1):
            if(checkInFourPariStraight(i, arrCard)):
                return True
    return False