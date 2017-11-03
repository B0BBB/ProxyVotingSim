from collections import OrderedDict
from itertools import combinations
# Library located at https://pypi.python.org/pypi/Distance/
from distance import hamming

# This is the configuration module, which will set the Global variables
PopSize = 22
A = 4
N = 22
WN = 21
Truth = range(A)  # [0,1,2,...,A-1]
PHI = 0.95
Mel = OrderedDict()
Vnearest = 3
Scenarios = ['E', 'V', 'P', 'B']
Runs = 100
K = 0
for i in combinations(Truth, 2):
    K += 1
distance = hamming
