import math
import os
import numpy as np
from numpy.lib.function_base import select
import torch as T
import torch.nn as nn
from torch.nn.modules.activation import ReLU
import torch.optim as optim
from torch.distributions.categorical import Categorical
from torch.distributions import MultivariateNormal

class PPOMemory:
    def __init__(self, batch_size):
        self.end_game = False
        self.states = []
        self.probs = []
        self.vals = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.actionsAvailables = []
        self.batch_size = batch_size
    
    def generate_batches(self):
        n_states = len(self.states)
        batch_start = np.arange(0, n_states, self.batch_size)
        indices = np.arange(n_states, dtype= np.int)
        np.random.shuffle(indices)
        batches = [indices[i:i+self.batch_size] for i in batch_start]

        return np.array(self.states),\
               np.array(self.actions),\
               np.array(self.probs),\
               np.array(self.vals),\
               np.array(self.rewards),\
               np.array(self.dones),\
               np.array(self.actionsAvailables),\
               batches

    def store_memory(self, state, action, probs, vals, reward, done, actionAvailable,index):
        self.states.append(state)
        self.actions.append(action)
        self.probs.append(probs)
        self.vals.append(vals)
        if(done):
            self.rewards.append([index, 0])
            self.dones.append(done)
            self.end_game = True
            last_index_player = [-1,-1,-1,-1]
            for i in range(len(self.rewards)):
                last_index_player[self.rewards[i][0]] = i
            for i in range(len(last_index_player)):
                if(last_index_player[i] != -1):
                    self.dones[last_index_player[i]] = True
                    self.rewards[last_index_player[i]][1] += reward[i]
        else:
            self.rewards.append([index, reward])
            self.dones.append(done)
        self.actionsAvailables.append(actionAvailable)

    def clear_memory(self):
        if(self.end_game):
            self.states = []
            self.actions = []
            self.probs = []
            self.vals = []
            self.rewards = []
            self.dones = []
            self.actionsAvailables = []
            self.end_game = False
        else:
            states = []
            actions = []
            probs = []
            vals = []
            rewards = []
            dones = []
            actionsAvailables = []
            last_index_player = [-1,-1,-1,-1]
            for i in range(len(self.rewards)):
                last_index_player[self.rewards[i][0]] = i
            for i in last_index_player:
                if i != -1:
                    states.append(self.states[i])
                    actions.append(self.actions[i])
                    probs.append(self.probs[i])
                    vals.append(self.vals[i])
                    rewards.append(self.rewards[i])
                    dones.append(self.dones[i])
                    actionsAvailables.append(self.actionsAvailables[i])
            self.states = states
            self.actions = actions
            self.probs = probs
            self.vals = vals
            self.rewards = rewards
            self.dones = dones
            self.actionsAvailables = actionsAvailables
            


class ActionNetwork(nn.Module):
    def __init__(self, n_actions, input_dims, alpha, fc1_dims = 512, fc2_dims = 256, chkpt_dir = "tmp/ppo"):
        super(ActionNetwork, self).__init__()

        self.checkpoint_file = os.path.join(chkpt_dir, 'actor_network_ppo_tienlenbot')
        self.action_var = []
        self.actor = nn.Sequential(
            nn.Linear(*input_dims, fc1_dims),
            nn.ReLU(),
            nn.Linear(fc1_dims, fc2_dims),
            nn.ReLU(),
            nn.Linear(fc2_dims, n_actions),
            nn.ReLU()
        )
        self.action_dims = n_actions
        self.optimizer = optim.Adam(self.parameters(), lr= alpha)
        self.device = T.device('cpu')
        if T.cuda.is_available():
            self.device = T.device('cuda:0') 
        self.to(self.device)

    def set_action_var(self, action_new):
        self.action_var = T.tensor(action_new, dtype= T.float32).to(self.device)

    def forward(self, state, actionAva, is_get_action):
        # dist = self.actor(state)
        # dist = Categorical(dist)
        # return dist
        self.set_action_var(actionAva)
        action_mean = self.actor(state)
        if(is_get_action == True):
            cov_mat = T.diag(self.action_var).unsqueeze(dim=0)
            dist = MultivariateNormal(action_mean, covariance_matrix=cov_mat)
        else:
            action_var = self.action_var.expand_as(action_mean)
            cov_mat = T.diag_embed(action_var).to(self.device)
            dist = MultivariateNormal(action_mean, covariance_matrix=cov_mat)
        return dist

    def save_checkpoint(self):
        T.save(self.state_dict() , self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))

class CriticNetwork(nn.Module):
    def __init__(self, input_dims, n_actions, alpha, fc1_dims = 512, fc2_dim2 = 256, chkpt_dir = "tmp/ppo"):
        super(CriticNetwork, self).__init__()

        self.checkpoint_file = os.path.join(chkpt_dir, 'critic_network_ppo_tienlenbot')
        self.action_var = []
        self.critic = nn.Sequential(
            nn.Linear(*input_dims, fc1_dims),
            nn.ReLU(),
            nn.Linear(fc1_dims, fc2_dim2),
            nn.ReLU(),
            nn.Linear(fc2_dim2, 1)
        )
        self.action_dims = n_actions
        self.optimizer = optim.Adam(self.parameters(), lr= alpha)
        self.device = T.device('cpu')
        if T.cuda.is_available():
            self.device = T.device('cuda:0')
        self.to(self.device)

    def set_action_var(self, action_new):
        self.action_var = T.tensor(action_new, dtype= T.float32).to(self.device)

    def forward(self, state):
        value = self.critic(state)
        return value

    def save_checkpoint(self):
        T.save(self.state_dict() , self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))

class Agent:
    def __init__(self,input_dims, n_actions, gamma = 0.99, alpha = 0.0003, gae_lambda = 0.95,
                 policy_clip = 0.1, batch_size = 64, N = 2024, n_epochs = 10):
        self.gamma = gamma
        self.alpha = alpha
        self.gae_lambda = gae_lambda
        self.policy_clip = policy_clip
        self.n_epochs = n_epochs

        self.actor = ActionNetwork(n_actions= n_actions, input_dims= input_dims, alpha = alpha)
        self.critic = CriticNetwork(input_dims=input_dims, n_actions=n_actions, alpha= alpha)
        self.memory = PPOMemory(batch_size)
        # print(self.policy_clip)
        
    def remember(self, state, action, probs, vals, reward, done, actionAva, index):
        self.memory.store_memory(state, action,probs,vals,reward,done, actionAva, index)

    def save_models(self):
        print("=========== save models ============")
        self.actor.save_checkpoint()
        self.critic.save_checkpoint()

    def load_models(self):
        try:
            print("... load models ...")
            self.actor.load_checkpoint()
            self.critic.load_checkpoint()
        except Exception:
            print(Exception)

    def choose_action(self, observation, actionAva):
        state = T.tensor([observation], dtype=T.float32).to(self.actor.device)
        dist = self.actor(state, actionAva, True)
        value = self.critic(state)
        action = dist.sample()
        probs = T.squeeze(dist.log_prob(action)).item()
        value = T.squeeze(value).item()

        return action, probs, value

    def learn(self):
        print("=============learning================")
        for _ in range(self.n_epochs):
            print("lan thu {}".format(_))
            state_arr, action_arr, old_probs_arr, vals_arr,\
                reward_arr, done_arr, action_ava_arr, batches = self.memory.generate_batches()
            values = vals_arr
            advantage = np.zeros(len(reward_arr), dtype= np.float)

            endT = len(reward_arr)

            for t in range(endT):
                index_player = reward_arr[t][0]
                discount = 1
                a_t = 0
                for k in range(t, endT):
                    if(reward_arr[k][0] == index_player):
                        next_k = -1
                        for nk in range(k+1, endT):
                            if(reward_arr[nk][0] == index_player):
                                next_k = nk
                                break
                        if(next_k != -1):
                            a_t += discount * (reward_arr[k][1] + self.gamma * values[next_k]*\
                                (1 - int(done_arr[k])) - values[k]) 
                            discount *= self.gae_lambda * self.gamma
                        else:
                            if(done_arr[k]):
                                a_t += discount * (reward_arr[k][1] - values[k]) 
                                discount *= self.gae_lambda * self.gamma
                advantage[t] = a_t

            advantage = T.tensor(advantage).to(self.actor.device)
            print(advantage)
            values = T.tensor(values).to(self.actor.device)
            for batchx in batches:
                for batch in batchx:
                    states = T.tensor(state_arr[batch], dtype= T.float32).to(self.actor.device)
                    old_probs = T.tensor(old_probs_arr[batch], dtype=T.float32).to(self.actor.device)
                    actions = T.tensor(action_arr[batch], dtype=T.float32).to(self.actor.device)
                    action_ava = action_ava_arr[batch]
                    print("in batch {}".format(batch))
                    
                    dist = self.actor(states, action_ava, False)
                    critic_value = self.critic(states)
                    critic_value = T.squeeze(critic_value)

                    dist_entropy = dist.entropy()
                    new_probs = dist.log_prob(actions)
                    prob_ratio = T.exp(new_probs.detach() - old_probs.detach())
                    weighted_probs = advantage[batch] * prob_ratio
                    weighted_probs = weighted_probs
                    weighted_clipped_probs = T.clamp(prob_ratio, 1 - self.policy_clip, 1 + self.policy_clip) * advantage[batch]
                    weighted_clipped_probs = weighted_clipped_probs
                    print("{} {} {} {} {} {} {}".format(dist_entropy,old_probs, new_probs, prob_ratio, weighted_probs, weighted_clipped_probs, advantage[batch]))
                    actor_loss = -T.min(weighted_probs, weighted_clipped_probs).mean()
                    returns = advantage[batch] + values[batch]
                    returns = returns
                    critic_loss = (returns - critic_value) ** 2
                    critic_loss = critic_loss.mean()
                    total_loss = actor_loss + 0.5 * critic_loss - 0.01 * dist_entropy
                    print("total_loss: {}".format(total_loss))
                    self.actor.optimizer.zero_grad()
                    self.critic.optimizer.zero_grad()
                    total_loss.mean().backward()
                    T.nn.utils.clip_grad_norm_(self.actor.parameters(), max_norm=0.5, error_if_nonfinite=False)
                    T.nn.utils.clip_grad_norm_(self.critic.parameters(), max_norm=0.5, error_if_nonfinite=False)
                    self.actor.optimizer.step()
                    self.critic.optimizer.step()

        self.memory.clear_memory()
        print("===========end learning===========")