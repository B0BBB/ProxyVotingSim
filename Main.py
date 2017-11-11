from collections import defaultdict
from random import sample
from time import time
import csv

import matplotlib.pyplot as plt
import numpy as np
from sympy.printing.pretty.pretty_symbology import pretty_symbol

# Library located at https://pypi.python.org/pypi/Distance/
from Simulations import create_mel_dist, create_f_pop, create_ballots, reset_active_agents, \
    get_proxy_ranks
from utils import borda_voting_rule
from config import *


def main():
    print 'All set, the parameters are:', pretty_symbol('phi'), '=', PHI, 'A =', A, 'N =', N, 'Iterations =', Runs
    print 'Population Size =', PopSize, 'Truth =', Truth, 'Vnearest =', Vnearest
    print 'Weights will be calculated for', WN, 'Agents \n'
    print 'Creating Mellow\'s Distribution for the Data Set \n'

    create_mel_dist(Truth, PHI, distance)

    n = N
    ftime = 0

    with open('popStat2.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Pop distance Mean', 'Pop distance Med', 'Pop distance Var', 'W(P[1])', 'B', 'P', 'V', 'E'])

    for big_run in range(100):
        overtime = time()
        distance_table = defaultdict(list)
        weight_table = defaultdict(list)
        counter = 1
        print 'Creating Population \n'
        data = create_f_pop(PopSize, Mel)
        print 'Running Simulations \n'
        for run in range(Runs):
            stime = time()
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
                ftime += time() - stime
                if counter % 100 == 0:
                    print 'Simulation number', counter, 'Number of active agents:', n, 'Exec Time:', int(ftime), 'Sec '
                    ftime = 0
        minutes = int((time() - overtime) / 60)
        seconds = int(time() - overtime - minutes)
        print counter, 'Simulations', 'Number of active agents:', n, 'Exec Time:', minutes, 'Min', seconds, 'Sec'
        dist_table = {}
        weight_table_p = [0] * WN
        weight_table_v = [0] * WN
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

        scen_list = [dist_table[(n, 'B')]]
        scen_list += [dist_table[(n, 'P')]]
        scen_list += [dist_table[(n, 'V')]]
        scen_list += [dist_table[(n, 'E')]]
        pop_distance = []
        for i in data:
            pop_distance += [distance(Truth, i.location)]
        with open('popStat2.csv', 'ab') as f:
            writer = csv.writer(f)
            x = [np.mean(pop_distance), np.median(pop_distance), np.var(pop_distance), weight_table_p[1]] + scen_list
            writer.writerow(x)

    with open('Population2.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in data:
            x = tuple(['D=', distance(Truth, i.location)])
            writer.writerow(i.location + x)


if __name__ == '__main__':
    main()
