# pure LIP (Linear Integer Programming)
# from docs

import numpy as np
from scipy.optimize import linear_sum_assignment

cost_matrix = np.array([
    [0, 1, 2], 
    [0, 2, 1], 
    [1, 0, 2]
])

row_ind, col_ind = linear_sum_assignment(cost_matrix)
opt_ass = col_ind
tc = cost_matrix[row_ind, col_ind].sum()
for i in range(3):
    print(cost_matrix[i, col_ind[i]])

print(opt_ass)
print('Total Assignment cost is %d' %tc)