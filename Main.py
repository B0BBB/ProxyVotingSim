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
            for scenario in Scenario:
                reset_active_agents(data, scenario)
                ballots = create_ballots(data, activeAgents, scenario)
                result = bm_majority_vote(ballots)
                distanceTable[(n, scenario)] += [hamming(result, Truth)]
            counter += 1
            # print 'Scenario ', scenario, 'result :', hamming(result, Truth)
    # for scenario, n in distanceTable:
    #     print 'the average distance for ', scenario, 'with', n, 'agents' , 'is ', float(sum(distanceTable[(scenario, n)])) / float(len(distanceTable[(scenario, n)]))
    with open('Test1.csv', 'w') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        fieldnames2 = ["Scenario", "Agents", "Avg dist"]
        writer.writerow(fieldnames2)
        for n, s in distanceTable:
            writer.writerow([n, s, float(sum(distanceTable[(n, s)])) / float(len(distanceTable[(n, s)]))])
    write_file.close()
    Blist = [0] * N
    Plist = [0] * N
    Vlist = [0] * N
    Elist = [0] * N
    agents = range(1, N + 1)

    for i in distanceTable:
        if i[1] == 'B':
            Blist[i[0]-1] = distanceTable[i][0]
        elif i[1] == 'P':
            Plist[i[0] - 1] = distanceTable[i][0]
        elif i[1] == 'V':
            Vlist[i[0] - 1] = distanceTable[i][0]
        elif i[1] == 'E':
            Elist[i[0] - 1] = distanceTable[i][0]
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
    rects4 = plt.bar(index + bar_width * 2, [0]*N, bar_width,
                     alpha=opacity,
                     color='w',
                     # error_kw=error_config,
                     # label='Virtual'
                     )

    plt.xlabel('Agents')
    plt.ylabel('Dist from T')
    plt.title('Distance from the Truth with ' + str(Runs) + ' simulations')
    plt.xticks(index - bar_width / 2, range(1, N + 1))
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
