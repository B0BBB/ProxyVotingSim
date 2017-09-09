from time import time
# Library located at https://pypi.python.org/pypi/Distance/
from distance import hamming
import VotingAgent
from Simulations import create_mel_dist, create_f_pop, create_active_voters, bm_majority_vote
from config import *


def main():
    print 'Creating Data Set'
    t1 = time()
    create_mel_dist(Truth, PHI, hamming, K)
    data = create_f_pop(PopSize, Mel)
    t2 = time()
    print 'Data set creation took :', t2 - t1
    scenario = raw_input('Enter Scenario B/P/E/P+V: \n')
    while scenario != '':
        t1 = time()
        print '\nComputing OutCome :'
        activeAgents = create_active_voters(data, N, scenario)
        if scenario == 'B' or scenario == 'b':
            print 'The Active agents are: ', activeAgents
        t2 = time()
        result = bm_majority_vote(activeAgents)
        print 'The result vector is: ', result
        print 'the distance from T is: ', hamming(result, Truth)
        t3 = time()
        print 'The build of active agent took:'
        if t2 - t1 < 60:
            print t2 - t1, 'Seconds'
        else:
            print (t2 - t1) / 60, 'Minutes'
        print 'The Computation took:', t3 - t2
        print 'Outcome Computation took (total):', t3 - t1
        scenario = raw_input('Enter Scenario B/P/E/P+V: \n')


if __name__ == '__main__':
    main()
