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
def create_ballots(pop, agents, s):
    for agent in agents:
        agent.isActive = True
    if s == 'B' or s == 'b':
        ballots = agents
    elif s == 'P' or s == 'p':
        ballots = assign_proxies(agents, pop)
    elif 'V' in s or 'v' in s:
        print 'Scenario P + V'
        proxies = sample(pop, n)
        ballots = create_virtual(proxies, pop)
    else:
        ballots = pop
    return ballots


# This will calculate the weight for each proxy
def assign_proxies(proxies, pop):
    for agent in pop:
        agent.calc_dist_mat(proxies)
        agent.set_proxy()
    voters = []
    for prox in proxies:
        voters += [prox] * prox.weight
    return voters


def reset_active_agents(agents):
    for agent in agents:
        agent.weight = 1
        agent.isActive = False
