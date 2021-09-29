from os import stat
from tokenize import endpats
import numpy as np
from ppo.NetworkPPO import Agent, MultiPPOMemory
from logic.TienLenGame import TienLenGame
from utils.Util import Util
import json
from logic.ActionSpace import ActionSpace
from torch.multiprocessing import Process, Pipe, set_start_method, Pool
import time, math
import torch as T
from numba import jit, cuda
file_log = open("log.txt", "w+")

# @jit(target ="cuda")

def worker(remote, parent_remote, env, agent):
    parent_remote.close()
    game = env
    agent = agent
    while True:
        cmd, data = remote.recv()
        if cmd == 'step':
            observation_, reward, done, info = game.step(data)
            remote.send((observation_,reward, done, info))
        elif cmd == 'reset':
            game.reset()
            pGo, cState, availAcs = game.getCurrentState()
            remote.send((pGo,cState,availAcs))
        elif cmd == 'getCurrState':
            pGo, cState, availAcs = game.getCurrentState()
            remote.send((pGo, cState, availAcs))
        elif cmd == 'close':
            remote.close()
            break
        elif cmd == 'train':
            agent.set_memory(data)
            agent.learn()
            agent.save_models()
            break
        else:
            print("Invalid command sent by remote")
            break
        

class vectorizedTienLenGame(object):
    def __init__(self, nGames, action_spaces, actions_new, agent):
        
        self.waiting = False
        self.closed = False
        self.envs = []
        self.agent = agent
        for i in range(nGames):
            env = TienLenGame(action=action_spaces,actions_new=actions_new)
            env.reset()
            self.envs.append(env)
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nGames)])
        self.ps = [Process(target=worker, args=(work_remote, remote, game, agent)) for (work_remote, remote, game) in zip(self.work_remotes, self.remotes, self.envs)]
        
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
        observation_, rewards, dones, infos = zip(*results)
        return observation_, rewards, dones, infos
    
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

    def learning_async(self, mem):
        for remote in self.remotes:
            remote.send(('train', mem))
        self.waiting = True
        
    def learning_wait(self):
        self.waiting = False
        return
    
    def learning(self, mem):
        self.learning_async(mem)
        return self.learning_wait()
    
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

class Simulation:
    def __init__(self, n_game, n_step, batch_size=32, alpha= 0.00025, n_epochs=1) -> None:
        self.batch_size = batch_size
        acs = ActionSpace()
        self.action_spaces = acs.actions
        self.actions_new = acs.actions_new
        self.ut = Util()
        self.n_game = n_game
        self.n_step = n_step
        
        self.multi_memory = MultiPPOMemory(batch_size,n_game)

        self.action_space_n = 8192
        self.input_dim = (746,)
        self.alpha = alpha
        self.n_epochs = n_epochs
        self.agent = Agent(input_dims=self.input_dim, n_actions=self.action_space_n,
            alpha= self.alpha, batch_size=self.batch_size,n_epochs=self.n_epochs)
        self.agent.load_models()
        self.mark_players = np.zeros((self.n_game, 4))

        self.vector_train = vectorizedTienLenGame(n_game, self.action_spaces,self.actions_new, self.agent)

    def run(self):
        for _ in range(self.n_step):
            indexs, observations, actionAvas = self.vector_train.getCurrStates()
            action_exs = []
            actions = []
            probs = []
            vals = []
            for (observation, actionAva) in zip(observations, actionAvas):
                action_ex, action, prob, val = self.agent.choose_action(observation, actionAva)
                action_exs.append(action_ex)
                actions.append(action)
                probs.append(prob)
                vals.append(val)
            observations_, rewards, dones, infos = self.vector_train.step(action_exs)
            for (idgame, index, observation, actionAva, prob, val, reward, done, action, mem, info, mark_player) in \
                zip(range(self.n_game), indexs, observations, actionAvas, probs, vals, rewards, dones, actions, self.multi_memory.memories, infos, self.mark_players):
                mem.store_memory(observation, action, prob, val, reward, done,actionAva, index)
                if(done):
                    for i in range(4):
                        mark_player[i] += reward[i]
                    objectInfo = {}
                    marks = []
                    for m in mark_player:
                        marks.append(m)
                    objectInfo["mark_player"] = marks
                    objectInfo["count_action_fail"] = info["count_action_fail"]
                    objectInfo["count_has_card_not_discard"] = info["count_has_card_not_discard"]
                    strInfo = json.dumps(objectInfo)
                    self.ut.printStrIntoFile(strContent=strInfo, fileName="info_each_game.txt")
                    mark_player = np.zeros((4))
                    self.mark_players[idgame] = mark_player
                    print("finish game")
                    file_log.write("finish game!")
                    file_log.flush()
                else:
                    mark_player[index] += reward
                    

    def train(self, n_train):
        n_update = n_train // (self.n_game * self.n_step)
        start = time.time()
        for _ in range(n_update):
            self.run()
            for mem in self.multi_memory.memories:
                # self.vector_train.learning(mem)
                self.agent.set_memory(mem)
                self.agent.learn()
                self.agent.save_models()

            if( _ % 100 == 0):
                strPrint = "Finish train times: {} in {} seconds\n".format(math.floor( _ /100),(time.time() - start))
                print(strPrint)
                file_log.write(strPrint)
                file_log.flush()

if __name__ == "__main__":
    try:
        set_start_method('spawn')
    except RuntimeError:
        pass
    start = time.time()
    sim = Simulation(8, 20)
    sim.train(100000)
    end = time.time()
    print("END with {} seconds".format(end - start))
    file_log.write("END with {} seconds".format(end - start))
    file_log.flush()
    
file_log.close()

