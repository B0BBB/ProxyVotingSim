from itertools import product
from time import time
from collections import OrderedDict
from numpy.random import multinomial
from random import sample, uniform, randint
# Library located at https://pypi.python.org/pypi/Distance/
from distance import hamming
from config import *


class VotingAgent:
    if 'V' in Scenario or 'v' in Scenario:
        virtual_scenario = True
    else:
        virtual_scenario = False

    def __init__(self, location):
        self.location = location
        self.isActive = False
        self.weight = 1
        self.distance = hamming(Truth, location)
        self.dist_mat = {}
        self.virtual_location = location
        self.proxy = None

    def calc_dist_mat(self, proxies):
        for i in proxies:
            self.dist_mat[i] = hamming(self.location, i) + uniform(0, 0.1)

    def set_proxy(self, v=virtual_scenario):
        assert not v, 'The scenario is Virtual, Virtual proxy should be calculated'
        self.proxy = min(self.dist_mat, key=self.dist_mat.get)
        print 'The chosen proxy is :', self.proxy

    def set_virtual_proxy(self, v=virtual_scenario):
        assert v, 'The scenario is not Virtual, regular proxy should be calculated'
        nearest_proxies = sorted(self.dist_mat, key=self.dist_mat.get)[-Vnearest:]
        for i in range(K):
            for j in nearest_proxies:
                self.virtual_location += nearest_proxies[j][i]
        for i, j in enumerate(self.virtual_location):
            if j > Vnearest/2:
                self.virtual_location[i] = 1
            elif j < Vnearest/2:
                self.virtual_location[i] = 0
            else:
                self.virtual_location[i] = randint(0, 1)
        print 'The virtual vote is: ', self.virtual_location

    def get_vote(self, v=virtual_scenario):
        if self.isActive:
            return self.location
        elif v:
            self.set_virtual_proxy()
            return self.virtual_location
        else:
            return self.proxy
