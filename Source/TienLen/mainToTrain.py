from tokenize import endpats
import numpy as np
from ppo.NetworkPPO import Agent, MultiPPOMemory
from logic.TienLenGame import TienLenGame
from utils.Util import Util
import json
from logic.ActionSpace import ActionSpace
from torch.multiprocessing import Process, Pipe, set_start_method, Pool
import time


def worker(remote, parent_remote, env):
    parent_remote.close()
    game = env
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
        else:
            print("Invalid command sent by remote")
            break
        

class vectorizedTienLenGame(object):
    def __init__(self, nGames, action_spaces):
        
        self.waiting = False
        self.closed = False
        self.envs = []
        for i in range(nGames):
            env = TienLenGame(action=action_spaces)
            env.reset()
            self.envs.append(env)
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nGames)])
        self.ps = [Process(target=worker, args=(work_remote, remote, game)) for (work_remote, remote, game) in zip(self.work_remotes, self.remotes, self.envs)]
        
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
    def __init__(self, n_game, n_step, batch_size=512, alpha= 0.00025, n_epochs=4) -> None:
        self.batch_size = batch_size
        self.action_spaces = ActionSpace().actions
        self.ut = Util()
        self.n_game = n_game
        self.n_step = n_step
        self.vector_train = vectorizedTienLenGame(n_game, self.action_spaces)
        self.multi_memory = MultiPPOMemory(batch_size,n_game)

        self.action_space_n = 8192
        self.input_dim = (746,)
        self.alpha = alpha
        self.n_epochs = n_epochs
        self.agent = Agent(input_dims=self.input_dim, n_actions=self.action_space_n,
            alpha= self.alpha, batch_size=self.batch_size,n_epochs=self.n_epochs)
        self.agent.load_models()
        self.mark_players = np.zeros((self.n_game, 4))

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
                else:
                    mark_player[index] += reward
                    

    def train(self, n_train):
        n_update = n_train // (self.n_game * self.n_step)
        for _ in range(n_update):
            self.run()
            for mem in self.multi_memory.memories:
                self.agent.set_memory(mem)
                self.agent.learn()
                self.agent.save_models()

if __name__ == "__main__":
    try:
        set_start_method('spawn')
    except RuntimeError:
        pass
    start = time.time()
    sim = Simulation(4, 20)
    sim.train(1000)
    end = time.time()
    print("END with {} seconds".format(end - start))

