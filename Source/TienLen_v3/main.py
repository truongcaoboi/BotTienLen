import time
import numpy as np
from logic.TienLenGame import TienLenGame, vectorizedTienLenGame
from ppo.PPONetworkKeras import Agent
import tensorflow as tf
from multiprocessing import Process, Pipe

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

tf.config.run_functions_eagerly(True)

file_log = open("info_log.txt", "a+")

#now create a vectorized environment
def worker_agent_train(remote, parent_remote, agent):
    parent_remote.close()
    agent = agent
    while True:
        cmd, data = remote.recv()
        if cmd == 'train_index_game':
            agent.learning(data)
        elif cmd == 'close':
            remote.close()
            break
        else:
            print("Invalid command sent by remote")
            break
        

class vectorizedAgentTrain(object):
    def __init__(self, nGames, agent):
        self.waiting = False
        self.closed = False
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nGames)])
        self.ps = [Process(target=worker_agent_train, args=(work_remote, remote, agent)) for (work_remote, remote) \
                    in zip(self.work_remotes, self.remotes)]
        
        for p in self.ps:
            p.daemon = True
            p.start()
        for remote in self.work_remotes:
            remote.close()
            
    def learning_async(self, indexs):
        for remote, index in zip(self.remotes, indexs):
            remote.send(('train_index_game', index))
        self.waiting = True
        
    def learning_wait(self):
        self.waiting = False
        return
    
    def learning(self, indexs):
        self.learning_async(indexs)
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





@tf.function
def train(n_game=1, n_steps=200, batch_size=10):
    agent = Agent(n_game)
    n_train = n_steps // (n_game * batch_size) + 1
    vec = vectorizedTienLenGame(n_game)
    vec_to_learning = vectorizedAgentTrain(n_game, agent)
    for _ in range(n_train):
        start = time.time()
        for __ in range(batch_size):
            index_players, observations, action_availables = vec.getCurrStates()
            action_exs, actions, values, log_probs = [], [], [], []
            for i in range(n_game):
                action_ex, action, value, log_prob = \
                    agent.choose_action(observations[i], action_availables[i])
                action_exs.append(action_ex)
                actions.append(action)
                values.append(value)
                log_probs.append(log_prob)
                
            
            rewards, dones, infos = vec.step(action_exs)
            for index_game in range(n_game):
                agent.storage(observations[index_game],\
                                action_availables[index_game],\
                                actions[index_game],\
                                log_probs[index_game],\
                                values[index_game],\
                                rewards[index_game],\
                                dones[index_game],\
                                index_game,\
                                index_players[index_game])
                if(dones[index_game]):
                    str_log = "On turn train {} Game {} Finish with round {} has infogame {}".format(
                        (_ + 1), index_game , infos[index_game]["numTurns"], infos[index_game]["infoGame"]
                    )
                    print(str_log)
                    file_log.write(str_log+"\n")
                    file_log.flush()
        indexs_to_learning = np.arange(0,n_game,1,dtype=np.int)
        agent.update()
        # vec_to_learning.learning(indexs_to_learning)
        agent.save_model()
        agent.clear_memory()
        end = time.time()
        str_log = f"Train {_}. Run {n_game * batch_size} steps and update models in {end - start} seconds"
        print(str_log)
        file_log.write(str_log+"\n")
        file_log.flush()

if(__name__ == "__main__"):
    start = time.time()
    train(4, 1600, 200)
    end = time.time()
    str_log = f"Total time {end - start} seconds"
    print(str_log)
    file_log.write(str_log+"\n")
    file_log.flush()
    file_log.close()