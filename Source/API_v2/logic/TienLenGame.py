import numpy as np
from .Player import Player
from .ActionSpace import ActionSpace
from .Function import Function
from . import FunctionCreaateInput as fci
class TienLenGame:
    def __init__(self):
        self.actions = ActionSpace().actions
        self.index_current = 0
        self.list_player = []
        self.is_must_three_spider = False
        self.last_group = []
        self.func = Function()

    def set_info_current(self, data):
        self.index_current = data["index"]
        self.list_player = []
        index_start = 0
        for info_player in data["listplayer"]:
            ids_card = info_player["idCards"]
            current_played = info_player["cardPlayed"]
            player = Player(index= index_start, idCards= ids_card, currentPlayed= current_played)
            self.list_player.append(player)
            index_start += 1
        while(len(self.list_player) < 4):
            self.list_player.append(Player(index= index_start, idCards= [], currentPlayed= []))
            index_start += 1
        self.last_group = data["lastGroup"]
        self.is_must_three_spider = data["isMustThreeSpider"]

    def convertAvailableActions(self,availAcs):
        #convert from (1,0,0,1,1...) to (0, -math.inf, -math.inf, 0,0...) etc
        availAcs[np.nonzero(availAcs==0)] = 0.000001
        availAcs[np.nonzero(availAcs==1)] = 1
        return availAcs

    def getActionUseful(self):
        countAction = 0
        cards = self.func.sortCard(self.list_player[self.index_current].idCards)
        actionavailable = np.zeros((len(self.actions)))
        if(len(self.last_group) == 0):
            for i in range(len(self.actions)):
                arrCard = self.func.convertActionToArrCard(self.actions[i], cards)
                if arrCard is not None:
                    if(self.func.acceptDiscards(arrCard, self.is_must_three_spider)):
                        actionavailable[i] = 1
                        countAction += 1
        else:
            for i in range(len(self.actions)):
                arrCard = self.func.convertActionToArrCard(self.actions[i],cards)
                if arrCard is not None:
                    if(self.func.compareTwoArrayCard(self.last_group, arrCard)):
                        actionavailable[i] = 1
                        countAction += 1
        return np.array(actionavailable, np.float)

    def create_action_availabel(self):
        return self.convertAvailableActions(self.getActionUseful())

    def create_input_network(self):
        arrInput = fci.createInput(self.list_player, self.index_current, np.array(self.last_group), self.is_must_three_spider)
        return np.array(arrInput)

    def get_cardids(self, action):
        cardIds = self.func.convertActionToArrCard(self.actions[action], self.list_player[self.index_current].idCards)
        return np.ndarray.tolist(cardIds)