import numpy as np
from .Util import Util
class ActionSpace:
    actions = []
    def __init__(self):
        self.loadActionSpace()

    def loadActionSpace(self):
        fileName = "tmp/tienlen/arrayBinary13.npz"
        try:
            self.actions = np.load(fileName)["data"]
        except Exception:
            self.actions = Util().generateArrayBinary(13)

    def getActionSpaceById(self,id):
        return np.array(self.actions[id])
    