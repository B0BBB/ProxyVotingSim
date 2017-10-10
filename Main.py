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
                        distanceTable[(n, scenario)] += []
                        continue
                reset_active_agents(data, scenario)
                ballots = create_ballots(data, activeAgents, scenario)
                result = bm_majority_vote(ballots)
                distanceTable[(n, scenario)] += [hamming(result, Truth)]
            counter += 1

    table = {}
    # Creates the table dict, which contains the average distances from all the Runs (simulations),
    # if it's an empty list will add 'None' - for the V scenario
    for n, s in distanceTable:
        if distanceTable[(n, s)]:
            table[(n, s)] = np.average(distanceTable[(n, s)])
        else:
            table[(n, s)] = None

    # Creating an empty list for each scenario
    Blist, Plist, Vlist, Elist = [], [], [], []

    print distanceTable
    print table

    # Create list with the average distances for each scenario
    for i in range(1, N + 1):
        for scenario in Scenarios:
            if scenario.upper() == 'B':
                Blist.append(table[(i, scenario)])
            elif scenario.upper() == 'P':
                Plist.append(table[(i, scenario)])
            elif scenario.upper() == 'V':
                Vlist.append(table[(i, scenario)])
            elif scenario.upper() == 'E':
                Elist.append(table[(i, scenario)])

    index = np.arange(N)
    # Each plot function is a specific line (scenario)
    plt.plot(index, Blist, color='b', linestyle='--', linewidth=2, marker='o', markerfacecolor='b',
             markersize=3, label='B')
    plt.plot(index, Plist, color='m', linestyle='-.', linewidth=2, marker='D', markerfacecolor='m',
             markersize=3, label='P')
    plt.plot(index, Vlist, color='c', linestyle=':', linewidth=2, marker='p', markerfacecolor='c',
             markersize=5, label='V')
    plt.plot(index, Elist, color='g', linestyle='-', linewidth=2, marker='s', markerfacecolor='g',
             markersize=5, label='E')

    plt.xlabel('Number of Agents')
    plt.ylabel('Avg Dist from T')
    plt.title('Distance from the Truth with ' + str(Runs) + ' simulations \nPopulation size: ' + str(PopSize))
    plt.xticks(index, range(1, N + 1))
    # Legend Box appearance
    plt.legend(shadow=True, fancybox=True)
    # Auto layout design function
    plt.tight_layout()
    # The rendering function - shows the output on the screen
    plt.show()


if __name__ == '__main__':
    main()
