from random import uniform, randint

from utils import borda_voting_rule
from config import *


class VotingAgent:
    virtual_scenario = None

    def __init__(self, location):
        self.location = location
        self.isActive = False
        self.weight = 1
        self.distance = distance(Truth, location) + uniform(0, 0.1)
        self.dist_mat = {}
        self.virtual_location = []
        self.proxy = None

    # Creates a matrix with the distances from self to each proxy - with addition of some noise for random tie breaking
    def calc_dist_mat(self, proxies):
        for i in proxies:
            self.dist_mat[i] = distance(self.location, i.location) + uniform(0, 0.1)

    # Sets the proxy with the minimal distance using the distances matrix
    def set_proxy(self, v=virtual_scenario):
        assert not v, 'The scenario is Virtual, Virtual proxy should be calculated'
        if self.isActive:
            return
        self.proxy = min(self.dist_mat, key=self.dist_mat.get)
        self.proxy.weight += 1

    # Sets the virtual location using the distance matrix
    def set_virtual_proxy(self):
        assert VotingAgent.virtual_scenario, 'The scenario is not Virtual, regular proxy should be calculated'
        if self.isActive:
            return
        assert self.dist_mat, 'Proxies distances matrix is empty'
        nearest_proxies = sorted(self.dist_mat, key=self.dist_mat.get)[:Vnearest]
        for proxy in nearest_proxies:
            proxy.weight += float(1) / Vnearest
        self.virtual_location = borda_voting_rule(nearest_proxies, A)

    # Returns the vote vector according to the scenario
    def get_vote(self):
        if self.isActive:
            return self.location
        elif VotingAgent.virtual_scenario:
            return self.virtual_location
        else:
            return self.proxy.location

    # Resets agents attributes
    def reset_agent(self):
        self.isActive = False
        self.weight = 1
        self.dist_mat = {}
        self.virtual_location = []
        self.proxy = None
