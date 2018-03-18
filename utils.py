import os
import random
import numpy as np

def probability(p):
    '''
    Returns true with probability p
    '''
    return p > random.uniform(0.0, 1.0)

def read_file(filename, sep='\n'):
    with open(filename, 'r') as file:
        return file.read().strip().split(sep)

def shape(f):
    return np.array(tuple(map(int,f))).reshape((9,9))

def min_random_tie(min_state, possible_states):
    '''
    Returns a random state index from the possible states that has 
    the smallest number of global conflicts 
    '''
    states = [i for i,v in enumerate(possible_states) if v[1] == min_state[1]]
    return random.choice(states)

def maybe_make_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def array2str(arr):
    return ''.join(str(x) for x in arr)