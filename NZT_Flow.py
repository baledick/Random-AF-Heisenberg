import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from random_singlets.NZT_RSS import NZT_Random_Spin
import time

start_time = time.time()

N_systems = 1000 #the amount of different systems we want to check
lattice_size = 1001 # the number of spin particles
ceiling = 1 # the ceiling for the possible strength of the bonds
floor = 0.01 # the floor to stop the RG process at low energies
transformation_iterations = 300 # how many transformations should be made in each system
range_iterations = np.array(range(transformation_iterations))
temperature = 1

plt.style.use('fivethirtyeight')

values = np.zeros(transformation_iterations)
log_values = np.zeros(transformation_iterations)
cov_values = np.zeros(transformation_iterations)

for i in tqdm(range(N_systems)):
    system = NZT_Random_Spin(lattice_size, ceiling, floor, temperature) #this creates the spin chain based on the chain class
    for j in range(transformation_iterations):
        system.nzt_elimination()
        values[j] = system.logmax
    log_values += values
    cov_values += values**2

log_values /= N_systems
cov_values /= N_systems
cov_values -= log_values**2
cov_values = np.sqrt(cov_values)

plt.errorbar(range_iterations, log_values, yerr = cov_values)
plt.plot(log_values)
plt.legend(loc = "upper right")
plt.ylabel("$\Gamma = -\ln(\Omega)$")
plt.xlabel("RG iterations")
plt.title(f"Change in $\Gamma$ for the Non-Zero Temperature Case, N_systems = {N_systems}")
plt.show()

print("--- %s seconds ---" % (time.time() - start_time))
