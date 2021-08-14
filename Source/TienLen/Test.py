from os import sep
from vo.Player import Player
from utils.Util import Util
import numpy as np
from logic.TienLenGame import TienLenGame
import time, random
from logic.Function import Function
from logic.ActionSpace import ActionSpace
import logic.FunctionCheckCard as fcc
import logic.FunctionCreaateInput as fci

env = TienLenGame()

actionSpaceObject = ActionSpace()
actionSpaceObject.loadActionSpace()

functionObject = Function()

# deck = np.random.permutation(52) + 1

# myCards = np.array(deck[0:13])
myCards = np.array([37, 36, 32, 11, 16, 30, 23, 38, 27, 41, 49, 26, 44])
# myCards = np.array([37, 36, 32, 11, 16, 30])
print("start")

def testCheckGroupCard():
    file = open("doithongs.txt", "r")
    strArr = file.readline()
    count2thong = 0
    count3thong = 0
    count4thong = 0
    while strArr != "":
        arr = np.fromstring(strArr, dtype= np.int_, sep = ",")
        re = functionObject.getTypeArrCard(arr)
        if re == functionObject.TYPE_TWO_FAIR_STRAIGHT:
            count2thong += 1
        elif re == functionObject.TYPE_THREE_FAIR_STRAIGHT:
            count3thong += 1
        elif re== functionObject.TYPE_FOUR_FAIR_STRAIGHT:
            count4thong += 1
        else:
            print(re)
            print("Function error!")
            print(arr)
            break
        strArr = file.readline()
    file.close()
    print("{} {} {}".format(count2thong,count3thong,count4thong))

def testOptimize():
    arrays = functionObject.util.generateArrayBinary(13)
    print(len(arrays))

def testEnv():
    env = TienLenGame()
    env.resetGame()
    while not env.gameOver:
        env.getIndexNext()
        action = env.getAction()
        env.step(action)

def testCheckCardInGroup(myCardsP):
    print("start")
    start = time.time()
    for iCard in myCardsP:
        if(fcc.checkCardA(iCard)>0):
            print("{} is type of A".format(functionObject.printCard(iCard)))
        if(fcc.checkCardTwo(iCard)>0):
            print("{} is type of 2".format(functionObject.printCard(iCard)))
        if(fcc.checkInPair(iCard,myCardsP)):
            print("{} is type of pair".format(functionObject.printCard(iCard)))
        if(fcc.checkInThreeOfKind(iCard, myCardsP)):
            print("{} is type of three of kind".format(functionObject.printCard(iCard)))
        if(fcc.checkInFourOfKind(iCard, myCardsP)):
            print("{} is type of four of kind".format(functionObject.printCard(iCard)))
        if(fcc.checkInTwoPairStraight(iCard, myCardsP)):
            print("{} is type of two pair straight".format(functionObject.printCard(iCard)))
        if(fcc.checkInThreePairStraight(iCard, myCardsP)):
            print("{} is type of three pair straight".format(functionObject.printCard(iCard)))
        if(fcc.checkInFourPariStraight(iCard, myCardsP)):
            print("{} is type of four pair straight".format(functionObject.printCard(iCard)))
        lenghtStraight = fcc.checkInStraight(iCard, myCardsP)
        if(lenghtStraight >= 3):
            print("{} is type of straight with maxLenght = {}".format(functionObject.printCard(iCard),lenghtStraight))
        lenghtStraight = fcc.checkInStraightFlush(iCard, myCardsP)
        if(lenghtStraight >= 3):
            print("{} is type of straight flush with maxLenght = {}".format(functionObject.printCard(iCard),lenghtStraight))
        print("==============================================================")
    end = time.time()
    print("Finish in {} seconds!".format((end - start)//1))

def testCreateInput():
    cp1 = [
        [3,4,5],
        [6,19],
        [18,31,32,45],
        [12,25,13,26]
    ]
    cp2 = [
        [8,21,34],
        [9,23,37],
        [18,31,32,45,20,33],
        [24,37,12,25,13,26]
    ]
    cp3 = [
        [12,25,38,51],
        [18,31,32,45,20,33,8,21],
        [13],
        [27],
        [10,49,24,37,12,25,13,26]
    ]
    ps1=[3,5,7,9]
    ps2=[3,5,7,9,10]
    ps3=[3,5,7,9,11,12]
    listPlayer = []
    for i in range(4):
        if(i == 0):
            listPlayer.append(Player(i,[],[]))
        elif i == 1:
            listPlayer.append(Player(i,ps1, cp1))
        elif i == 2:
            listPlayer.append(Player(i,ps2, cp2))
        elif i == 3:
            listPlayer.append(Player(i,ps3, cp3))
    ar = fci.createInput(listPlayer, 1, [], True)
    print(ar)

def testFunctionConvertAction():
    print(functionObject.compareTwoArrayCard(np.array([2,15,3,16,4,17,5,18]),np.array([28,41,29,42,30,43,31,44])))
    print(functionObject.getTypeArrCard(np.array([28,41,29,42,30,43,31,44])))

def testCheckFastWin():
    arrCard = [4,17,5,18,6,19,7,20]
    print(fcc.arrCardHasFourPairStraight(arrCard))

def testCompareFunction():
    count = 0
    for i in range(len(actionSpaceObject.actions)):
        action = actionSpaceObject.actions[i]
        arrCard = functionObject.convertActionToArrCard(action, myCards)
        if(functionObject.compareTwoArrayCard(np.array([2,16,17]),arrCard)):
            print(action)
            print(arrCard)
            count += 1
    print(count)

action_ex = 0
env.step(action_ex)