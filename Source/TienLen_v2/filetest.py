import math
from numpy import random
import torch
import numpy as np
from torch._C import dtype
from torch.distributions.categorical import Categorical

device = torch.device("cpu")

a = torch.ones((12), dtype=torch.float64)

b = np.array([1,0,1,0,1,0,1,0,0,1,1,0])

mask = torch.tensor(b, dtype=torch.bool).to(device)

a[~mask] = -math.inf
a = torch.softmax(a, dim=0)
print(a)
for i in range(0,100000,1):
    re = Categorical(a)

    arr = re.sample().item()
    if(b[arr] == 0):
        print("fail")
        break