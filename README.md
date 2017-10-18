# ProxyVotingSim
Simulations for proxy voting

`VotingAgent.py` - Contains the class of a voting agent.

`config.py` - Configuration file, contains all the global configurations for the simulations

`Simulations.py` - All the functions a single simulation is using (sort of utility functions)

`Main.py` - The main function of the program connects and puts into use all the other modules

## config.py

*PopSize*  
Sets the population size

*K*  
Sets the number of topics for voting

*N*  
Sets the number of Active agents that will be sampled

*Truth*  
Sets the ground truth

*PHI*  
Sets the parameter in the mellow distribution model for the population

*Vnearest*  
Sets the number of nearest proxies that will be chosen in the virtual scenario

*Runs*  
Sets the number of simulation that will run for each combination of scenario (s) and number of agents (n)

### Global variables:  
Mel = OrderedDict()  
The dictionary that holds the sampled population

Scenarios = ['E', 'V', 'P', 'B']  
A list of the scenarios that will run
