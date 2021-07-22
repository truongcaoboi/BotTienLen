import numpy as np
from numpy.random import set_state
from utils.Util import Util
class ActionSpace:
    actions = []
    def __init__(self):
        self.actions = self.loadActionSpace()

    def loadActionSpace(self):
        fileName = "Dump/arrayBinary13.npz"
        try:
            self.actions = np.load(fileName)["data"]
        except Exception:
            self.actions = Util().generateArrayBinary()

    def getActionSpaceById(self,id):
        return np.array(self.actions[id])
    