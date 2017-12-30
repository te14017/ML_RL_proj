#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# copyright (C) Team Kingslayer, University of Zurich, 2017.
"""
@author: Te Tan, Yves Steiner, Victoria Barth, Lihua Cao
"""

import random
from helpers import *
from environment import Environment


class Robot(object):
    """Robot Class"""

    def __init__(self, algo=1, multi_step=1):
        dealer_card, robot_card = Environment.dealCards()
        self.state = State(dealer_card, robot_card.value)
        """
        the algorithm robot uses to update Q value
        1 represents Q-learning(default), 2 represents Temporal-Different (SARSA or Multi-step)
        """
        self.algo = algo
        self.multi_step = multi_step # if the algo is TD, how many steps should be taken into account, 1 is SARSA
        self.q = {}  # stores Q values
        self.previous_states = []   # store previous states robot passed

        self.alpha = 0.9  # learning rate
        self.gamma = 1  # discount factor
        self.epsilon = 0.9999  # exploration rate
        self.explorations = 0  # counts number of explorations
        self.exploration_threshold = 3000   # exploration rate only decline after robot's exploration reach the threshold

        self.bust_penalty_below = -10  # penalty of bust below 1
        self.bust_penalty_above = -1   # penalty of bust above 21
        self.dealer_bust_reward = 10    # reward of dealer bust

    def __repr__(self):
        return "%s is @ %s. " % (self.__class__.__name__, self.state)

    def  doAction(self, explore=False):
        """ Let the robot perform his card play
        :return Action
        """
        # initialize possible action with q value 0
        available_qs = {
            (self.state, ACTION.hit): 0,
            (self.state, ACTION.stick): 0,
        }
        # search if there are q values for state action pair
        for state_action_pair in self.q:
            if self.state == state_action_pair[0]:
                available_qs[state_action_pair] = self.q[state_action_pair]

        biggest_reward = list(available_qs.values())[0]  # value for best possible options
        for reward in available_qs.values():
            if reward > biggest_reward:
                biggest_reward = reward

        go_on_exploration = random.uniform(0, 1) < self.epsilon  # determines whether the robot should explore or not
        # the exploration rate will only be decrease when the robot was already exploring for some time
        if self.explorations > self.exploration_threshold and not explore:
            if self.epsilon > 0:
                self.epsilon -= 0.01

        feasible_actions = []  # holds actions which the robot can choose from
        if not go_on_exploration:
            # robot does not explore
            for state_action_pair, reward in available_qs.items():
                if reward == biggest_reward:
                    feasible_actions.append(state_action_pair[1])
        else:
            # robot is going on randomly play
            self.explorations += 1
            for state_action_pair, reward in available_qs.items():
                    feasible_actions.append(state_action_pair[1])

        if len(feasible_actions) == 1:  # if the is only one, take it
            return feasible_actions[0]
        else:  # if there are multiple good actions to take the robot chooses randomly which to take
            choice = random.randint(0, len(feasible_actions) - 1)
            return feasible_actions[choice]

    def update(self, new_state, action, reward):
        """
        Updates the robot after getting feedback from environment
        :param new_state: robot's new State
        :param action: (Position, Movement) what the robot chose to do
        :return: nothing
        """
        self.previous_states.append((self.state, action, reward))
        self.state = new_state

    def updateQ(self, target_step, T, new_action):
        """
        Updates q values
        """
        # Q-learning update
        if self.algo == 1:
            state, action, reward = self.previous_states.pop()
            current_q = self.q.get((state, action), 0)
            value_list = []
            for state_action_pair, value in self.q.items():
                if self.state == state_action_pair[0]:
                    value_list.append(value)
            next_q = max(value_list) if value_list else 0

            new_q = current_q + self.alpha * (reward + self.gamma * next_q - current_q)
            self.q[(state, action)] = new_q
        else:
            # SARSA or Multi-step TD
            if target_step >= 0:
                target_state, target_action, reward = self.previous_states[target_step]
                current_q = self.q.get((target_state, target_action), 0)
                q_value = 0
                i = target_step
                upper = target_step + self.multi_step - 1 if (target_step + self.multi_step <= T) else T-1
                while i <= upper:
                    state, action, reward = self.previous_states[i]
                    # compute sum of discounted reward over steps
                    discount = i - target_step
                    q_value += self.gamma ** discount * reward
                    i += 1

                # add prospective Q value if not terminate
                if target_step + self.multi_step < T:
                    q_current_state = self.q.get((self.state, new_action), 0)
                    q_value += self.gamma ** self.multi_step * q_current_state

                new_q = current_q + self.alpha * (q_value - current_q)

                self.q[(target_state, target_action)] = new_q

    def reset(self):
        """Resets the robot to start without erasing the q values"""
        dealer_card, robot_card = Environment.dealCards()
        self.state = State(dealer_card, robot_card.value)
        self.previous_states = []

    def evaluate_robot(self):
        self.reset()
        runs = 5000
        wins = 0  # how many times robot win the game
        i = 1

        # firstly calculate the complete random play case
        self.epsilon = 1
        while i <= runs:
            terminate = False
            while not terminate:
                action = self.doAction(explore=True)
                newState, reward, terminate, dealer_final = Environment.doStep(self, action)
                self.update(new_state=newState, action=action, reward=reward)
            if reward >= 1:
                wins += 1
            self.reset()
            i += 1
        print("Winning rate of random play is: " + str(wins / runs))

        # then calculate the ideal play case
        wins = 0
        i = 1
        self.epsilon = 0  # set exploration rate to 0 to evaluate its Q-value quality
        while i <= runs:
            terminate = False
            while not terminate:
                action = self.doAction()
                newState, reward, terminate, dealer_final = Environment.doStep(self, action)
                self.update(new_state=newState, action=action, reward=reward)
            if reward >= 1:
                wins += 1

            self.reset()
            i += 1
        print("Winning rate of ideal play is: " + str(wins / runs))

