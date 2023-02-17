import numpy as np

x = np.arange(1, 25).reshape(2, 12)

x1, x2, x3 = np.hsplit(x, 3)
print(x1)
print(x2)
print(x3)
