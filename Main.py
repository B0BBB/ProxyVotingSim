from time import time
from collections import defaultdict
from random import sample
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
            for scenario in Scenarios:
                # If number of agents smaller than Vnearest append 0 and continue
                if scenario.upper() == 'V':
                    if n < Vnearest:
                        distanceTable[(n, scenario)] += [0]
                        continue
                reset_active_agents(data, scenario)
                ballots = create_ballots(data, activeAgents, scenario)
                result = bm_majority_vote(ballots)
                distanceTable[(n, scenario)] += [hamming(result, Truth)]
            counter += 1
    with open('Test1.csv', 'w') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        fieldnames2 = ["Scenario", "Agents", "Avg dist"]
        writer.writerow(fieldnames2)
        for n, s in distanceTable:
            writer.writerow([n, s, np.average(distanceTable[(n, s)])])
    write_file.close()
    table = {}
    for n, s in distanceTable:
        table[(n, s)] = np.average(distanceTable[(n, s)])
    Blist, Plist, Vlist, Elist = [], [], [], []

    print distanceTable
    print table
    # Create list with the average distances for each scenario
    for i in range(1, N+1):
        for scenario in Scenarios:
            if scenario == 'B':
                Blist.append(table[(i, scenario)])
            elif scenario == 'P':
                Plist.append(table[(i, scenario)])
            elif scenario == 'V':
                Vlist.append(table[(i, scenario)])
            elif scenario == 'E':
                Elist.append(table[(i, scenario)])
    fig, ax = plt.subplots()
    index = np.arange(N)
    bar_width = 0.2

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index - bar_width * 2, Blist, bar_width,
                     alpha=opacity,
                     color='b',
                     # error_kw=error_config,
                     label='Basic')

    rects2 = plt.bar(index - bar_width , Plist, bar_width,
                     alpha=opacity,
                     color='r',
                     # error_kw=error_config,
                     label='Proxy')

    rects3 = plt.bar(index, Elist, bar_width,
                     alpha=opacity,
                     color='g',
                     # error_kw=error_config,
                     label='E scenario')

    rects4 = plt.bar(index + bar_width, Vlist, bar_width,
                     alpha=opacity,
                     color='purple',
                     # error_kw=error_config,
                     label='Virtual')
    # Empty bar - adds the spaces between the bars
    rects4 = plt.bar(index + bar_width * 2, [0]*N, bar_width,
                     alpha=opacity,
                     color='w',
                     # error_kw=error_config,
                     # label='Virtual'
                     )

    plt.xlabel('Agents')
    plt.ylabel('Dist from T')
    plt.title('Distance from the Truth with ' + str(Runs) + ' simulations \nPopulation size: ' + str(PopSize))
    plt.xticks(index - bar_width / 2, range(1, N + 1))
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
