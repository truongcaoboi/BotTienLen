import gym
from PPONetwork import PPONetwork
from stable_baselines3.common.env_util import make_vec_env
from Enviroment import Enviroment
env = Enviroment()
model = PPONetwork("MlpPolicy", env)
model.learn(10000)
obs = env.reset()
count = 0
for i in range(1):
    count = 0
    dones = False
    obs = env.reset()
    # env.render()
    while(not dones):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        # env.render()
        count += 1
    print(count)
input()
