import numpy as np
from ppo.NetworkPPO import Agent
from logic.TienLenGame import TienLenGame

env = TienLenGame()

N = 2
batch_size = 10
n_epochs = 4
alpha = 0.00025
agent = Agent(n_actions=env.action_space.n, batch_size= batch_size, alpha= alpha, n_epochs= n_epochs, input_dims= env.observation_space.shape)
agent.load_models()
n_games = 1
learn_iters= 0
for i in range(n_games):
    env.reset()
    index, observation, actionAva = env.getCurrentState()
    done = False
    score = 0
    n_steps = 0
    while not done:
        print("player {} has actionAva: {} and lastGroup: {}".format(index, actionAva, env.lastGroup))
        action, prob, val = agent.choose_action(observation, actionAva)
        action = action.detach().cpu().numpy().flatten()
        action_ex = np.argmax(action)
        print("Gia tri action trong actionAva: {}".format(actionAva[action_ex]))
        observation_, reward, done, info = env.step(action_ex)
        n_steps += 1
        score += reward
        agent.remember(observation, action, prob, val, reward, done,actionAva)
        if n_steps % N == 0:
            agent.learn()
            learn_iters += 1
            agent.save_models()
        index, observation, actionAva = env.getCurrentState()
print("END")