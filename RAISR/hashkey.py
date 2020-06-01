import numpy as np
from math import atan2, floor, pi

def hashkey(block, Qangle, W):
    gy, gx = np.gradient(block)

    gx = gx.ravel()
    gy = gy.ravel()

    G = np.vstack((gx,gy)).T
    GTWG = G.T.dot(W).dot(G)
    w, v = np.linalg.eig(GTWG);

    nonzerow = np.count_nonzero(np.isreal(w))
    nonzerov = np.count_nonzero(np.isreal(v))
    if nonzerow != 0:
        w = np.real(w)
    if nonzerov != 0:
        v = np.real(v)

    idx = w.argsort()[::-1]
    w = w[idx]
    v = v[:, idx]

    theta = atan2(v[1, 0], v[0, 0])
    if theta < 0:
        theta = theta + pi

    lamda = w[0]

    sqrtlamda1 = np.sqrt(w[0])
    sqrtlamda2 = np.sqrt(w[1])
    if sqrtlamda1 + sqrtlamda2 == 0:
        u = 0
    else:
        u = (sqrtlamda1 - sqrtlamda2) / (sqrtlamda1 + sqrtlamda2)

    angle = floor(theta / pi * Qangle)
    if lamda < 0.0001:
        strength = 0
    elif lamda > 0.001:
        strength = 2
    else:
        strength = 1
    if u < 0.25:
        coherence = 0
    elif u > 0.5:
        coherence = 2
    else:
        coherence = 1

    if angle > 23:
        angle = 23
    elif angle < 0:
        angle = 0

    return angle, strength, coherence
