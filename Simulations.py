from itertools import permutations

from numpy.random import multinomial

# Library located at https://pypi.python.org/pypi/Distance/
from VotingAgent import VotingAgent
from config import *


# Creates the Mellows model distribution
# Mel {(index, vector): probability}
def create_mel_dist(t, phi, dist):
    a = permutations(t)
    for i, vec in enumerate(a):
        Mel[(i, vec)] = phi ** dist(t, vec)
    z = float(sum(Mel.values()))
    for i in Mel:
        Mel[i] = Mel[i] / z


# Creates the population profile
# returns a list of VotingAgent objects [VotingAgent, VotingAgent, ...]
def create_f_pop(f, dist):
    pop = []
    p = multinomial(f, dist.values())
    for i, vec in Mel:
        for j in range(p[i]):
            pop.append(VotingAgent(vec))
    return pop


# Creates the Voters profile according to the given Scenario
def create_ballots(pop, agents, s):
    for agent in agents:
        agent.isActive = True
    if s.upper() == 'B':
        ballots = agents
    elif s.upper() == 'P':
        ballots = assign_proxies(agents, pop)
    elif 'V' in s.upper():
        ballots = assign_virtual_proxies(agents, pop)
    else:
        for agent in pop:
            agent.isActive = True
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


def assign_virtual_proxies(proxies, pop):
    for agent in pop:
        if agent.isActive:
            continue
        agent.calc_dist_mat(proxies)
        agent.set_virtual_proxy()
    return pop


# returns a list of the weights of the proxies sorted by their distance from the truth 1st proxy is the closest
def get_proxy_ranks(proxies):
    weights = []
    for agent in sorted(proxies, key=lambda proxy: proxy.distance):
        weights.append(agent.weight)
    return weights


# Should run at the beginning of a simulation, an set the Agents variables to default values according to the scenario
def reset_active_agents(pop, s):
    if 'V' in s.upper():
        VotingAgent.virtual_scenario = True
    else:
        VotingAgent.virtual_scenario = False
    for agent in pop:
        agent.reset_agent()
