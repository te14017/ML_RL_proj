#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# copyright (C) Team Kingslayer, University of Zurich, 2017.
"""
@author: Te Tan, Yves Steiner, Victoria Barth, Lihua Cao
"""

from helpers import *
import random


class Environment(object):
    """Environment"""

    def __init__(self):
        pass

    @staticmethod
    def drawOneCard():
        """
        randomly generate a card
        :return: Card
        """
        color_int = random.randint(1, 3)
        value_int = random.randint(1, 10)
        if color_int == 1:
            return Card(Card.COLOR.Red, value_int)
        else:
            return Card(Card.COLOR.Black, value_int)

    @staticmethod
    def dealCards():
        """
        start the game, give two black cards to dealer and robot respectively
        :return: Card, Card
        """
        # generate a black card for dealer
        while True:
            dealer_card = Environment.drawOneCard()
            if dealer_card.color == Card.COLOR.Black:
                break

        # generate a black card for robot
        while True:
            robot_card = Environment.drawOneCard()
            if robot_card.color == Card.COLOR.Black:
                break

        return dealer_card, robot_card


    @staticmethod
    def _is_bust(sum):
        """
        if sum is below 1, return -1, if sum is above 21 return 1, else return 0
        :param sum:
        :return:
        """
        if sum < 1:
            return -1
        elif sum > 21:
            return 1
        else:
            return 0

    @staticmethod
    def doStep(robot, action):
        """
        Performs the action of the player in the environment
        :param robot: dealer's first card number + player's current sum
        :param action: hits or stick, the player intend to do
        :return: newState: State, reward: int, terminate: boolean, dealer_sum: int
        """
        newState = State(robot.state.dealer_card, robot.state.robot_sum)
        reward = 0
        terminate = False
        dealer_final = robot.state.dealer_card.value    # dealer's final sum

        # if robot choose to hit, draw another card
        if action == ACTION.hit:
            card = Environment.drawOneCard()
            if card.color == Card.COLOR.Red:
                newState.robot_sum -= card.value
            else:
                newState.robot_sum += card.value
            # check if robot is bust(if is, below 1 or above 21)
            if Environment._is_bust(newState.robot_sum) == -1:
                reward = robot.bust_penalty_below
                terminate = True
            elif Environment._is_bust(newState.robot_sum) == 1:
                reward = robot.bust_penalty_above
                terminate = True

            return newState, reward, terminate, dealer_final

        # if robot choose to stick, dealer starts to draw cards and game ends
        else:
            # continue to draw cards until dealer's sum equal or bigger than 17
            terminate = True
            dealer_sum = dealer_final
            dealer_bust = False

            while dealer_sum < 17:
                card = Environment.drawOneCard()
                if card.color == Card.COLOR.Red:
                    dealer_sum -= card.value
                else:
                    dealer_sum += card.value
                # if dealer is bust, robot wins with reward
                if Environment._is_bust(dealer_sum) != 0:
                    dealer_bust = True
                    break

            if dealer_bust:
                reward = robot.dealer_bust_reward
            else:
                if newState.robot_sum > dealer_sum:
                    reward = 1
                elif newState.robot_sum < dealer_sum:
                    reward = -1
                else:
                    reward = 0

            return newState, reward, terminate, dealer_sum

