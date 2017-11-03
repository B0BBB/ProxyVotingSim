from collections import OrderedDict
from utils import kendall_tau

# This is the configuration module, which will set the Global variables
PopSize = 100
A = 4
N = 5
WN = 5
Truth = range(A)
PHI = 0.95
Mel = OrderedDict()
Vnearest = 3
Scenarios = ['E', 'P', 'B']
Runs = 100
distance = kendall_tau
