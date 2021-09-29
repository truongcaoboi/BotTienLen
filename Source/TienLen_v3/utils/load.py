import numpy as np

def loadAllGroup():
    # save np.load
    np_load_old = np.load

    # modify the default parameters of np.load
    np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
    a = np.load("allGroup.npz")["data"]

    # restore np.load for future normal usage
    np.load = np_load_old
    return a