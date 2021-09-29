from multiprocessing import Pipe, Process

import numpy as np
from utils.Util import Util
from logic.Function import Function
import time
from logic.TienLenGame import TienLenGame
from logic.ActionSpace import ActionSpace
from ppo.NetworkPPO import Agent

ac = ActionSpace()
batch_size = 32
action_spaces = ac.actions
action_new = ac.actions_new
ut = Util()
n_game = 1
n_step = 20

action_space_n = 8192
input_dim = (746,)
alpha = 0.00025
n_epochs = 4
agent = Agent(input_dims=input_dim, n_actions=action_space_n,
    alpha= alpha, batch_size=batch_size,n_epochs=n_epochs)
agent.load_models()

env = TienLenGame(action=action_spaces, actions_new=action_new)
env.reset()

start = time.time()

index, obs, actionA = env.getCurrentState()
end = time.time()
print(end - start)
start = time.time()
action_ex, action, prob, val = agent.choose_action(obs, actionA)
end = time.time()


print(end - start)