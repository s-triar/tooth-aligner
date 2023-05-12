import numpy as np

a = np.array([
    [1,2],
    [2,3],
    [4,7],
    [7,1],
    [9,4]
    ])
print(a[:,0])
print(np.argmin(a[:,0]))
print(np.argmin(a[:,1]))