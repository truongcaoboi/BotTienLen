from os import remove
import numpy as np
from numpy.lib.function_base import select
from ppo.NetworkPPO import Agent, PPOMemory
from logic.TienLenGame import TienLenGame
from utils.Util import Util
import json
from multiprocessing import Process, Pipe
import time

def run(env):
    ut = Util()
    batch_size = 512
    alpha = 0.00025
    n_epochs = 4
    agent = Agent(n_actions=env.action_space.n,
                     batch_size=batch_size,
                      alpha=alpha,
                       n_epochs=n_epochs,
                        input_dims= env.observation_space.shape)
    agent.load_models()
    memory = PPOMemory(agent.batch_size)

    mark_player = np.zeros((4))
    index, observation, actionAva = env.getCurrentState()
    done = False
    score = 0
    n_steps = 0
    while not done:
        # print("player {} has actionAva: {} and lastGroup: {}".format(index, actionAva, self.envSim.lastGroup))
        action_ex, action, prob, val = agent.choose_action(observation, actionAva)
        observation_, reward, done, info = env.step(action_ex)
        n_steps += 1
        
        memory.store_memory(observation, action, prob, val, reward, done,actionAva, index)

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
            objectInfo["count_action_fail"] = env.countActionFail
            objectInfo["count_has_card_not_discard"] = env.countHasCardNotDiscard
            strInfo = json.dumps(objectInfo)
            ut.printStrIntoFile(strContent=strInfo, fileName="info_each_game.txt")
        else:
            score += reward
            mark_player[index] += reward

        index, observation, actionAva = env.getCurrentState()
    
    #end while
    return memory

def worker(remote, parent_remote, env):
    parent_remote.close()
    while True:
        cmd, data = remote.recv()
        if cmd == 'run':
            memory = run(env=env)
            remote.send((memory))
        elif cmd == 'close':
            remote.close()
            break
        else:
            print("Invalid command sent by remote")
            break

class VectorTrain(object):
    def __init__(self, nGames):
        
        self.waiting = False
        self.closed = False
        self.envs = []
        for i in range(nGames):
            env = TienLenGame()
            env.reset()
            self.envs.append(env)
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nGames)])
        self.ps = [Process(target=worker, args=(work_remote, remote, env)) for (work_remote, remote, env) in zip(self.work_remotes, self.remotes, self.envs)]
        
        for p in self.ps:
            p.daemon = True
            p.start()
        for remote in self.work_remotes:
            remote.close()
    
    def run_async(self):
        for remote in self.remotes:
            remote.send(("run", None))
        self.waiting = True
    
    def run_wait(self):
        memorys = [remote.recv() for remote in self.remotes]
        self.waiting = False
        return memorys

    def run(self):
        self.run_async()
        return self.run_wait()

class Simulation:
    def __init__(self, alpha = 0.00025, n_epochs = 4, batch_size = 512, n_process = 8):
        self.alpha = alpha
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.n_process = n_process
        self.env = TienLenGame()
        self.agent = Agent(input_dims=self.env.observation_space.shape,
            n_actions= self.env.action_space.n, alpha= alpha, batch_size=batch_size,
            n_epochs=n_epochs, memory=None)
        self.vector_train = VectorTrain(self.n_process)
    
    def train(self,n_game):
        n_train = n_game // self.n_process + 1
        for i in range(n_train):
            memorys = self.vector_train.run()
            for memory in memorys:
                self.agent.set_memory(memory)
                self.agent.learn()
                self.agent.save_models()


start = time.time()
sim = Simulation(n_process=4)
sim.train(100)
end = time.time()
print("END with {} seconds".format(end - start))
