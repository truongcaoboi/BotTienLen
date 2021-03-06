from vo.Card import Card
from vo.Player import Player
import logic.FunctionCreaateInput as fci
from logic.Function import Function
import logic.Constants as cons
import logic.FunctionCheckCard as fcc
import numpy as np
import random, time
import math
from multiprocessing import Process, Pipe
from gym import spaces, Env

class TienLenGame(Env):
    num_envs = 4
    actions = []
    indexCurrentPlayer = 0
    indexStartRound = 0
    lastGroup = []
    listPlayer = []
    lastWinner = -1
    gameOver = False
    round = 0
    numGame = 0
    countActionFail = 0
    countHasCardNotDiscard = 0
    desk = []
    numPlayerFold = 0
    isGetIndex = False
    inputNetwork = []
    isMustPlayThreeSpider = False
    countBitInput = 0
    func = Function()
    rewards = np.zeros((4))
    totalMarkInRound = 0
    rewardStep = 0
    historyNotDiscard = []
    historyNotDisCardInRound = []
    notMatchCard = False


    def __init__(self, action):
        self.actions = action
        # self.reset()
    def convertAvailableActions(self,availAcs):
        #convert from (1,0,0,1,1...) to (0, -math.inf, -math.inf, 0,0...) etc
        availAcs[np.nonzero(availAcs==0)] = 0.000001
        availAcs[np.nonzero(availAcs==1)] = 1
        return availAcs
    def reset(self):
        print("reset game")
        self.isMustPlayThreeSpider = False
        self.historyNotDiscard = []
        self.desk = np.random.permutation(52) + 1
        cardsForPlayer = []
        cardsForPlayer.append(self.desk[: 13])
        cardsForPlayer.append(self.desk[13: 26])
        cardsForPlayer.append(self.desk[26: 39])
        cardsForPlayer.append(self.desk[39:])
        self.listPlayer = []
        self.listPlayer.append(Player(index= 0, idCards=cardsForPlayer[0], currentPlayed=[]))
        self.listPlayer.append(Player(index= 1, idCards=cardsForPlayer[1], currentPlayed=[]))
        self.listPlayer.append(Player(index= 2, idCards=cardsForPlayer[2], currentPlayed=[]))
        self.listPlayer.append(Player(index= 3, idCards=cardsForPlayer[3], currentPlayed=[]))

        # print(self.listPlayer[0].idCards)

        if(self.checkFastWin()):
            self.lastWinner = -1
            return self.reset()

        self.indexCurrentPlayer = self.lastWinner
        for i in range(4):
            for iCard in self.listPlayer[i].idCards:
                if(iCard == 2):
                    if(self.lastWinner == -1):
                        self.isMustPlayThreeSpider = True
                        self.indexCurrentPlayer = self.listPlayer[i].index
                        break
        self.round = 0
        self.numGame += 1
        self.countActionFail = 0
        self.countHasCardNotDiscard = 0
        self.gameOver = False
        self.isGetIndex = True
        self.resetRound()

        self.updateInputNetwork()
        return np.array(self.inputNetwork[self.indexCurrentPlayer])

    # ??i???u ki???n win nhanh: t??? 2, s???nh r???ng, 6 ????i, 4 x??m, 5 ????i th??ng, n???u l?? v??n kh???i ?????ng c?? b??? ch???a 3 b??ch ch???n 2
    def checkFastWin(self):
        for i in range(4):
            if(fcc.checkFastWin(self.listPlayer[i].idCards, self.lastWinner == -1) > 0):
                return True
        return False

    def resetRound(self):
        # print("reset round")
        self.indexStartRound = self.indexCurrentPlayer
        self.round += 1
        for player in self.listPlayer:
            player.isInRound = True
        self.numPlayerFold = 0
        self.totalMarkInRound = 0
        if(len(self.historyNotDisCardInRound) > 0):
            self.historyNotDiscard = self.historyNotDisCardInRound + self.historyNotDiscard
        self.historyNotDisCardInRound = []
        self.lastGroup = []

    
    def getIndexNext(self):
        if(self.isGetIndex):
            return
        indexNext = self.indexCurrentPlayer + 1
        if(indexNext == 4):
            indexNext = 0
        lps = self.listPlayer[indexNext:]
        lps += self.listPlayer[:indexNext]
        # for player in lps:
        #     print("player index {} has isInRound: {}".format(player.index, player.isInRound))
        for player in lps:
            if(player.isInRound):
                self.indexCurrentPlayer = player.index
                break
        if(self.numPlayerFold == 3):
            self.resetRound()

    def updateGame(self, action):
        # print(self.actions[action])
        self.notMatchCard = False
        typePrevHand = self.func.getTypeArrCard(self.lastGroup)
        typeCurrHand = self.func.TYPE_NONE
        player = self.listPlayer[self.indexCurrentPlayer]
        arrCard = self.func.convertActionToArrCard(self.actions[action], player.idCards)
        if(arrCard is not None):
            flag = False
            if(len(self.lastGroup) == 0):
                flag = self.func.acceptDiscards(arrCard, self.isMustPlayThreeSpider)
            else:
                flag = self.func.compareTwoArrayCard(self.lastGroup, arrCard)
            if(flag):
                typeCurrHand = self.func.getTypeArrCard(arrCard)
                if(len(arrCard) > 0):
                    playerCards = np.ndarray.tolist(player.idCards)
                    for iCard in arrCard:
                        playerCards.remove(iCard)
                    player.idCards = np.array(playerCards, dtype= np.int)
                    playerDiscard = player.currentPlayed.copy()
                    playerDiscard.append(np.array(arrCard, dtype= np.int))
                    player.currentPlayed = playerDiscard
                    if(len(player.idCards) == 0):
                        self.gameOver = True
                    self.lastGroup = arrCard
                else:
                    if(len(arrCard) == 0 and player.numberActionAvailable > 1):
                        self.historyNotDisCardInRound.append(player.index)
                        self.countHasCardNotDiscard += 1
                    self.executeNotDiscard(player)
            else:
                self.notMatchCard = True
        else:
            self.notMatchCard = True
        self.calReward(typePrevHand=typePrevHand, typeActionHand= typeCurrHand)
        strCard = "empty"
        if(arrCard is not None):
            strCard = ""
            for id in arrCard:
                strCard += self.func.printCard(id) + ", "
        if(self.notMatchCard):
            # print("player {} chon sai action r - arrCard: {}".format(self.indexCurrentPlayer, strCard))
            self.countActionFail += 1
            self.notMatchCard = False
            # input()
            return
        # print("player {} Chon dung action roi nhe! - {}".format(self.indexCurrentPlayer, strCard))
        # input()
        self.isGetIndex = False
        self.isMustPlayThreeSpider = False
        self.getIndexNext()
        self.updateInputNetwork()
    
    def executeNotDiscard(self, player):
        player.isInRound = False
        self.numPlayerFold += 1
        pass

    def calReward(self, typePrevHand, typeActionHand):
        if(self.notMatchCard):
            self.rewardStep = -50
            return
        self.rewards = np.zeros((len(self.listPlayer)))
        self.rewardStep = self.calRewardStep(typePrevHand, typeActionHand)
        winnerMark = 0
        if(self.gameOver):
            for index in range(len(self.listPlayer)):
                if(index != self.lastWinner):
                    player = self.listPlayer[index]
                    mark = self.calRewardForPlayer(player)
                    winnerMark += mark
                    self.rewards[index] = (-1) * mark
            self.rewards[self.lastWinner] = winnerMark + self.rewardStep + 100
            indexPayForAll = self.getPayForAllPlayer()
            if(indexPayForAll >= 0):
                self.rewards[indexPayForAll] = (-1) * winnerMark

    #Con cap nhat them
    #Hien tai chi cong khi dc an bo do
    def calRewardStep(self, typePreHand, typeActionHand):
        rew = 0
        if(typeActionHand < 0 or self.notMatchCard):
            return rew
        if(typePreHand == self.func.TYPE_ONE_2_BLACK):
            rew = cons.MARK_FOR_ONE_CARD_TWO_BLACK
        elif (typePreHand == self.func.TYPE_ONE_2_RED):
            rew = cons.MARK_FOR_ONE_CARD_TWO_RED
        elif (typePreHand == self.func.TYPE_PAIR_2_BLACK):
            rew = cons.MARK_FOR_ONE_CARD_TWO_BLACK * 2
        elif (typePreHand == self.func.TYPE_PAIR_2_RED):
            rew = cons.MARK_FOR_ONE_CARD_TWO_RED * 2
        elif (typePreHand == self.func.TYPE_PAIR_2):
            rew = cons.MARK_FOR_ONE_CARD_TWO_RED + cons.MARK_FOR_ONE_CARD_TWO_BLACK
        elif (typePreHand == self.func.TYPE_THREE_FAIR_STRAIGHT):
            rew = cons.MARK_FOR_THREE_PAIR_STRAIGHT
        elif (typePreHand == self.func.TYPE_FOUR_OF_KIND):
            rew = cons.MARK_FOR_FOUR_OF_KIND
        elif (typePreHand == self.func.TYPE_FOUR_FAIR_STRAIGHT):
            rew = cons.MARK_FOR_FOUR_PAIR_STRAIGHT
        self.totalMarkInRound += rew
        return rew

    def calRewardForPlayer(self, player):
        rew = 0
        arrCard = player.idCards
        if(len(arrCard) == 13):
            rew += (len(arrCard)) * cons.MARK_FOR_ONE_CARD_LEFT * cons.MULTI_FOR_LOST_FULL
        else:
            rew += len(arrCard) * cons.MARK_FOR_ONE_CARD_LEFT
        for iCard in arrCard:
            numCard = self.func.getNumCardByCardId(iCard)
            if(numCard == 2):
                suitCard = self.func.getSuitCardByCardId(iCard)
                if(suitCard <=2):
                    rew += cons.MARK_FOR_ONE_CARD_TWO_BLACK
                else:
                    rew += cons.MARK_FOR_ONE_CARD_TWO_RED
        if(fcc.arrCardHasFourOfKind(arrCard)):
            rew += cons.MARK_FOR_FOUR_OF_KIND
        if(fcc.arrCardHasThreePairStraight(arrCard)):
            rew += cons.MARK_FOR_THREE_PAIR_STRAIGHT
        if(fcc.arrCardHasFourPairStraight(arrCard)):
            rew += cons.MARK_FOR_FOUR_PAIR_STRAIGHT
        return rew

    # Tim nguoi den lang
    def getPayForAllPlayer(self):
        count = 0
        for player in self.listPlayer:
            if(len(player.idCards) == 13):
                count += 1
        if(count >= 2):
            return self.historyNotDiscard[0]
        return -1

    def step(self, action):
        cPlayer = self.indexCurrentPlayer
        self.updateGame(action)
        if self.gameOver == False:
            reward = self.rewardStep
            done = False
            info = {}
        else:
            reward = self.rewards
            done = True
            info = {}
            info['numTurns'] = self.round
            info['rewards'] = self.rewards
            info['count_action_fail'] = self.countActionFail
            info['count_has_card_not_discard'] = self.countHasCardNotDiscard
            #what else is worth monitoring?            
            self.reset()
        return np.array(self.inputNetwork[self.indexCurrentPlayer]), reward, done, info


    def updateInputNetwork(self):
        self.inputNetwork = []
        for player in self.listPlayer:
            arrInput = fci.createInput(self.listPlayer, player.index, np.array(self.lastGroup), self.isMustPlayThreeSpider)
            self.inputNetwork.append(arrInput)
            self.countBitInput = len(arrInput)
        self.inputNetwork = np.array(self.inputNetwork)

    def getActionUseful(self):
        countAction = 0
        cards = self.func.sortCard(self.listPlayer[self.indexCurrentPlayer].idCards)
        actionavailable = np.zeros((len(self.actions)))
        if(len(self.lastGroup) == 0):
            for i in range(len(self.actions)):
                arrCard = self.func.convertActionToArrCard(self.actions[i], cards)
                if arrCard is not None:
                    if(self.func.acceptDiscards(arrCard, self.isMustPlayThreeSpider)):
                        actionavailable[i] = 1
                        countAction += 1
        else:
            for i in range(len(self.actions)):
                arrCard = self.func.convertActionToArrCard(self.actions[i],cards)
                if arrCard is not None:
                    if(self.func.compareTwoArrayCard(self.lastGroup, arrCard)):
                        actionavailable[i] = 1
                        countAction += 1
        self.listPlayer[self.indexCurrentPlayer].numberActionAvailable = countAction
        return np.array(actionavailable, np.float)

    def getCurrentState(self):
        actionAva = self.convertAvailableActions(self.getActionUseful())
        return self.indexCurrentPlayer, self.inputNetwork[self.indexCurrentPlayer], actionAva
    
#now create a vectorized environment

