import random

def probability(p):
    "Return true with probability p."
    return p > random.uniform(0.0, 1.0)