#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# copyright (C) Team Kingslayer, University of Zurich, 2017.
"""
@author: Te Tan, Yves Steiner, Victoria Barth, Lihua Cao
"""

import helpers
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def removebykey(d, key):
    """
          Removes unwanted entries in the dictionary by key.
          :param d: dictionary
          :param key: key of dictionary entry to be removed
          :return: new dictionary with removed entry
          """
    r = dict(d)
    del r[key]
    return r


def removebyaction(d, a):
    """
          Removes unwanted entries in the dictionary by the action: hit or stick.
          :param d: dictionary
          :param a: the action defined in the helper class e.g. ACTION.stick
          :return: d: new dictionary with removed entry
          :return: str: name of action taken
          """
    # itterates over dictionary and calls function removebykey if action is e.g. stick
    for key in d:
        # tmp = {(key[0], ACTION.hit): robot.q.get((key[0], ACTION.hit), 0),
        #     (key[0], ACTION.stick): robot.q.get((key[0], ACTION.stick), 0)}
        # minkey = min(tmp.keys(), key=(lambda key: tmp[key]))
        # if minkey in plotq:
        #     plotq = removekey(plotq,minkey)
        if key[1] == a:
            d = removebykey(d, key)
    return d, 'removed_'+a.name

def removeminqval(d):
    """
          Removes smaller q value of either: hit or stick.
          :param d: dictionary
          :return: d: new dictionary with removed entries
          :return: str: name of action taken
          """
    # itterates over dictionary and calls function removebykey if action is e.g. stick
    for key in d:
        tmp = {(key[0], helpers.ACTION.hit): d.get((key[0], helpers.ACTION.hit), 0),
               (key[0], helpers.ACTION.stick): d.get((key[0], helpers.ACTION.stick), 0)}
        minkey = min(tmp.keys(), key=(lambda key: tmp[key]))
        if minkey in d:
            d = removebykey(d, minkey)
    return d, 'removed_q_min'

def removeminqval(d):
    """
          Removes smaller q value of either: hit or stick.
          :param d: dictionary
          :return: d: new dictionary with removed entries
          :return: str: name of action taken
          """
    # itterates over dictionary and calls function removebykey if action is e.g. stick
    for key in d:
        tmp = {(key[0], helpers.ACTION.hit): d.get((key[0], helpers.ACTION.hit), 0),
               (key[0], helpers.ACTION.stick): d.get((key[0], helpers.ACTION.stick), 0)}
        minkey = min(tmp.keys(), key=(lambda key: tmp[key]))
        if minkey in d:
            d = removebykey(d, minkey)
    return d, 'removed_q_min'

def subtractactions(d):
    """
          Returns a directory where the q-values of the hit and stick actions in the same state get subtracted.
          :param d: dictionary
          :return: tdir: new dictionary with subtracted q-values
          :return: str: name of action taken
          """
    tdir = {}
    for key in d:
        new_q = d.get((key[0], helpers.ACTION.hit),0)-d.get((key[0], helpers.ACTION.stick),0)
        if (key[0], helpers.ACTION.hit) not in tdir:
            tdir[(key[0], helpers.ACTION.hit)] = new_q
    return tdir, 'subtracted_hit_stick'

def getalgoname(a, ms):
    '''
    Returns the algorithms name.
    :param a: algorithm number of the robot.
    :param ms: multistep number of the robot.
    :return: The name of the algorithm.
    '''
    if a == 1 and ms == 1:
        t = 'Q-Learning'
    elif a == 2 and ms == 1:
        t = 'SALASA'
    else:
        t = 'Multistep'
    return t

def createplot(robot):
    """
       Creates a 3d plot of the q-value dictionary compiled by the learning function of the robot.
       The dealer's initial state on the x-axis, the robot/player's sum on the y-axis
       and the q-value of the corresponding situation on the z-axis
       :param robot: robot compiled by the reinforcement learning algorithm
       :return: nothing - image is stored in the output directory
       """
    #plotq = robot.q

    #plotq, valuehandling = removebyaction(robot.q, helpers.ACTION.stick)
    #plotq, valuehandling = removeminqval(robot.q)
    plotq, valuehandling = subtractactions(robot.q)

    # initializing arrays for the axis
    X = np.arange(0, 11, 1)
    Y = np.arange(0, 22, 1)
    Z = np.zeros((11, 22))

    # extracting the q-values from the dictionary and store it
    # in the two dimensional array for the z-axis
    zmax = -10
    for key in plotq:
        i = key[0].dealer_card.value
        j = key[0].robot_sum
        qval = plotq[key]
        Z[i][j] = qval
        zmax = max(zmax, qval)

    # defining the mesh
    X, Y = np.meshgrid(X, Y)
    zs = np.array(Z)
    Z = zs.reshape(X.shape)

    # retreiving the name of the algorithm
    title = getalgoname(robot.algo, robot.multi_step)

    # defining the figure
    fig = plt.figure()
    fig.suptitle(title, fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.winter, linewidth=0, antialiased=True)

    ax.set_xlabel('Dealer showing')
    ax.set_ylabel('Player sum')
    ax.set_zlabel('Q-Value')
    # sets range of axis
    #ax.set_zlim(0, max(zmax+1,10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 21)
    # removes decimal points on x-axis which are automatically generated
    ax.get_yaxis().set_major_formatter(
        tic.FuncFormatter(lambda Y, p: format(int(Y), ',')))

    #plt.show()
    # stores the figure as png in the output directory
    plt.savefig('output/'+title+'_'+ valuehandling+'.png')
    print('Figure for '+title+' has been stored in the output directory.')

def create2dplot(robot, dealerval):
    """
       Creates a 2d plot of the q-value dictionary compiled by the learning function of the robot.
       One dealer initial state is picked, all the robot/player's sums and q-values corresponding
       to that initial state are printed
       :param robot: robot compiled by the reinforcement learning algorithm
       :param dealerval: the value of the dealer to be used for printing
       :return: nothing - image is stored in the output directory
       """

    plotq = robot.q

    # defining the y-axis
    X = np.arange(0, 22, 1)
    Yh = np.zeros(22)
    Ys = np.zeros(22)

    zmax = -10
    # extracting the q-values and store it in a y-axis array for hit or stick
    for key in plotq:
        if key[0].dealer_card.value == dealerval:
            j = key[0].robot_sum
            qval = plotq[key]
            if key[1] == helpers.ACTION.hit:
                Yh[j] = qval
            else:
                Ys[j] = qval
            zmax = max(zmax, qval)

    Yh = np.array(Yh)
    Ys = np.array(Ys)

    # retreiving the name of the algorithm
    title = getalgoname(robot.algo, robot.multi_step)
    valuehandling = '2d_plot_dealer_'+ str(dealerval)

    # defining the figure with title and subtitle
    fig = plt.figure()
    fig.suptitle(title, fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_title('Dealer\'s initial card ' + str(dealerval))

    # First plot stick
    plt.plot(X, Ys, label='Stick', color='red')

    # Second plot hit
    plt.plot(X, Yh, label='Hit', color='lightblue')

    plt.xlabel('Player sum')
    plt.ylabel('Q-Value')
    plt.legend()

    ax.set_xlim(1, 21)
    plt.xticks(np.arange(1, max(X) + 1, 1.0))

    #plt.show()
    # stores the figure as png in the output directory
    plt.savefig('output/' + title + '_' + valuehandling + '.png')
    print('Figure for ' + title + ' has been stored in the output directory.')