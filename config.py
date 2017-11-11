from collections import OrderedDict
from utils import kendall_tau

# This is the configuration module, which will set the Global variables
PopSize = 100
A = 6
N = 25
WN = 25
Truth = range(A)
PHI = 0.95
Mel = OrderedDict()
Vnearest = 3
Scenarios = ['E', 'P', 'V', 'B']
Runs = 5000
distance = kendall_tau
