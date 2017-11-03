from itertools import permutations, combinations
from random import randint

from numpy.random import multinomial


from VotingAgent import VotingAgent
from config import Mel, A


# Creates the Mellows model distribution
# Mel {(index, vector): probability}
def create_mel_dist(t, phi, dist):
    l = permutations(range(A))
    temp = []
    for vec in l:
        temp.append(trans2bin(A, vec))
    for i, vec in enumerate(temp):
        Mel[(i, vec)] = phi ** dist(t, vec)
    z = float(sum(Mel.values()))
    for i in Mel:
        Mel[i] = Mel[i] / z


# A transformation of an ordinal vector to a binary vector, in reference to T vector
def trans2bin(A, v):
    pairs = combinations(range(A), 2)
    result = []
    for x, y in pairs:
        a = v.index(y) - v.index(x)
        if a < 0:
            result.append(1)
        else:
            result.append(0)
    return tuple(result)


# Kendell's Tao distance between vector A and B
def kendall_tau(v, u):
    pairs = combinations(v, 2)
    dist = 0
    for x, y in pairs:
        a = v.index(x) - v.index(y)
        b = u.index(x) - u.index(y)
        # if discordant (different signs)
        if a * b < 0:
            dist += 1
    return dist


# Creates the population profile
# returns a list of VotingAgent objects [VotingAgent, VotingAgent, ...]
def create_f_pop(f, t, dist):
    pop = []
    p = multinomial(f, dist.values())
    for i, vec in Mel:
        for j in range(p[i]):
            pop.append(VotingAgent(vec, t))
    return pop


# Boyer Moore majority vote algorithm, tie will be {0,1} randomly
# returns a single vector {0,1} of size k
def bm_majority_vote(k, ballots):
    result = []
    for i in range(k):
        m = None
        count = 0
        for agent in ballots:
            if count == 0:
                m = agent.get_vote()[i]
                count = 1
            elif m == agent.get_vote()[i]:
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
