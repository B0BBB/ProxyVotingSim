from collections import OrderedDict
from utils import kendall_tau

# This is the configuration module, which will set the Global variables
PopSize = 22
A = 5
N = 22
WN = 7
Truth = range(A)
PHI = 0.95
Mel = OrderedDict()
Vnearest = 3
Scenarios = ['E', 'P', 'V', 'B']
Runs = 15000
distance = kendall_tau
