from time import time
from collections import defaultdict
from random import sample
import csv
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
    counter = 1
    for n in range(1, N + 1):
        for run in range(Runs):
            activeAgents = sample(data, n)
            print 'Simulation number ', counter
            for scenario in Scenario:
                reset_active_agents(data, scenario)
                ballots = create_ballots(data, activeAgents, scenario)
                result = bm_majority_vote(ballots)
                distanceTable[(scenario, n)] += [hamming(result, Truth)]
            counter += 1
                # print 'Scenario ', scenario, 'result :', hamming(result, Truth)
    # for scenario, n in distanceTable:
    #     print 'the average distance for ', scenario, 'with', n, 'agents' , 'is ', float(sum(distanceTable[(scenario, n)])) / float(len(distanceTable[(scenario, n)]))

    with open('Test1.csv', 'w') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        fieldnames2 = ["Scenario", "Agents", "Avg dist"]
        writer.writerow(fieldnames2)
        for s, n in distanceTable:
            writer.writerow([s, n, float(sum(distanceTable[(s, n)])) / float(len(distanceTable[(s, n)]))])
    write_file.close()


if __name__ == '__main__':
    main()
