from multiprocessing import Pipe, Process
import pickle



from logic.TienLenGame import TienLenGame

import numpy as np

a = np.array([1,1])
a[0] = 0
print(a)