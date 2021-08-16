from os import environ
import gym
import numpy as np
import torch as T
from ppo.pponetworktest import Agent
from torch.distributions import MultivariateNormal

env = gym.make("CartPole-v0")

def train(env):
    N = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0003
    agent = Agent(n_actions=env.action_space.n, batch_size= batch_size, alpha= alpha, n_epochs= n_epochs, input_dims= env.observation_space.shape)
    n_games = 300
    # figure_file = "plots/cartpole.png"
    best_score = env.reward_range[0]
    score_history = []
    learn_iters = 0
    avg_score = 0
    n_steps = 0
    for i in range(n_games):
        observation = env.reset()
        done = False
        score = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            n_steps += 1
            score += reward
            agent.remember(observation, action, prob, val, reward, done)
            if n_steps % N == 0:
                agent.learn()
                learn_iters += 1
            observation = observation_
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        
        if avg_score > best_score: 
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score, 'time_step', n_steps, 'learning_step', learn_iters)

def run(env):
    N = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0003
    agent = Agent(n_actions=env.action_space.n, batch_size= batch_size, alpha= alpha, n_epochs= n_epochs, input_dims= env.observation_space.shape)
    agent.load_models()
    for i in range(10):
        observation = env.reset()
        env.render()
        done = False
        score = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            env.render()
            observation = observation_
        print("game %d" % i, 'has score', score)

# a = np.array([1,-1])
# b = np.array([4,1])

# ma = T.tensor(a , dtype=T.float64).to(T.device("cpu"))
# cov = T.diag(T.tensor(b,dtype=T.float64).to(T.device("cpu"))).unsqueeze(dim=0)
# d = MultivariateNormal(ma, covariance_matrix=cov)
# actions = d.sample()
# print(actions)
# action = actions.detach().cpu().numpy().flatten()
# print(action)
# print(np.argmax(action))
a = T.tensor(np.array([100]), dtype=T.float64).to(T.device("cpu"))
print(a / 2)