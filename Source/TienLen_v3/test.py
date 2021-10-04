from os import times
from logic.TienLenGame import TienLenGame


from logic.TienLenGame import TienLenGame
from logic.ActionSpace import ActionSpace
import numpy as np
import time

action_space = ActionSpace()
env = TienLenGame(action_space.actions, action_space.actions_new)
env.reset()
playertest = -1
while(env.gameOver == False):
    index, obs, actionA = env.getCurrentState()

    actionA = np.reshape(actionA, (8192,))
    actionIndex = [i for i in range(len(actionA)) if actionA[i] == 0.]
    print(f"Player in turn: {index}")
    if(playertest == -1):
        playertest = index
    if(index == playertest):
        np.random.shuffle(actionIndex)
        env.step(actionIndex[0])
    else:
        env.step(0)
    print(f"List index has card but not dis card: {env.historyNotDiscard}")
    time.sleep(1)
