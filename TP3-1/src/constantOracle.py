# initialization
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, assemble, transpile

# import basic plot tools
from qiskit.visualization import plot_histogram

# set the length of the n-bit input string. 
n = 3

const_oracle = QuantumCircuit(n+1)

for i in range(n):
    output = np.random.randint(2)
    if output == 1:
        const_oracle.x(n)


print(const_oracle.draw())