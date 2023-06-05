import random
import numpy as np
import pandas as pd
from operator import add
import collections
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import copy
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop


class Agent:
    def __init__(self, agent):
        self.reward = 0
        self.state = 0
        self.action = 0
        self.gamma = 0.975
        self.epsilon = 1
        self.agent = agent


    def get_state(self):
        state = np.zeros((5,1))

        state[0, 0] = torch.getQlength()
        state[1, 0] = torch.getQlength()
        state[2, 0] = torch.getQlength()
        state[3, 0] = torch.getQlength()

        state[4, 0] = self.agent.getTLSphase()

        return state

    def get_reward(state):
        qLengths = state[:4]
        reward = (-1) * np.sum(qLengths) * np.std(qLengths)

        return reward

    # TODO code a function that inputs into the game object, every possible configuration
    def play_game(self):
        model = Sequential()
        model.add(Dense(164, kernel_initializer='lecun_uniform', input_shape=(5,)))
        model.add(Activation('relu'))
        # model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

        model.add(Dense(150, kernel_initializer='lecun_uniform'))
        model.add(Activation('relu'))
        # model.add(Dropout(0.2))

        model.add(Dense(2, kernel_initializer='lecun_uniform'))
        model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)
        model.predict(self.state.reshape(1, 5), batch_size=1)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Train the DQN agent on the <state, action, reward, next_state, is_done>
        tuple at the current timestep.
        """
        self.train()
        torch.set_grad_enabled(True)
        target = reward
        next_state_tensor = torch.tensor(next_state.reshape((1, 11)), dtype=torch.float32).to(DEVICE)
        state_tensor = torch.tensor(state.reshape((1, 11)), dtype=torch.float32, requires_grad=True).to(DEVICE)
        if not done:
            target = reward + self.gamma * torch.max(self.forward(next_state_tensor[0]))
        output = self.forward(state_tensor)
        target_f = output.clone()
        target_f[0][np.argmax(action)] = target
        target_f.detach()
        self.optimizer.zero_grad()
        loss = F.mse_loss(output, target_f)
        loss.backward()
        self.optimizer.step()


    # TODO a function that reads in the previous state and calculates the q score
    # TODO should this function do reinforced or unreinforced ML
    def calc_loss(self, memory):
        X_train = []
        y_train = []
        old_state, action, reward, new_state = memory
        old_qval = self.predict(old_state.reshape(1, 5), batch_size=1)
        newQ = self.predict(new_state.reshape(1, 5), batch_size=1)
        maxQ = np.max(newQ)
        y = np.zeros((1, 2))
        y[:] = old_qval[:]
        update = (reward + (self.gamma * maxQ))
        y[0][action] = update
        X_train.append(old_state.reshape(5, ))
        y_train.append(y.reshape(2, ))
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        return X_train, y_train

def run(params):
    agent = Agent(params)
    agent.play_game()
    # TODO edit play the game for as long as you want
    while (True):
        agent.save_config()
        agent.calc_loss()

        state_old = agent.get_state(engineer, food1)

        # perform random actions based on agent.epsilon, or choose the action
        if random.uniform(0, 1) < agent.epsilon:
            final_move = np.eye(3)[randint(0, 2)]
        else:
            # predict action based on the old state
            with torch.no_grad():
                state_old_tensor = torch.tensor(state_old.reshape((1, 11)), dtype=torch.float32).to(DEVICE)
                prediction = agent(state_old_tensor)
                final_move = np.eye(3)[np.argmax(prediction.detach().cpu().numpy()[0])]

        # perform new move and get new state
        engineer.configure_roads(final_move, game, food1, agent)
        state_new = agent.get_state(game, player1, food1)

        # set reward for the new state
        reward = agent.set_reward(engineer, game.crash)

        if params['train']:
            # train short memory base on the new action and state
            agent.train_short_memory(state_old, final_move, reward, state_new, game.crash)
            # store the new data into a long term memory
            agent.remember(state_old, final_move, reward, state_new, game.crash)

if __name__ == '__main__':
    run()
