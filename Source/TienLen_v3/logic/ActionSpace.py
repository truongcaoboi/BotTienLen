import numpy as np
from utils.Util import Util
class ActionSpace:
    actions = []
    actions_new = []
    def __init__(self):
        self.loadActionSpace()

        self.actions_new = []

        for i in range(14):
            self.actions_new.append({"index":0, "array":[]})

        for action in self.actions:
            count = 0
            for bin in action:
                if bin == 1:
                    count += 1
            self.actions_new[count]["array"].append(action)
        index = 0
        for obj in self.actions_new:
            obj["index"] = index
            index += len(obj["array"])

        self.actions = []
        for actionarr in self.actions_new:
            for action in actionarr["array"]:
                self.actions.append(action)

    def loadActionSpace(self):
        fileName = "Dump/arrayBinary13.npz"
        try:
            self.actions = np.load(fileName)["data"]
        except Exception:
            self.actions = Util().generateArrayBinary()

    def getActionSpaceById(self,id):
        return np.array(self.actions[id])
    