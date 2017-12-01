#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# copyright (C) Team Kingslayer, University of Zurich, 2017.
"""
@author: Te Tan, Yves Steiner, Victoria Barth, Lihua Cao
"""

from robot import *
from environment import Environment
import random


def main():
    robot = Robot()
    i = 1
    n = 3000   # trials we want to run
    random.seed(2016)
    while i <= n:
        terminate = False
        steps = 0
        while not terminate:
            action = robot.doAction()
            newState, reward, terminate, dealer_final = Environment.doStep(robot, action)
            robot.update(new_state=newState, action=action, reward=reward)
            steps += 1

        # pretty output that helps
        if n-i < 50:
            print("Trial %s: # steps: %d - %s. dealer's final: %d, Reward is: %d" % (i, steps, robot, dealer_final, reward))

        robot.reset()
        i += 1
    print("size of robot's Q value dictionary: " + str(len(robot.q)))
    print("random exploration times: " + str(robot.explorations) + ", " + str(robot.epsilon))
    # print(robot.q)

    """Next evaluate robot's performance"""
    robot.evaluate_robot()


if __name__ == '__main__':
    main()
