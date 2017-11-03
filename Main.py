from collections import defaultdict
from random import sample

import matplotlib.pyplot as plt
import numpy as np

# Library located at https://pypi.python.org/pypi/Distance/
from Simulations import create_mel_dist, create_f_pop, create_ballots, reset_active_agents, \
    get_proxy_ranks
from utils import borda_voting_rule
from config import *


def main():
    print 'Creating Data Set'

    distance_table = defaultdict(list)
    weight_table = defaultdict(list)
    counter = 1
    create_mel_dist(Truth, PHI, distance)
    data = create_f_pop(PopSize, Mel)
    for n in range(2, N + 1):
        for run in range(Runs):
            active_agents = sample(data, n)
            for scenario in Scenarios:
                # If number of agents smaller than Vnearest append 0 and continue
                if scenario.upper() == 'V':
                    if n < Vnearest:
                        distance_table[(n, scenario)] += []
                        continue
                reset_active_agents(data, scenario)
                ballots = create_ballots(data, active_agents, scenario)
                result = borda_voting_rule(ballots, A)
                distance_table[(n, scenario)] += [distance(result, Truth)]
                if scenario.upper() == 'P' and n == WN:
                    # currently saves the weight, the key is the number of the simulation
                    weight_table[('P', counter)] += get_proxy_ranks(active_agents)
                elif scenario.upper() == 'V' and n == WN:
                    weight_table[('V', counter)] = get_proxy_ranks(active_agents)
            counter += 1
        print 'Simulation number ', counter, ' Number of active agents: ', n

    dist_table = {}
    weight_table_p = [0] * N
    weight_table_v = [0] * N
    # Creates the table dict, which contains the average distances from all the Runs (simulations),
    # if it's an empty list will add 'None' - for the V scenario
    for n, s in distance_table:
        if distance_table[(n, s)]:
            dist_table[(n, s)] = np.average(distance_table[(n, s)])
        else:
            dist_table[(n, s)] = None

    for i in range(WN):
        for k in weight_table:
            if k[0] == 'P':
                weight_table_p[i] += weight_table[k][i]
            else:
                weight_table_v[i] += weight_table[k][i]
    for i in range(WN):
        weight_table_v[i] = weight_table_v[i] / float(Runs)
        weight_table_p[i] = weight_table_p[i] / float(Runs)

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
    # avg_errors.extend(plt.plot(index_a, Vlist, color='c', linestyle=':', marker='p', markerfacecolor='c', label='V'))
    avg_errors.extend(plt.plot(index_a, Elist, color='g', linestyle='-', marker='s', markerfacecolor='g', label='E'))
    plt.setp(avg_errors, linewidth=2, markersize=5)

    plt.xlabel('Number of Active Subset')
    plt.ylabel('Avg Dist from T')
    plt.title(
        'Distance from the Truth with ' + str(Runs) + ' simulations \nPopulation size: ' + str(PopSize) + ' PHI=' + str(
            PHI) + ' A=' + str(A))
    plt.xticks(index_a, range(2, N + 1))
    # Legend Box appearance
    plt.legend(shadow=True, fancybox=True)
    # Auto layout design function
    plt.tight_layout()

    # set a new current figure
    plt.figure(2)
    # Plotting the weights graphs
    index_b = np.arange(1, WN + 1)
    avg_weights = []
    avg_weights.extend(
        plt.plot(index_b, weight_table_p, color='y', linestyle='-', marker='s', markerfacecolor='y', label='Proxy'))
    # avg_weights.extend(
    #     plt.plot(index_b, weight_table_v, color='r', linestyle='-', marker='s', markerfacecolor='r', label='Virtual Proxy'))
    # plt.setp(avg_weights, linewidth=2, markersize=5)

    plt.xlabel('The rank of the Active agent')
    plt.ylabel('Average Weight')
    plt.title('The average weights of the proxies ' + str(Runs) + ' simulations \nPopulation size: ' + str(PopSize))
    plt.xticks(index_b, range(1, WN + 1))
    # Legend Box appearance
    plt.legend(shadow=True, fancybox=True)
    # Auto layout design function
    plt.tight_layout()

    # The rendering function - shows the output on the screen
    plt.show()


if __name__ == '__main__':
    main()
