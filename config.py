from collections import OrderedDict
from utils import kendall_tau

# This is the configuration module, which will set the Global variables
PopSize = 100
A = 4
N = 20
WN = 20
Truth = range(A)
PHI = 0.95
Mel = OrderedDict()
Vnearest = 3
Scenarios = ['E', 'P', 'V', 'B']
Runs = 20000
distance = kendall_tau
