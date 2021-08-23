import numpy as np
from ppo.NetworkPPO import Agent
from logic.TienLenGame import TienLenGame
from utils.Util import Util
import json
ut = Util()

env = TienLenGame()

N = 100
batch_size = 512
n_epochs = 4
alpha = 0.00025
agent = Agent(n_actions=env.action_space.n, batch_size= batch_size, alpha= alpha, n_epochs= n_epochs, input_dims= env.observation_space.shape)
agent.load_models()
n_games = 100
learn_iters= 0

class Simulation():
    def __init__(self) -> None:
        self.envSim = TienLenGame()
        pass

    def run(self,):
        for i in range(n_games):
            mark_player = np.zeros((4))
            self.envSim.reset()
            index, observation, actionAva = self.envSim.getCurrentState()
            done = False
            score = 0
            n_steps = 0
            while not done:
                # print("player {} has actionAva: {} and lastGroup: {}".format(index, actionAva, self.envSim.lastGroup))
                action_ex, action, prob, val = agent.choose_action(observation, actionAva)
                observation_, reward, done, info = self.envSim.step(action_ex)
                n_steps += 1
                
                agent.remember(observation, action, prob, val, reward, done,actionAva, index)

                if(done):
                    score += reward[index]
                    for i in range(4):
                        mark_player[i] += reward[i]
                    objectInfo = {}
                    objectInfo["total_score"] = score
                    marks = []
                    for m in mark_player:
                        marks.append(m)
                    objectInfo["mark_player"] = marks
                    objectInfo["count_action_fail"] = self.envSim.countActionFail
                    objectInfo["count_has_card_not_discard"] = self.envSim.countHasCardNotDiscard
                    strInfo = json.dumps(objectInfo)
                    ut.printStrIntoFile(strContent=strInfo, fileName="info_each_game.txt")

                    
                    agent.learn()
                    agent.save_models()
                else:
                    score += reward
                    mark_player[index] += reward
                    if n_steps % N == 0:
                        agent.learn()
                        learn_iters += 1
                        agent.save_models()

                index, observation, actionAva = self.envSim.getCurrentState()

print("END")