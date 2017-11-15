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

    def __init__(self):
        dealer_card, robot_card = Environment.dealCards()
        self.state = State(dealer_card, robot_card.value)
        self.q = {}  # stores Q values
        self.previous_states = []   # store previous states robot passed

        self.alpha = 0.9  # learning rate
        self.gamma = 1  # discount factor
        self.epsilon = 0.9999  # exploration rate
        self.explorations = 0  # counts number of explorations
        self.exploration_threshold = 800
        self.bust_penalty_below = -1  # penalty of bust below 1
        self.bust_penalty_above = -1   # penalty of bust above 21
        self.dealer_bust_reward = 1    # reward of dealer bust

    def __repr__(self):
        return "%s is @ %s. " % (self.__class__.__name__, self.state)

    def doAction(self):
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
        if self.explorations > self.exploration_threshold:
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
        :param reward: reward robot gets
        :return: nothing
        """
        self._updateQ(state=new_state, action=action, reward=reward)
        self.previous_states.append(self.state)
        self.state = new_state

    def _updateQ(self, state, action, reward):
        """
        Updates all q values
        :param state: robot's new State
        :param action: hit or stick the robot choose to do
        :param reward: reward robot gets
        :return: nothing
        """
        current_q = self.q.get((self.state, action), 0)
        value_list = []
        for state_action_pair, value in self.q.items():
            if state == state_action_pair[0]:
                value_list.append(value)
        next_q = max(value_list) if value_list else 0

        new_q = current_q + self.alpha * (reward + self.gamma * next_q - current_q)

        self.q[(self.state, action)] = new_q

    def reset(self):
        """Resets the robot to start without erasing the q values"""
        dealer_card, robot_card = Environment.dealCards()
        self.state = State(dealer_card, robot_card.value)

