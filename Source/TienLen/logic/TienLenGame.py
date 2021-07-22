from numpy.lib.function_base import select
from logic.ActionSpace import ActionSpace
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

class TienLenGame:
    actions = []
    indexCurrentPlayer = 0
    indexStartRound = 0
    lastGroup = []
    listPlayer = []
    lastWinner = -1
    gameOver = False
    round = 0
    numGame = 0
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

    def __init__(self,):
        self.actions = ActionSpace().actions
        self.resetGame()
    def convertAvailableActions(availAcs):
        #convert from (1,0,0,1,1...) to (0, -math.inf, -math.inf, 0,0...) etc
        availAcs[np.nonzero(availAcs==0)] = -math.inf
        availAcs[np.nonzero(availAcs==1)] = 0
        return availAcs
    def resetGame(self):
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

        if(self.checkFastWin()):
            self.lastWinner = -1
            self.resetGame()

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
        self.gameOver = False
        self.isGetIndex = True
        self.resetRound()

        self.updateInputNetwork()

    # điều kiện win nhanh: tứ 2, sảnh rồng, 6 đôi, 4 xám, 5 đôi thông, nếu là ván khởi động có bộ chứa 3 bích chặn 2
    def checkFastWin(self):
        for i in range(4):
            if(fcc.checkFastWin(self.listPlayer[i].idCards, self.lastWinner == -1) > 0):
                return True
        return False

    def resetRound(self):
        self.indexStartRound = self.indexCurrentPlayer
        self.round += 1
        for player in self.listPlayer:
            player.isInRound = True
        self.numPlayerFold = 0
        self.totalMarkInRound = 0
        if(len(self.historyNotDisCardInRound) > 0):
            self.historyNotDiscard = self.historyNotDisCardInRound + self.historyNotDiscard
        self.historyNotDisCardInRound = []

    def getAction(self):
        if(self.indexStartRound == self.indexCurrentPlayer):
            return 1
        else:
            return random.randint(0,2)
    
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
        player = self.listPlayer[self.indexCurrentPlayer]
        arrCard = self.func.convertActionToArrCard(self.actions[action], player.idCards)
        playerCards = np.ndarray.tolist(player.idCards)
        for iCard in arrCard:
            playerCards.remove(iCard)
        player.idCards = np.array(playerCards)
        playerDiscard = np.ndarray.tolist(player.currentPlayed)
        playerDiscard.append(arrCard)
        player.currentPlayed = np.array(playerDiscard)
        if(len(arrCard) == 0 and player.numberActionAvailable > 1):
            self.historyNotDisCardInRound.append(player.index)
        self.isGetIndex = False
        self.isMustPlayThreeSpider = False
        self.getIndexNext()
        self.updateInputNetwork()

    def calReward(self, typePrevHand, typeActionHand):
        self.rewards = np.zeros((len(self.listPlayer)))
        self.rewardStep = self.rewardStep(typePrevHand, typeActionHand)
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
        self.updateGame(action)
        if self.gameOver == False:
            reward = self.rewardStep
            done = False
            info = None
        else:
            reward = self.rewards
            done = True
            info = {}
            info['numTurns'] = self.round
            info['rewards'] = self.rewards
            #what else is worth monitoring?            
            self.resetGame()
        return reward, done, info


    def updateInputNetwork(self):
        self.inputNetwork = []
        for player in self.listPlayer:
            arrInput = fci.createInput(self.listPlayer, player.index, np.array([]), self.isMustPlayThreeSpider)
            self.inputNetwork.append(arrInput)
            self.countBitInput = len(arrInput)
        self.inputNetwork = np.array(self.inputNetwork)

    def getActionUseful(self):
        countAction = 0
        cards = self.func.sortCard(self.listPlayer[self.indexCurrentPlayer].idCards)
        actionavailable = np.zeros((len(self.actions)))
        if(self.indexCurrentPlayer == self.indexStartRound):
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
        return actionavailable

    def getCurrentState(self):
        return self.indexCurrentPlayer, self.inputNetwork[self.indexCurrentPlayer].reshape(1, self.countBitInput), self.convertAvailableActions(self.getActionUseful()).reshape(1, len(self.actions))
    
#now create a vectorized environment
def worker(remote, parent_remote):
    parent_remote.close()
    game = TienLenGame()
    while True:
        cmd, data = remote.recv()
        if cmd == 'step':
            reward, done, info = game.step(data)
            remote.send((reward, done, info))
        elif cmd == 'reset':
            game.resetGame()
            pGo, cState, availAcs = game.getCurrentState()
            remote.send((pGo,cState))
        elif cmd == 'getCurrState':
            pGo, cState, availAcs = game.getCurrentState()
            remote.send((pGo, cState, availAcs))
        elif cmd == 'close':
            remote.close()
            break
        else:
            print("Invalid command sent by remote")
            break
        

class vectorizedTienLenGame(object):
    def __init__(self, nGames):
        
        self.waiting = False
        self.closed = False
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nGames)])
        self.ps = [Process(target=worker, args=(work_remote, remote)) for (work_remote, remote) in zip(self.work_remotes, self.remotes)]
        
        for p in self.ps:
            p.daemon = True
            p.start()
        for remote in self.work_remotes:
            remote.close()
            
    def step_async(self, actions):
        for remote, action in zip(self.remotes, actions):
            remote.send(('step', action))
        self.waiting = True
        
    def step_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        rewards, dones, infos = zip(*results)
        return rewards, dones, infos
    
    def step(self, actions):
        self.step_async(actions)
        return self.step_wait()
        
    def currStates_async(self):
        for remote in self.remotes:
            remote.send(('getCurrState', None))
        self.waiting = True
        
    def currStates_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        pGos, currStates, currAvailAcs = zip(*results)
        return np.stack(pGos), np.stack(currStates), np.stack(currAvailAcs)
    
    def getCurrStates(self):
        self.currStates_async()
        return self.currStates_wait()
    
    def close(self):
        if self.closed:
            return
        if self.waiting:
            for remote in self.remotes:
                remote.recv()
        for remote in self.remotes:
            remote.send(('close', None))
        for p in self.ps:
            p.join()
        self.closed = True

