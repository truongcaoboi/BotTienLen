import numpy as np


class Player:
    index = 0
    idCards = []
    currentPlayed = []
    countPlayError = 0
    isInRound = True
    numberActionAvailable = 0
    
    def __init__(self, index, idCards = [], currentPlayed = []):
        self.index = index
        self.idCards = np.array(idCards)
        self.currentPlayed = np.array(currentPlayed)
        self.isInRound = True
        pass
    
    def resetInfo(self):
        self.idCards = []
        self.currentPlayed = []
        self.countPlayError = 0
        self.isInRound = True