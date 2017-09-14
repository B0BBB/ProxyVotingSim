from time import time
from collections import defaultdict
from random import sample
# Library located at https://pypi.python.org/pypi/Distance/
from distance import hamming
import VotingAgent
from Simulations import create_mel_dist, create_f_pop, create_ballots, bm_majority_vote, reset_active_agents
from config import *


def main():
    print 'Creating Data Set'
    create_mel_dist(Truth, PHI, hamming, K)
    data = create_f_pop(PopSize, Mel)
    distanceTable = defaultdict(list)
    for run in range(Runs):
        activeAgents = sample(data, N)
        print 'Simulation number ', run + 1
        for scenario in Scenario:
            ballots = create_ballots(data, activeAgents, scenario)
            result = bm_majority_vote(ballots)
            distanceTable[scenario] += [hamming(result, Truth)]
            reset_active_agents(activeAgents)
            # print 'Scenario ', scenario, 'result :', hamming(result, Truth)
    for scenario in Scenario:
        print 'the average distance for ', scenario, 'is ', float(sum(distanceTable[scenario])) / float(
            len(distanceTable[scenario]))


if __name__ == '__main__':
    main()
