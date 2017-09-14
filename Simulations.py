from itertools import product
from time import time
from numpy.random import multinomial
from random import sample, uniform, randint
# Library located at https://pypi.python.org/pypi/Distance/
from distance import hamming
from VotingAgent import VotingAgent
from config import *


# Creates the Mellows model distribution
# Mel {(index, vector): probability}
def create_mel_dist(t, phi, dist, k):
    a = product(range(2), repeat=k)
    for i, vec in enumerate(a):
        Mel[(i, vec)] = phi ** dist(t, vec)
    z = float(sum(Mel.values()))
    for i in Mel:
        Mel[i] = Mel[i] / z


# Creates the population profile
# returns a list of tuples [(),(), ... ,()]
def create_f_pop(f, dist):
    pop = []
    p = multinomial(f, dist.values())
    for i, vec in Mel:
        for j in range(p[i]):
            pop.append(VotingAgent(vec))
    return pop


# Boyer Moore majority vote algorithm, tie will be {0,1} randomly
# returns a single vector {0,1} of size k
def bm_majority_vote(ballots):
    result = []
    for i in range(K):
        m = None
        count = 0
        for agent in ballots:
            if count == 0:
                m = agent.location[i]
                count = 1
            elif m == agent.location[i]:
                count += 1
            else:
                count -= 1
        if count > 0:
            result.append(m)
        elif count < 0:
            result.append(abs(1 - m))
        else:
            result.append(randint(0, 1))
    return result


# Creates the Voters profile according to the given Scenario
def create_active_voters(pop, n, s):
    # Sample N votes from the population
    if s == 'B' or s == 'b':
        print 'Scenario B'
        voters = sample(pop, n)
    # Sample N active + (PopSize - N) proxy weights
    elif s == 'P' or s == 'p':
        print 'Scenario P'
        proxies = sample(pop, n)
        voters = assign_proxies(proxies, pop)
    elif 'V' in s or 'v' in s:
        print 'Scenario P + V'
        proxies = sample(pop, n)
        voters = create_virtual(proxies, pop)
    else:
        print 'Scenario E'
        voters = pop
    return voters


# This will calculate the weight for each proxy
# TODO: need to improve the weight calculation performance - consider using a dictionary for the repeating agents
# TODO: The problem is that all agents with same profile will choose the same proxy
def assign_proxies(prox, pop):
    newproxies = {i: 0 for i in prox}
    popdict = {}
    for i in pop:
        popdict[i] = [prox[0], hamming(i, prox[0]) + uniform(-0.1, 0.1)]
        for j in prox:
            if popdict[i][1] > hamming(i, j):
                popdict[i] = [j, hamming(i, j) + uniform(-0.1, 0.1)]
        newproxies[popdict[i][0]] += 1
    assert sum(newproxies.values()) == PopSize, 'The weights of the proxies incorrect'
    print newproxies
    voters = []
    for i in newproxies:
        voters.extend([i] * newproxies[i])
    return voters
