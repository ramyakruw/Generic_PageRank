import numpy as np
import scipy as sc
import pandas as pd
from fractions import Fraction


# keep it clean and tidy
def float_format(vector, decimal):
    return np.round(vector.astype(np.float), decimals=decimal)


def filter_connections(p_column, p_column_index):
    global adj_matrix
    # filter connections from node column_index to all other nodes
    connections_from_column_index = [x for x in adj_matrix if int(x.strip().split(" ")[0]) == p_column_index]
    total_connections_from_column_index = len(connections_from_column_index)
    if total_connections_from_column_index == 0:
        return
    node_value = Fraction(1, total_connections_from_column_index)
    for b in [int(x.split(" ")[1]) for x in connections_from_column_index]:
        p_column[b - 1] = node_value

# text file with the adjacency matrix as graph.txt
fileName = "graph.txt"

with open(fileName) as f:
    adj_matrix = f.readlines()

# filter nodes with links
adj_matrix = [x.strip() for x in adj_matrix if int(x.strip().split(" ")[2]) == 1]

# Get the max number of nodes
leftColumnMaxNode = max([int(x.split(" ")[0]) for x in adj_matrix])
rightColumnMaxNode = max([int(x.split(" ")[1]) for x in adj_matrix])

# total nodes
totalNodes = int(max(leftColumnMaxNode, rightColumnMaxNode))

# Build the stocashtic matrix
M = np.zeros((totalNodes, totalNodes), np.double)

column_index = 1
for column in M.T:
    filter_connections(column, column_index)
    column_index += 1

print(totalNodes)
print(float_format(M, 6))

n = Fraction(1, totalNodes)

En = np.zeros((6, 6))
En[:] = n

print("v", En)
# beta value
beta = 0.85

# Multiply M with beta
A = beta * M
print("A", A)
# Initial the value of vector v
v = np.matrix([n, n, n, n, n, n])
v = np.transpose(v)
print("initial vector", float_format(v, 6))
previous_vector = v
for it in range(1, 300):
    v = A * v + ((1 - beta) * En)
    print("v'", float_format(v, 6))
    print("count", it)
    # check if converged
    if (float_format(previous_vector, 6) == float_format(v, 6)).all():
        break
    previous_vector = v

print("Final:\n", float_format(v, 6))
