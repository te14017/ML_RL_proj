#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# copyright (C) Team Kingslayer, University of Zurich, 2017.
"""
@author: Te Tan, Yves Steiner, Victoria Barth, Lihua Cao
"""

from robot import *
from environment import Environment
import random
import math
import plotter

def main():
    # algo: 1 is Q-learning, 2 is TD
    # multi-step: when algo=2, if multi-step=1, then it's SARSA
    robot = Robot(algo=1, multi_step=1)
    i = 1
    n = 3000   # trials we want to run
    wins = 0
    random.seed(2016)

    while i <= n:
        t = 0
        T = math.inf    # record how many steps until terminate

        action = robot.doAction()
        while True:
            if t < T:
                newState, reward, terminate, dealer_final = Environment.doStep(robot, action)
                robot.update(new_state=newState, action=action, reward=reward)      # update robot state immediately
                if terminate:
                    T = t + 1
                    if reward == 1:
                        wins += 1
                else:
                    action = robot.doAction()   # update action for next step

            updated_step = t - robot.multi_step + 1     # this is the step whose Q-value will be updated in TD algorithm

            # update Q value of the robot
            robot.updateQ(target_step=updated_step, T=T, new_action=action)

            if updated_step == T - 1:
                break
            t += 1

        # pretty output that helps
        if n-i < 50:
            print("Trial %s: # steps: %d - %s. dealer's final: %d, Reward is: %d" % (i, T, robot, dealer_final, reward))

        robot.reset()
        i += 1
    print("size of robot's Q value dictionary: " + str(len(robot.q)))
    print("random exploration times: " + str(robot.explorations) + ", " + str(robot.epsilon))
    print("Winning rate: " + str(wins/n))
    print(robot.q)

    """Next evaluate robot's performance"""
    # robot.evaluate_robot()

    plotter.createplot(robot)

if __name__ == '__main__':
    main()
