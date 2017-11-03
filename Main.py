from collections import defaultdict
from random import sample
from time import time

import matplotlib.pyplot as plt
import numpy as np

from Simulations import create_mel_dist, create_f_pop, create_ballots, bm_majority_vote, reset_active_agents, \
    get_proxy_ranks, trans2bin
from config import *


def main():
    distanceTable = defaultdict(list)
    weightTable = defaultdict(list)
    counter = 1
    binary_truth = trans2bin(A, Truth)
    for n in range(2, N + 1):
        for run in range(Runs):
            create_mel_dist(binary_truth, PHI, distance)
            data = create_f_pop(PopSize, binary_truth, Mel)
            activeAgents = sample(data, n)
            for scenario in Scenarios:
                # If number of agents smaller than Vnearest append 0 and continue
                if scenario.upper() == 'V':
                    if n < Vnearest:
                        distanceTable[(n, scenario)] += []
                        continue
                reset_active_agents(data, scenario)
                ballots = create_ballots(data, activeAgents, scenario)
                result = bm_majority_vote(K, ballots)
                distanceTable[(n, scenario)] += [distance(result, binary_truth)]
                if scenario.upper() == 'P' and n == WN:
                    # currently saves the weight, the key is the number of the simulation
                    weightTable[('P', counter)] += get_proxy_ranks(activeAgents)
                elif scenario.upper() == 'V' and n == WN:
                    weightTable[('V', counter)] = get_proxy_ranks(activeAgents)
            counter += 1
        print 'Simulation number ', counter, ' Number of agents ', n + 1

    dist_table = {}
    wtable_P = [0] * WN
    wtable_V = [0] * WN
    # Creates the table dict, which contains the average distances from all the Runs (simulations),
    # if it's an empty list will add 'None' - for the V scenario
    for n, s in distanceTable:
        if distanceTable[(n, s)]:
            dist_table[(n, s)] = np.average(distanceTable[(n, s)])
        else:
            dist_table[(n, s)] = None

    for i in range(WN):
        for k in weightTable:
            if k[0] == 'P':
                wtable_P[i] += weightTable[k][i]
            else:
                wtable_V[i] += weightTable[k][i]
    for i in range(WN):
        wtable_V[i] = wtable_V[i] / float(Runs)
        wtable_P[i] = wtable_P[i] / float(Runs)

    # Creating an empty list for each scenario
    Blist, Plist, Vlist, Elist = [], [], [], []

    # Create list with the average distances for each scenario
    for i in range(2, N + 1):
        for scenario in Scenarios:
            if scenario.upper() == 'B':
                Blist.append(dist_table[(i, scenario)])
            elif scenario.upper() == 'P':
                Plist.append(dist_table[(i, scenario)])
            elif scenario.upper() == 'V':
                Vlist.append(dist_table[(i, scenario)])
            elif scenario.upper() == 'E':
                Elist.append(dist_table[(i, scenario)])

    index_a = np.arange(2, N + 1)
    # Define the current figure, all functions/commands will apply to the current figure
    plt.figure(1)
    avg_errors = []
    # Each plot function is a specific line (scenario)
    avg_errors.extend(plt.plot(index_a, Blist, color='b', linestyle='--', marker='o', markerfacecolor='b', label='B'))
    avg_errors.extend(plt.plot(index_a, Plist, color='m', linestyle='-.', marker='D', markerfacecolor='m', label='P'))
    avg_errors.extend(plt.plot(index_a, Vlist, color='c', linestyle=':', marker='p', markerfacecolor='c', label='V'))
    avg_errors.extend(plt.plot(index_a, Elist, color='g', linestyle='-', marker='s', markerfacecolor='g', label='E'))
    plt.setp(avg_errors, linewidth=2, markersize=5)

    plt.xlabel('Number of Active Agents')
    plt.ylabel('Avg Dist from T')
    plt.title(
        'Distance from the Truth with ' + str(Runs) + ' simulations \nPopulation size: ' + str(PopSize) + ' A=' + str(
            A) + ' PHI=' + str(PHI))
    plt.xticks(index_a, range(2, N + 1))
    # Legend Box appearance
    plt.legend(shadow=True, fancybox=True)
    # Auto layout design function
    plt.tight_layout()

    # Generates a unique image name
    figname = '.\Plots\Error'
    figname += 'K=' + str(K) + 'PHI=' + str(PHI) + 'V=' + str(Vnearest)
    figname += '-' + str(time())
    figname += '.png'
    # Saves the generated figures
    # plt.savefig(figname, dpi=400)
    # Closes the current figure
    # plt.close()

    # set a new current figure
    plt.figure(2)
    # Plotting the weights graphs
    index_b = np.arange(1, WN + 1)
    avg_weights = []
    avg_weights.extend(
        plt.plot(index_b, wtable_P, color='y', linestyle='-', marker='s', markerfacecolor='y', label='Proxy'))
    avg_weights.extend(
        plt.plot(index_b, wtable_V, color='r', linestyle='-', marker='s', markerfacecolor='r', label='Virtual Proxy'))
    plt.setp(avg_weights, linewidth=2, markersize=5)

    plt.xlabel('The rank of the Active agent')
    plt.ylabel('Average Weight')
    plt.title('The average weights of the proxies ' + str(Runs) + ' simulations \nPopulation size: ' + str(
        PopSize) + ' A= ' + str(A) + ' PHI= ' + str(PHI))
    plt.xticks(index_b, range(1, WN + 1))
    # Legend Box appearance
    plt.legend(shadow=True, fancybox=True)
    # Auto layout design function
    plt.tight_layout()

    # Generates a unique image name
    # figname = '.\Plots\Weights'
    # figname += 'K=' + str(K) + 'PHI=' + str(PHI)
    # figname += '-' + str(time())
    # figname += '.png'
    # Saves the generated figures
    # plt.savefig(figname, dpi=400)
    # Closes the current figure
    # plt.close()

    # The rendering function - shows the output on the screen
    plt.show()


if __name__ == '__main__':
    # for i in range(15):
    main()
