#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# copyright (C) Team Kingslayer, University of Zurich, 2017.
"""
@author: Te Tan, Yves Steiner, Victoria Barth, Lihua Cao
"""

from enum import Enum


class Card(object):
    """
    color and value of the card
    if the color is red, value contributes negatively to the sum,
    if the color is black, value contributes positively to the sum
    """
    COLOR = Enum('COLOR', ('Red', 'Black'))

    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def __repr__(self):
        return "%s (%d,%d)" % (self.__class__.__name__, self.color, self.value)

    def __cmp__(self, other):
        if self.color == other.color:
            if self.value == other.value:
                return 0
            elif self.value < other.value:
                return -1
            else:
                return 1
        elif self.color == Card.COLOR.Red:
            return -1
        else:
            return 1

    def __gt__(self, other):
        if self.color == other.color:
            return self.value > other.value
        elif self.color == Card.COLOR.Black:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.color, self.value))


class State(object):
    """
    dealer's initial card and robot's current sum of values
    """

    def __init__(self, dealer_card, robot_sum):
        self.dealer_card = dealer_card
        self.robot_sum = robot_sum

    def __eq__(self, other):
        return self.dealer_card == other.dealer_card and self.robot_sum == other.robot_sum

    def __repr__(self):
        return "%s (dealer's initial: %d, robot's sum: %d)" % (self.__class__.__name__, self.dealer_card.value, self.robot_sum)

    def __hash__(self):
        return hash((self.dealer_card, self.robot_sum))

    def __cmp__(self, other):
        if self.dealer_card < other.dealer_card:
            return -1
        elif self.dealer_card > other.dealer_card:
            return 1
        else:
            if self.robot_sum == other.robot_sum:
                return 0
            elif self.robot_sum < other.robot_sum:
                return -1
            else:
                return 1

    def __gt__(self, other):
        return self.dealer_card > other.dealer_card and self.robot_sum > other.robot_sum

# actions the robot able to perform
ACTION = Enum('ACTION', ('hit', 'stick'))