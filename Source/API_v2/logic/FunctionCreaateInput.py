from numpy.core.records import array
from numpy.lib.function_base import append
from .Function import Function 
from . import FunctionCheckCard as fcc
import numpy as np

function = Function()

def createInfoCurrentCard(player):
    cardsPlayer = np.ndarray.tolist(player.idCards)
    cards = cardsPlayer.copy()
    cards = np.array(cards)
    cards = function.sortCard(cards)
    result = []
    for iCard in cards:
        arrBin = np.zeros((41), dtype= np.int_)
        numCard = function.getNumCardByCardId(iCard)
        suitCard = function.getSuitCardByCardId(iCard)
        arrBin[numCard - 2] = 1
        arrBin[12 + suitCard] = 1
        if(fcc.checkInFourOfKind(iCard, cards)):
            arrBin[19] = 1
            arrBin[18] = 1
            arrBin[17] = 1
        elif(fcc.checkInThreeOfKind(iCard, cards)):
            arrBin[18] = 1
            arrBin[17] = 1
        if (fcc.checkInFourPariStraight(iCard, cards)):
            arrBin[22] = 1
            arrBin[21] = 1
            arrBin[20] = 1
            arrBin[17] = 1
        elif (fcc.checkInThreePairStraight(iCard, cards)):
            arrBin[21] = 1
            arrBin[20] = 1
            arrBin[17] = 1
        elif (fcc.checkInTwoPairStraight(iCard, cards)):
            arrBin[20] = 1
            arrBin[17] = 1
        elif (fcc.checkInPair(iCard,cards)):
            arrBin[17] = 1
        lengthFlushStraight = fcc.checkInStraightFlush(iCard, cards)
        for i in range(lengthFlushStraight+1):
            if(i>2):
                arrBin[32 + i - 3] = 1
        lengthStraight = fcc.checkInStraight(iCard, cards)
        for i in range(lengthStraight+1):
            if(i>2):
                arrBin[23 + i - 3] = 1
        result.append(arrBin)
    while(len(result) < 13):
        arrBin = np.zeros((41), dtype= np.int_)
        result.append(arrBin)
    result = np.array(result)
    result = result.reshape((533))
    return result

def createInfoOtherPlayers(listPlayer, indexCurrentPlayer):
    lsp = []
    if(indexCurrentPlayer == 0):
        lsp = listPlayer[1:]
    elif(indexCurrentPlayer == len(listPlayer) - 1):
        lsp = listPlayer[:indexCurrentPlayer]
    else:
        lsp = listPlayer[indexCurrentPlayer+1:]
        lsp += listPlayer[:indexCurrentPlayer]
    result = []
    for player in lsp:
        arrBin = np.zeros((36), dtype= np.int_)
        countCard = len(player.idCards)
        cardPlayeds = player.currentPlayed
        bin = function.convertUnSignIntegerToArrayBinary(countCard,4)
        for i in range(4):
            arrBin[i] = bin[i]
        for arrCard in cardPlayeds:
            typeArrCard = function.getTypeArrCard(arrCard)
            if typeArrCard == function.TYPE_ONE or typeArrCard == function.TYPE_ONE_2:
                if(fcc.checkCardA(arrCard[0]) > 0):
                    arrBin[3 + fcc.checkCardA(arrCard[0])] = 1
                elif(fcc.checkCardTwo(arrCard[0]) > 0):
                     arrBin[7 + fcc.checkCardTwo(arrCard[0])] = 1
            elif typeArrCard == function.TYPE_PAIR or typeArrCard == function.TYPE_PAIR_2:
                arrBin[12] = 1
                for iCard in arrCard:
                    if(fcc.checkCardA(iCard) > 0):
                        arrBin[3 + fcc.checkCardA(iCard)] = 1
                    elif(fcc.checkCardTwo(arrCard[0]) > 0):
                        arrBin[7 + fcc.checkCardTwo(iCard)] = 1
            elif typeArrCard == function.TYPE_THREE_OF_KIND:
                arrBin[13] = 1
                for iCard in arrCard:
                    if(fcc.checkCardA(iCard) > 0):
                        arrBin[3 + fcc.checkCardA(iCard)] = 1
                    elif(fcc.checkCardTwo(arrCard[0]) > 0):
                        arrBin[7 + fcc.checkCardTwo(iCard)] = 1
            elif typeArrCard == function.TYPE_FOUR_OF_KIND:
                arrBin[14] = 1
                for iCard in arrCard:
                    if(fcc.checkCardA(iCard) > 0):
                        arrBin[3 + fcc.checkCardA(iCard)] = 1
                    elif(fcc.checkCardTwo(arrCard[0]) > 0):
                        arrBin[7 + fcc.checkCardTwo(iCard)] = 1
            elif typeArrCard == function.TYPE_TWO_FAIR_STRAIGHT:
                arrBin[15] = 1
                for iCard in arrCard:
                    if(fcc.checkCardA(iCard) > 0):
                        arrBin[3 + fcc.checkCardA(iCard)] = 1
            elif typeArrCard == function.TYPE_THREE_FAIR_STRAIGHT:
                arrBin[16] = 1
                for iCard in arrCard:
                    if(fcc.checkCardA(iCard) > 0):
                        arrBin[3 + fcc.checkCardA(iCard)] = 1
            elif typeArrCard == function.TYPE_FOUR_FAIR_STRAIGHT:
                arrBin[17] = 1
                for iCard in arrCard:
                    if(fcc.checkCardA(iCard) > 0):
                        arrBin[3 + fcc.checkCardA(iCard)] = 1
            elif typeArrCard > function.TYPE_STRAIGHT_FLUSH * 100:
                lengthStraight = typeArrCard % (function.TYPE_STRAIGHT_FLUSH * 100)
                arrBin[27 + lengthStraight - 3] = 1
                if(fcc.checkCardA(arrCard[lengthStraight - 1])>0):
                    arrBin[3 + fcc.checkCardA(arrCard[lengthStraight - 1])] = 1
            elif typeArrCard > function.TYPE_STRAIGHT_NORMAL * 100:
                lengthStraight = typeArrCard % (function.TYPE_STRAIGHT_NORMAL * 100)
                arrBin[18 + lengthStraight - 3] = 1
                if(fcc.checkCardA(arrCard[lengthStraight - 1])>0):
                    arrBin[3 + fcc.checkCardA(arrCard[lengthStraight - 1])] = 1
        
        result.append(arrBin)
    while(len(result) < 3):
        arrBin = np.zeros((36), np.int_)
        result.append(arrBin)
    result = np.array(result)
    result = result.reshape((108))
    return result

def createInfoArrayDisCard(listPlayer):
    arrCardId = []
    for player in listPlayer:
        for arr in player.currentPlayed:
            for iCard in arr:
                arrCardId.append(iCard)
    result = function.convertCardOnHandToBinary52(arrCardId)
    return result

def createInput(listPlayer, indexCurrentPlayer, cardPrevHand, disCardThreeSpider):
    result = []
    a = createInfoCurrentCard(listPlayer[indexCurrentPlayer])
    b = createInfoOtherPlayers(listPlayer, indexCurrentPlayer)
    c = createInfoArrayDisCard(listPlayer)
    d = function.convertCardOnHandToBinary52(cardPrevHand)
    e = []
    if(disCardThreeSpider):
        e = [1]
    else:
        e = [0]
    a = np.ndarray.tolist(a)
    b = np.ndarray.tolist(b)
    c = np.ndarray.tolist(c)
    d = np.ndarray.tolist(d)
    result += a
    result += b
    result += c
    result += d
    result += e
    result = np.array(result)
    return result