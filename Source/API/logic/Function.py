# input and output all function array is instance of numpy
import numpy as np
from numpy.core.records import array
from .Util import Util
from .Card import Card
class Function:
    util = None
    
    TYPE_EMPTY = -1
    TYPE_ONE = 0
    TYPE_PAIR = 1
    TYPE_THREE_OF_KIND = 2
    TYPE_FOUR_OF_KIND = 3
    TYPE_TWO_FAIR_STRAIGHT = 4
    TYPE_THREE_FAIR_STRAIGHT = 5
    TYPE_FOUR_FAIR_STRAIGHT = 6
    TYPE_STRAIGHT_NORMAL = 7
    TYPE_STRAIGHT_FLUSH = 8
    TYPE_ONE_2 = 9
    TYPE_PAIR_2 = 10
    TYPE_ONE_2_BLACK = 11
    TYPE_ONE_2_RED = 12
    TYPE_PAIR_2_BLACK = 13
    TYPE_PAIR_2_RED = 14
    TYPE_NONE = -2

    def __init__(self):
        self.util = Util()
        pass
    
    # input: carids, output: array binary size 13
    def convertCardOnHandToBinary13(self, arrCard):
        arrBin = np.zeros(13)
        for i in range(len(arrCard)):
            arrBin[i] = 1
        return np.array(arrBin, dtype=np.int_)

    # input: arrayAction: array binary size 13, arrCardOnHand: cardIds
    # output: boolean
    def checkSuitableCardOnHand(self, arrayAction, arrCardOnHand):
        arrCardBin = self.convertCardOnHandToBinary13(arrCardOnHand)
        checkArrAction = int(self.util.convert_array_toString(arrayAction), base= 2)
        checkCardOnHand = int(self.util.convert_array_toString(arrCardBin), base= 2)
        # print(arrayAction)
        # print(arrCardBin)
        # print("===================")
        return checkArrAction == checkArrAction & checkCardOnHand
    
    # input: cardId
    # output: number of card
    def getNumCardByCardId(self, cardId):
        return (cardId - 1) % 13 + 2
    
    # input: cardId
    # output: suit of card
    def getSuitCardByCardId(self, cardId):
        return (cardId - 1) // 13 + 1

    # input: cardIds
    # output: boolean
    # describe: check card is two card
    def isOneTwo(self, arrCard):
        if(len(arrCard) == 1):
            if(self.getNumCardByCardId(arrCard[0]) == 2):
                return True
            else:
                return False
        else:
            return False

    def isOneTwoBlack(self, arrCard):
        if(self.isOneTwo(arrCard)):
            suitCard = self.getSuitCardByCardId(arrCard[0])
            if(suitCard <= 2):
                return True
        return False

    def isOneTwoRed(self, arrCard):
        if(self.isOneTwo(arrCard)):
            suitCard = self.getSuitCardByCardId(arrCard[0])
            if(suitCard > 2):
                return True
        return False
    # input: cardIds
    # output: boolean
    # describe: check cards is pair
    def isPair(self, arrCard):
        if(len(arrCard) == 2):
            return (self.getNumCardByCardId(arrCard[0]) == self.getNumCardByCardId(arrCard[1])) and (self.getSuitCardByCardId(arrCard[0]) != self.getSuitCardByCardId(arrCard[1]))
        else:
            return False

    # input: cardIds
    # output: boolean
    # describe: check cards is two pair
    def isPairTwo(self, arrCard):
        if(self.isPair(arrCard)):
            if(self.getNumCardByCardId(arrCard[0]) == 2):
                return True
            else:
                return False
        else:
            return False

    def isPairTwoBlack(self, arrCard):
        if(self.isPairTwo(arrCard)):
            suitCard1 = self.getSuitCardByCardId(arrCard[0])
            suitCard2 = self.getSuitCardByCardId(arrCard[1])
            if(suitCard1 <= 2 and suitCard2 <=2):
                return True
        return False

    def isPairTwoRed(self, arrCard):
        if(self.isPairTwo(arrCard)):
            suitCard1 = self.getSuitCardByCardId(arrCard[0])
            suitCard2 = self.getSuitCardByCardId(arrCard[1])
            if(suitCard1 > 2 and suitCard2 > 2):
                return True
        return False

    # input: cardIds
    # output: boolean
    # describe: check cards is three of kind
    def isThreeOfKind(self, arrCard):
        if(len(arrCard) == 3):
            numCard = self.getNumCardByCardId(arrCard[0])
            arrS = [1,2,3,4]
            for idCard in arrCard:
                if numCard != self.getNumCardByCardId(idCard):
                    return False
                if self.getSuitCardByCardId(idCard) in arrS:
                    arrS.remove(self.getSuitCardByCardId(idCard))
                else:
                    return False
            return True
        else:
            return False

    # input: cardIds
    # output: boolean
    # describe: check cards is four of kind
    def isFourOfKind(self, arrCard):
        if(len(arrCard) == 4):
            numCard = self.getNumCardByCardId(arrCard[0])
            arrS = [1,2,3,4]
            for idCard in arrCard:
                if numCard != self.getNumCardByCardId(idCard):
                    return False
                if self.getSuitCardByCardId(idCard) in arrS:
                    arrS.remove(self.getSuitCardByCardId(idCard))
                else:
                    return False
            return True
        else:
            return False

    # input: cardIds
    # output: boolean
    # describe: check cards is straight size >=3
    def isStraight(self, arrCard):
        if(len(arrCard) >= 3):
            arrN = []
            for iCard in arrCard:
                arrN.append(self.getNumCardByCardId(iCard))
            arrN.sort()
            if(arrN[0] > 2):
                for i in range(len(arrN)):
                    if(i != 0):
                        if(arrN[i] - arrN[i - 1] != 1):
                            return False
                return True
            else:
                return False
        else:
            return False

    # input: cardIds
    # output: boolean
    # describe: check cards is straight same suit size >=3
    def isStraightFlush(self, arrCard):
        if(self.isStraight(arrCard)):
            suit = self.getSuitCardByCardId(arrCard[0])
            for iCard in arrCard:
                if(self.getSuitCardByCardId(iCard) != suit):
                    return False
            return True
        else:
            return False

    # input: cardIds
    # output: boolean
    # describe: check cards is two pair straight
    def isTwoPairStraight(self, arrCardOrign):
        if(len(arrCardOrign) == 4):
            arrCard = self.sortCard(arrCardOrign)
            arrN = []
            arrS = []
            for iCard in arrCard:
                arrN.append(self.getNumCardByCardId(iCard))
                arrS.append(self.getSuitCardByCardId(iCard))
            if arrN[0] > 2:
                if((arrN[0] == arrN[1]) and (arrS[0] != arrS[1])):
                    if((arrN[2] == arrN[3]) and (arrS[2] != arrS[3])):
                        if(arrN[1] + 1 == arrN[2]):
                            return True
            return False
        else:
            return False

    # input: cardIds
    # output: boolean
    # describe: check cards is three pair straight
    def isThreePairStraight(self, arrCardOrign):
        if(len(arrCardOrign) == 6):
            arrCard = self.sortCard(arrCardOrign)
            arrN = []
            arrS = []
            for iCard in arrCard:
                arrN.append(self.getNumCardByCardId(iCard))
                arrS.append(self.getSuitCardByCardId(iCard))
            if(arrN[0] > 2):
                if((arrN[0] == arrN[1]) and (arrS[0] != arrS[1])):
                    if((arrN[2] == arrN[3]) and (arrS[2] != arrS[3])):
                        if((arrN[4] == arrN[5]) and (arrS[4] != arrS[5])):
                            if(arrN[1] + 1 == arrN[2]):
                                if(arrN[3] + 1 == arrN[4]):
                                    return True
            return False
        else:
            return False

    # input: cardIds
    # output: boolean
    # describe: check cards is four pair straight
    def isFourPairStraight(self, arrCardOrign):
        if(len(arrCardOrign) == 8):
            arrCard = self.sortCard(arrCardOrign)
            arrN = []
            arrS = []
            for iCard in arrCard:
                arrN.append(self.getNumCardByCardId(iCard))
                arrS.append(self.getSuitCardByCardId(iCard))
            if(arrN[0] > 2):
                if((arrN[0] == arrN[1]) and (arrS[0] != arrS[1])):
                    if((arrN[2] == arrN[3]) and (arrS[2] != arrS[3])):
                        if((arrN[4] == arrN[5]) and (arrS[4] != arrS[5])):
                            if((arrN[6] == arrN[7]) and (arrS[6] != arrS[7])):
                                if(arrN[1] + 1 == arrN[2]):
                                    if(arrN[3] + 1 == arrN[4]):
                                        if(arrN[5] + 1 == arrN[6]):
                                            return True
            return False
        else:
            return False

    # input: cardIds
    # output: array binary size 52
    def convertCardOnHandToBinary52(self,arrCard):
        arrBin = np.zeros((52))
        for idCard in arrCard:
            arrBin[idCard - 1] = 1
        return np.array(arrBin, dtype= np.int_)

    # input: object of Card
    # output: int = numberCard * 10 + suitCard
    def customSort(self,card):
            return card.getN() * 10 + card.getS()
        #Sắp xếp bộ bài theo tứ tự từ nhỏ tới lơn (numCard, suitCard)
        #Tức sắp xếp bộ bài từ 2 -> A, từ Bích, Tép, Rô, Cơ
    
    # input: cardIds
    # output: cardIds is sorted by numberCard and suitCard
    def sortCard(self,arrCard):
        cards = []
        for iCard in arrCard:
            cards.append(Card(id= iCard))
        cards.sort(key= self.customSort)
        result = []
        for card in cards:
            result.append(card.getId())
        return np.array(result, dtype= np.int_)
    
    # input: arrAction: array binary size 13, arrCard: cardIds
    # output: if arrayAction isn't suittable with arrCard return None, otherwise return cardIds
    def convertActionToArrCard(self, arrayAction, arrCard):
        if(len(arrayAction) == 0):
            print("Nguoi choi khong chon bai")
        if(self.checkSuitableCardOnHand(arrayAction, arrCard)):
            arrCardAction = []
            arrIdCardSort = self.sortCard(arrCard)
            for index in range(len(arrayAction)):
                if(arrayAction[index] == 1):
                    arrCardAction.append(arrIdCardSort[index])
            strCard = ""
            for idCard in arrCardAction:
                strCard += self.printCard(idCard)+", "
            # print(strCard)
            return np.array(arrCardAction, dtype= np.int_)
        else:
            return None

    # input: cardIds
    # output: int
    # describe: get type of group card
    def getTypeArrCard(self, arrCard):
        if(len(arrCard) >= 1):
            if(self.isOneTwo(arrCard)):
                return self.TYPE_ONE_2
            if(len(arrCard) == 1):
                return self.TYPE_ONE
            if(self.isPairTwo(arrCard)):
                return self.TYPE_PAIR_2
            if(self.isPair(arrCard)):
                return self.TYPE_PAIR
            if(self.isThreeOfKind(arrCard)):
                return self.TYPE_THREE_OF_KIND
            if(self.isFourOfKind(arrCard)):
                return self.TYPE_FOUR_OF_KIND
            if(self.isTwoPairStraight(arrCard)):
                return self.TYPE_TWO_FAIR_STRAIGHT
            if(self.isStraightFlush(arrCard)):
                return self.TYPE_STRAIGHT_FLUSH * 100 + len(arrCard)
            if(self.isStraight(arrCard)):
                return self.TYPE_STRAIGHT_NORMAL * 100 + len(arrCard)
            if(self.isThreePairStraight(arrCard)):
                return self.TYPE_THREE_FAIR_STRAIGHT
            if(self.isFourPairStraight(arrCard)):
                return self.TYPE_FOUR_FAIR_STRAIGHT
            return self.TYPE_NONE
        else:
            return self.TYPE_EMPTY

    # Chi tiet type
    def getTypeDetailArrCard(self, arrCard):
        if(len(arrCard) >= 1):
            if(self.isOneTwoBlack(arrCard)):
                return self.TYPE_ONE_2_BLACK
            if(self.isOneTwoRed(arrCard)):
                return self.TYPE_ONE_2_RED
            if(self.isOneTwo(arrCard)):
                return self.TYPE_ONE_2
            if(len(arrCard) == 1):
                return self.TYPE_ONE
            if(self.isPairTwoBlack(arrCard)):
                return self.TYPE_PAIR_2_BLACK
            if(self.isPairTwoRed(arrCard)):
                return self.TYPE_PAIR_2_RED
            if(self.isPairTwo(arrCard)):
                return self.TYPE_PAIR_2
            if(self.isPair(arrCard)):
                return self.TYPE_PAIR
            if(self.isThreeOfKind(arrCard)):
                return self.TYPE_THREE_OF_KIND
            if(self.isFourOfKind(arrCard)):
                return self.TYPE_FOUR_OF_KIND
            if(self.isTwoPairStraight(arrCard)):
                return self.TYPE_TWO_FAIR_STRAIGHT
            if(self.isStraightFlush(arrCard)):
                return self.TYPE_STRAIGHT_FLUSH * 100 + len(arrCard)
            if(self.isStraight(arrCard)):
                return self.TYPE_STRAIGHT_NORMAL * 100 + len(arrCard)
            if(self.isThreePairStraight(arrCard)):
                return self.TYPE_THREE_FAIR_STRAIGHT
            if(self.isFourPairStraight(arrCard)):
                return self.TYPE_FOUR_FAIR_STRAIGHT
            return self.TYPE_NONE
        else:
            return self.TYPE_EMPTY

    # Khong chặn được trả về false và chặn được trả về true
    # input: arrCardPrevOrigin: cardIds of previous player, arrCardCalOrigin: cardIds prepare discards
    # output: boolean
    def compareTwoArrayCard(self, arrCardPrevOrigin, arrCardCalOrigin):
        arrCardPrev = self.sortCard(arrCardPrevOrigin)
        arrCardCal = self.sortCard(arrCardCalOrigin)
        typeArrCardPrev = self.getTypeArrCard(arrCardPrev)
        typeArrCardCal = self.getTypeArrCard(arrCardCal)
        lenCardPrev = len(arrCardPrev)
        lenCardCal = len(arrCardCal)
        if(typeArrCardCal == self.TYPE_NONE):
            return False
        if (typeArrCardCal == self.TYPE_EMPTY):
            return True
        if(typeArrCardPrev == typeArrCardCal):
            #2 bo cung loai
            # cung 1 la, cung 2 la
            if(   typeArrCardPrev == self.TYPE_ONE 
                 or typeArrCardPrev == self.TYPE_PAIR
                 or typeArrCardPrev == self.TYPE_ONE_2
                 or typeArrCardPrev == self.TYPE_PAIR_2):
                numCardPrev = self.getNumCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                numCardCal = self.getNumCardByCardId(arrCardCal[len(arrCardCal) - 1])
                if(numCardCal == numCardPrev):
                    if(numCardPrev > 2 and numCardPrev < 6):
                        return True
                    else:
                        suitCardPrev = self.getSuitCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                        suitCardCal = self.getSuitCardByCardId(arrCardCal[len(arrCardCal) - 1])
                        return suitCardCal > suitCardPrev
                else:
                    return numCardCal > numCardPrev
            # cung 3 xam , cung tu quy
            if(   typeArrCardPrev == self.TYPE_THREE_OF_KIND 
                 or typeArrCardPrev == self.TYPE_FOUR_OF_KIND):
                numCardPrev = self.getNumCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                numCardCal = self.getNumCardByCardId(arrCardCal[len(arrCardCal) - 1])
                if(numCardPrev == 2):
                     return False
                elif(numCardCal == 2):
                    return True
                else:
                    return numCardCal > numCardPrev
            # cung 3 doi thong, cung 4 doi thon
            if(   typeArrCardPrev == self.TYPE_THREE_FAIR_STRAIGHT 
                 or typeArrCardPrev == self.TYPE_FOUR_FAIR_STRAIGHT):
                numCardPrev = self.getNumCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                numCardCal = self.getNumCardByCardId(arrCardCal[len(arrCardCal) - 1])
                if(numCardCal == numCardPrev):
                    if(numCardPrev == 5):
                        return True
                    else:
                        suitCardPrev = self.getSuitCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                        suitCardCal = self.getSuitCardByCardId(arrCardCal[len(arrCardCal) - 1])
                        return suitCardCal > suitCardPrev
                else:
                    return numCardCal > numCardPrev
            # cung 2 doi thong
            if(   typeArrCardPrev == self.TYPE_TWO_FAIR_STRAIGHT):
                numCardPrev = self.getNumCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                numCardCal = self.getNumCardByCardId(arrCardCal[len(arrCardCal) - 1])
                if(numCardCal == numCardPrev):
                    if(numCardPrev == 4 or numCardPrev == 5):
                        return True
                    else:
                        suitCardPrev = self.getSuitCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                        suitCardCal = self.getSuitCardByCardId(arrCardCal[len(arrCardCal) - 1])
                        return suitCardCal > suitCardPrev
                else:
                    return numCardCal > numCardPrev
            # cung sanh thuong, cung sanh dong mau
            if(   typeArrCardPrev == self.TYPE_STRAIGHT_NORMAL * 100 + lenCardPrev
                 or typeArrCardPrev == self.TYPE_STRAIGHT_FLUSH * 100 + lenCardPrev):
                numCardPrev = self.getNumCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                numCardCal = self.getNumCardByCardId(arrCardCal[len(arrCardCal) - 1])
                if(numCardCal == numCardPrev):
                    if(lenCardPrev == 3 and numCardPrev == 5):
                        return True
                    else:
                        suitCardPrev = self.getSuitCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                        suitCardCal = self.getSuitCardByCardId(arrCardCal[len(arrCardCal) - 1])
                        return suitCardCal > suitCardPrev
                else:
                    return numCardCal > numCardPrev
            pass
        else:
            #2 bo khac loai
            # trong bo don 2 la to nhat
            if(typeArrCardPrev == self.TYPE_ONE and typeArrCardCal == self.TYPE_ONE_2):
                return True
            # trong bo doi doi 2 la to nhat
            if(typeArrCardPrev == self.TYPE_PAIR and typeArrCardCal == self.TYPE_PAIR_2):
                return True
            # sanh dong chat chan sanh thuong theo luat sanh thuong
            if(   typeArrCardPrev == self.TYPE_STRAIGHT_NORMAL * 100 + lenCardPrev
                and typeArrCardCal == self.TYPE_STRAIGHT_FLUSH * 100 + lenCardCal):
                numCardPrev = self.getNumCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                numCardCal = self.getNumCardByCardId(arrCardCal[len(arrCardCal) - 1])
                if(lenCardCal == lenCardPrev):
                    if(numCardCal == numCardPrev):
                        if(lenCardPrev == 3 and numCardPrev == 5):
                            return True
                        else:
                            suitCardPrev = self.getSuitCardByCardId(arrCardPrev[len(arrCardPrev) - 1])
                            suitCardCal = self.getSuitCardByCardId(arrCardCal[len(arrCardCal) - 1])
                            return suitCardCal > suitCardPrev
                    else:
                        return numCardCal > numCardPrev
            # 3 doi thong, tu quy, 4 doi thong  chan don 2
            if( typeArrCardPrev == self.TYPE_ONE_2 and
                (typeArrCardCal == self.TYPE_THREE_FAIR_STRAIGHT  or
                 typeArrCardCal == self.TYPE_FOUR_FAIR_STRAIGHT  or
                 typeArrCardCal == self.TYPE_FOUR_OF_KIND) ):
                return True
            # Tu quy, 4 doi thong chan doi 2
            if( typeArrCardPrev == self.TYPE_PAIR_2 and (
                typeArrCardCal == self.TYPE_FOUR_OF_KIND  or
                typeArrCardCal == self.TYPE_FOUR_FAIR_STRAIGHT )):
                return True
            # Tu quy, 4 doi thong chan 3 doi thong
            if( typeArrCardPrev == self.TYPE_THREE_FAIR_STRAIGHT and (
                typeArrCardCal == self.TYPE_FOUR_OF_KIND  or
                typeArrCardCal == self.TYPE_FOUR_FAIR_STRAIGHT )):
                return True
            # 4 doi thong chan tu quy
            if( typeArrCardPrev == self.TYPE_FOUR_OF_KIND and typeArrCardCal == self.TYPE_FOUR_FAIR_STRAIGHT):
                return True
            pass
        return False

    # input: arrCard: cardIds, isFisrtPlayer: Player is first playing, isn't player
    # output: boolean
    # describe: if cards is one of type group return true otherwise return false        
    def acceptDiscards(self, arrCard, isPlayThreeSpider):
        typeGroup = self.getTypeArrCard(arrCard)
        if(typeGroup != self.TYPE_NONE and typeGroup != self.TYPE_EMPTY):
            if isPlayThreeSpider:
                cardIdThreeSpider = 2
                for cardI in arrCard:
                    if(cardI == cardIdThreeSpider):
                        return True
                return False
            else:
                return True
        else: 
            return False
    
    def printCard(self, idCard):
        numCard = self.getNumCardByCardId(idCard)
        suitCard = self.getSuitCardByCardId(idCard)
        if(numCard == 11):
            numCard = "J"
        elif (numCard == 12):
            numCard = "Q"
        elif (numCard == 13):
            numCard = "K"
        elif numCard == 14:
            numCard = "A"
        
        if suitCard == 1:
            suitCard = "Bich"
        elif suitCard == 2:
            suitCard = "Tep"
        elif suitCard == 3:
            suitCard = "Ro"
        elif suitCard == 4:
            suitCard = "Co"
        
        return "{} {}".format(numCard, suitCard)

    def convertUnSignIntegerToArrayBinary(self, number, sizeBin):
        arr = []
        number = number // 1
        if(number < 0):
            number *= (-1)
        while(number > 1):
            arr.append(number%2)
            number = number // 2
        arr.append(number)
        while(len(arr) < sizeBin):
            arr.append(0)
        arr.reverse()
        return np.array(arr)