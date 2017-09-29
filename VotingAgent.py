from itertools import product
from time import time
from collections import OrderedDict
from numpy.random import multinomial
from random import sample, uniform, randint
# Library located at https://pypi.python.org/pypi/Distance/
from distance import hamming
from config import *


class VotingAgent:
    virtual_scenario = None
    # TODO: give a unique ID to every agent
    def __init__(self, location):
        self.location = location
        self.isActive = False
        self.weight = 1
        self.distance = hamming(Truth, location)
        self.dist_mat = {}
        self.virtual_location = []
        self.proxy = None

    def calc_dist_mat(self, proxies):
        for i in proxies:
            self.dist_mat[i] = hamming(self.location, i.location) + uniform(0, 0.1)

    def set_proxy(self, v=virtual_scenario):
        assert not v, 'The scenario is Virtual, Virtual proxy should be calculated'
        if self.isActive:
            # self.proxy = self.location
            # print 'This is a proxy', self, 'location: ', self.location
            return
        self.proxy = min(self.dist_mat, key=self.dist_mat.get)
        self.proxy.weight += 1
        # print 'The chosen proxy is :', self.proxy, 'location: ', self.proxy.location

    def set_virtual_proxy(self):
        assert VotingAgent.virtual_scenario, 'The scenario is not Virtual, regular proxy should be calculated'
        assert self.dist_mat, 'Proxies distances matrix is empty'
        # TODO: add 1/Vnearest to the weight of the selected proxy
        nearest_proxies = sorted(self.dist_mat, key=self.dist_mat.get)[:Vnearest]
        templist = []
        for i in range(K):
            templist.insert(i, 0)
            for j in nearest_proxies:
                templist[i] += j.location[i]
        for i, j in enumerate(templist):
            if j > Vnearest/2.0:
                self.virtual_location.insert(i, 1)
            elif j < Vnearest/2.0:
                self.virtual_location.insert(i, 0)
            else:
                self.virtual_location.insert(i, randint(0, 1))

    def get_vote(self):
        if self.isActive:
            return self.location
        elif VotingAgent.virtual_scenario:
            return self.virtual_location
        else:
            return self.proxy.location

    def reset_agent(self):
        self.isActive = False
        self.weight = 1
        self.dist_mat = {}
        self.virtual_location = []
        self.proxy = None
