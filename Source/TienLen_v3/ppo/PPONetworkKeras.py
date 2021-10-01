import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, Activation, InputLayer
from tensorflow.python.ops.gen_batch_ops import batch

import logic.Constants as cons
import numpy as np
import time

class PPOMemory:
    def __init__(self, batch_size=64):
        self.observations = []
        self.action_availables = []
        self.actions = []
        self.old_probs = []
        self.old_values = []
        self.rewards = []
        self.dones = []
        self.index_players = []
        self.batch_size = batch_size

    def get_memory(self):
        size_memory = len(self.observations)
        batches = np.arange(0, size_memory, 1, dtype=np.int)
        return self.observations,\
               self.action_availables,\
               self.actions,\
               self.old_probs,\
               self.old_values,\
               self.rewards,\
               self.dones,\
               self.index_players,\
               batches
    
    def store_memory(self, observation, action_available, action, prob, value, reward, done, index_player):
        self.observations.append(observation)
        self.action_availables.append(action_available)
        self.actions.append(action)
        self.old_probs.append(prob)
        self.old_values.append(value)
        self.dones.append(done)
        self.index_players.append(index_player)
        if(done):
            self.rewards.append(reward[index_player])
            for i in range(len(reward)):
                if(i != index_player):
                    for j in range(len(self.index_players) - 1,-1, -1):
                        if(self.index_players[j] == i):
                            self.rewards[j] += reward[i]
                            self.dones[j] = True
                            break
        else:
            self.rewards.append(reward)
        

    def clear_memory(self):
        self.observations = self.observations[-4:]
        self.action_availables = self.action_availables[-4:]
        self.actions = self.actions[-4:]
        self.old_probs = self.old_probs[-4:]
        self.old_values = self.old_values[-4:]
        self.rewards = self.rewards[-4:]
        self.dones = self.dones[-4:]
        self.index_players = self.index_players[-4:]


class PPOActionNetwork(Model):
    def __init__(self):
        super(PPOActionNetwork, self).__init__()
        self.input_layer = InputLayer(input_shape= [1,cons.SIZE_OBSERVATIONS], dtype=tf.float32)
        self.hidden_layer = Dense(cons.SIZE_HIDDEN_1, activation= tf.nn.relu)
        self.hidden_layer_pi = Dense(cons.SIZE_HIDDEN_PI, activation= tf.nn.relu)
        self.pi = Dense(cons.SIZE_ACTION_SPACES, activation=tf.nn.relu)

    def call(self, observation):
        X = self.input_layer(observation)
        h1 = self.hidden_layer(X)
        h2 = self.hidden_layer_pi(h1)
        pi = self.pi(h2)
        return pi
    
    def save(self, filepath, overwrite=True, include_optimizer=True, save_format=None, signatures=None, options=None, save_traces=True):
        return super().save(filepath, overwrite=overwrite, include_optimizer=include_optimizer, save_format=save_format, signatures=signatures, options=options, save_traces=save_traces)


class PPOCriticNetwork(Model):
    def __init__(self):
        super(PPOCriticNetwork, self).__init__()
        self.input_layer = InputLayer(input_shape= [1,cons.SIZE_OBSERVATIONS], dtype=tf.float32)
        self.hidden_layer = Dense(cons.SIZE_HIDDEN_1, activation= tf.nn.relu)
        self.hidden_layer_vf = Dense(cons.SIZE_HIDDEN_VF, activation=tf.nn.relu)
        self.vf = Dense(1, activation=tf.nn.tanh)

    def call(self, observation):
        X = self.input_layer(observation)
        h1 = self.hidden_layer(X)
        h3 = self.hidden_layer_vf(h1)
        vf = self.vf(h3)
        return vf
    
    def save(self, filepath, overwrite=True, include_optimizer=True, save_format=None, signatures=None, options=None, save_traces=True):
        return super().save(filepath, overwrite=overwrite, include_optimizer=include_optimizer, save_format=save_format, signatures=signatures, options=options, save_traces=save_traces)


class Agent(object):
    def __init__(self, n_game=8):
        super(Agent, self).__init__()
        self.ALPHA = 0.00025
        self.GAMMA = 0.99
        self.BATCH_SIZE = 64
        self.N_EPOCHS = 4
        self.N_STEPS = 20
        self.N_GAMES = n_game
        self.LAM = 0.97
        self.MAX_GRAD_NORM = 0.5
        self.SAVE_EVERY = 10
        self.ENT_COEF = 0.5
        self.VF_COEF = 0.5
        self.MIN_LEARNING_RATE = 0.000001
        self.LEARNING_RATE_ACTION = 3e-4
        self.LEARNING_RATE_CRITIC = 1e-3
        self.CLIP_RATIO = 0.2

        self.memories = []
        for i in range(self.N_GAMES):
            mem = PPOMemory()
            self.memories.append(mem)

        self.actor, self.critic = self.load_model_network()
        self.action_optimizer = keras.optimizers.Adam(learning_rate=self.LEARNING_RATE_ACTION)
        self.critic_optimizer = keras.optimizers.Adam(learning_rate=self.LEARNING_RATE_CRITIC)

    @tf.function
    def choose_action(self, observation, action_available):
        action_ava = tf.Variable(action_available, dtype= tf.float32)
        #forward network to cal logits and value
        logits, value = (self.actor(observation), self.critic(observation))
        action_cal = tf.add(logits, action_ava)
        #distributions to get action
        action = tf.squeeze(tf.random.categorical(action_cal, 1), axis=1)
        #cal logprobaility
        logprobability = self.get_log_probability(logits, action)
        action_ex = action.numpy()[0]
        return action_ex, action, value, logprobability

    
    def storage(self, observation, action_available, action, prob, value, reward, done, index_game, index_player):
        self.memories[index_game].store_memory(observation, action_available, action, prob, value, reward, done, index_player)

    def save_model(self):
        print("================================Saving model================================")
        self.actor.save("tmp/ppo/action_network_ppo_keras")
        self.critic.save("tmp/ppo/critic_network_ppo_keras")
        print("============================Completely save model===========================")

    def load_model_network(self):
        print("================================Loading model===============================")
        try:
            model_action = load_model("tmp/ppo/action_network_ppo_keras")
            model_critic = load_model("tmp/ppo/critic_network_ppo_keras")
        except Exception:
            print(Exception)
            model_action = PPOActionNetwork()
            model_critic = PPOCriticNetwork()
        print("============================Completely loading model========================")
        return model_action, model_critic
    
    @tf.function
    def get_log_probability(self, logits, action):
        logprobabilities_all = tf.nn.log_softmax(logits)
        logprobability = tf.reduce_sum(
            tf.one_hot(action, cons.SIZE_ACTION_SPACES) * logprobabilities_all, axis= 1
        )
        return logprobability

    @tf.function
    def learning(self, index_game):
        print("=================================Learning===================================")
        observations, action_availables, actions, old_log_probs, old_values,\
            rewards, dones, index_players, batchs = self.memories[index_game].get_memory()
        #Cal advantages
        advantages = np.zeros((len(rewards,)))
        batch_size = len(rewards)
        for k in range(4):
            ids = []
            for i in range(batch_size):
                if(index_players[i] == k):
                    ids.append(i)
            ids.reverse()
            last_gae_lam = 0
            for i in range(1,len(ids),1):
                next_non_terminal = 1.0 - dones[ids[i]]
                next_value = old_values[ids[i - 1]]
                delta = rewards[ids[i]] + self.GAMMA * next_value * next_non_terminal - old_values[ids[i]]
                last_gae_lam = delta + self.GAMMA * self.LAM * next_non_terminal * last_gae_lam
                advantages[ids[i]] = last_gae_lam

        advantage_mean, advantage_std = (
            np.mean(advantages),
            np.std(advantages),
        )

        advantage_buffer = (advantages - advantage_mean) / advantage_std
        return_buffer = advantages + old_values

        advantage_buffer = tf.constant(advantage_buffer, dtype=tf.float32)
        for _ in range(self.N_EPOCHS):
            np.random.shuffle(batchs)
            for batch in batchs:
                observation = observations[batch]
                action_available = action_availables[batch]
                old_prob = old_log_probs[batch]
                old_value = old_values[batch]
                old_action = actions[batch]
                with tf.GradientTape() as tape:
                    tape.watch(self.actor.trainable_variables)
                    new_logits = self.actor(observation)
                    new_prob = self.get_log_probability(new_logits, old_action)

                    new_prob = tf.constant(new_prob, dtype=tf.float32)
                    old_prob = tf.constant(old_prob, dtype=tf.float32)

                    ratio = tf.exp(new_prob - old_prob) 
                    min_advantage = tf.where(
                        advantage_buffer[batch] > 0,
                        (1 + self.CLIP_RATIO) * advantage_buffer[batch],
                        (1 - self.CLIP_RATIO) * advantage_buffer[batch]
                    )
                    policy_loss = -tf.reduce_mean(
                        tf.minimum(ratio * advantage_buffer[batch], min_advantage)
                    )
                policy_grads = tape.gradient(policy_loss, self.actor.trainable_variables)
                self.action_optimizer.apply_gradients(zip(policy_grads, self.actor.trainable_variables))
                with tf.GradientTape() as tape:
                    tape.watch(self.critic.trainable_variables)
                    new_value = self.critic(observation)
                    value_loss = tf.reduce_mean((return_buffer - new_value) ** 2)
                value_grads = tape.gradient(value_loss, self.critic.trainable_variables)
                self.critic_optimizer.apply_gradients(zip(value_grads, self.critic.trainable_variables))
            #End batch
            # self.save_model()
            print(f"Epochs {_} game {index_game} End learning")
    
    def update(self):
        for index_game in range(self.N_GAMES):
            self.learning(index_game)

    def clear_memory(self):
        for mem in self.memories:
            mem.clear_memory()        


        





