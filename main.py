import numpy as np
import random
from itertools import combinations
import math, sys
from utils import *
import time

digits = [1,2,3,4,5,6,7,8,9]

class Sudoku():
    def __init__(self, initial_state):
        self.state = initial_state
        self.fixed_cells = list(zip(*np.where(self.state != 0)))

    def hill_climbing(self):
        explored = []

        def min_random_tie(min_state, arr): 
                states = [i for i,v in enumerate(arr) if v[1] == min_state[1]]
                return random.choice(states)

        while True:
            possible_states = []

            for c in self.actions_combinations():
                ns = self.swap(c[0], c[1])
                possible_states.append((ns, self.global_conflicts(ns)))

            # TODO could remove since p_state will never be empty
            #if not possible_states:
            #    return self.state, len(explored)

            minimum_state = min(possible_states, key=lambda x:x[1])
            rc = min_random_tie(minimum_state, possible_states)

            if possible_states[rc][1] >= self.global_conflicts(self.state):
                return self.state, len(explored)
           
            print(possible_states[rc])
            self.state = possible_states[rc][0]
            explored.append(possible_states[rc][0])
           
    '''
    FROM AIMA

    def hill_climbing(problem):
        """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Fig. 4.2]"""
    current = Node(problem.initial)
    explored = set()
    while True:
        neighbors = current.expand(problem)
        explored.update(node.state for node in neighbors)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors,
                                     lambda node: problem.value(node.state))
        if problem.value(neighbor.state) <= problem.value(current.state):
            break
        current = neighbor
    return current.state, len(explored)

    '''
    

    # TODO cost function should go towards 0
    def simulated_annealing(self):
        T = 3.0
        alpha = 0.9999 # 0.99
        epoch = 10000
        
        for _ in range(epoch):
            # TODO could remove since T will never be 0
            #if T == 0:
            #    return self.state
            possible_states = []
            for a in self.actions_combinations():
                state = self.swap(a[0], a[1])
                possible_states.append(state)

            # TODO could remove since possible_states will never be empty
            if not possible_states:
                return self.state

            next_state = random.choice(possible_states)
            delta_e = self.cost_function(next_state) - self.cost_function(self.state)

            # neighbour is accepted if is better than current state with respect
            # of cost function or probability
            '''
            # TODO FIX: probability range overflow [FIXED] by adding 9s into alpha
              TODO FIX: seems not to converge to 0?
            '''
            if delta_e < 0 or probability(math.exp(delta_e/T)):
                self.state = next_state

            #print(T, self.cost_function(self.state))
            T = alpha * T
        return self.state

    '''
    FROM AIMA

    def exp_schedule(k=20, lam=0.005, limit=100):
        "One possible schedule function for simulated annealing"
        return lambda t: if_(t < limit, k * math.exp(-lam * t), 0)

    def simulated_annealing(problem, schedule=exp_schedule()):
        "[Fig. 4.5]"
        current = Node(problem.initial)
        for t in xrange(sys.maxint):
            T = schedule(t)
            if T == 0:
                return current
            neighbors = current.expand(problem)
            if not neighbors:
                return current
            next = random.choice(neighbors)
            delta_e = problem.value(next.state) - problem.value(current.state)
            if delta_e > 0 or probability(math.exp(delta_e/T)):
                current = next
    '''
    
    def actions_combinations(self):
        '''
        combinations of non fixed cases with non fixed cases for each unit
        '''
        for i,j in ((x,y) for x in range(3) for y in range(3)):
            all_actions = ((x,y) for x in range(i*3,i*3+3) for y in range(j*3,j*3+3))
            permissible_actions = (x for x in all_actions if x not in set(self.fixed_cells))
            for c in combinations(permissible_actions, 2):
                yield c


    def cost_function(self, state):
        '''
        sum of values of row and column
        values = calculates the number of values, 1 through n^2 that are NOT present
        optimal solution should be equal to 0
        '''    
        total = 0
        set_digits = set(digits)
        for i in range(9):
            total += len(set_digits - set(state[i])) 
            total += len(set_digits - set(state[:,i]))
        return total


    '''
    TODO may remove this
    WIP : trying to remove indexes where doesn't contain the value in the row and column
    in another square
    
    def select_permissible_case(self, i, j, k):
        #for i in range(0,9):
        #    for j in range(0,9):
        #if (i,j) not in self.set_fixed_cells:
        row = self.state[i]
        col = self.state[:,j]
        unit = self.state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]

        for i,j in zip(*np.where(unit != 0)):
            #if k not in row and k not in col:
            print(i,j)
        #print(unit)
 

        #if k not in row and k not in col and k not in unit:
        #    yield (i, j, k)
    '''

    def swap(self, c1, c2):
        new_state = np.copy(self.state)
        i,j = c1
        m,n = c2
        new_state[i,j], new_state[m,n] = new_state[m,n], new_state[i,j]
        return new_state

    '''
    # TODO is this needed
    def action(self):
        
        #action possible for current state
        
        for i in range(9):
            for j in range(9):
                if (i,j) not in self.fixed_cells:
                    k = self.state[i,j]
                    yield (i, j, k)

    # TODO is this needed
    def result(self, action):
        
        #result of action for a state
        
        new_state = self.state
        i,j,k = action
        new_state[i,j] = k
        return new_state
    '''

    def random_fill(self):
        '''
        generate filled problem with unit constraint
        '''
        for i,j in zip(*np.where(self.state == 0)):
            current_unit = self.state[i//3*3:i//3*3+3,j//3*3:j//3*3+3].ravel()
            possible_values = np.setdiff1d(digits, current_unit)
            self.state[i,j] = random.choice(possible_values)
    
    def global_conflicts(self, state):
        global_score = 0
        for i in range(9):
            _,r_counts = np.unique(state[i], return_counts=True)
            _,c_counts = np.unique(state[:,i], return_counts=True)
            r_count_3 = sum(item for item in r_counts if item == 3)
            r_count_2 = len([item for item in r_counts if item == 2])
            c_count_3 = sum(item for item in c_counts if item == 3)
            c_count_2 = len([item for item in c_counts if item == 2])
            global_score += r_count_3 + r_count_2 + c_count_3 + c_count_2
        return global_score

    '''
    def test_goal(self, state):
        return global_conflicts(state) == 0
    '''

def read_file(filename, sep='\n'):
    with open(filename, 'r') as file:
        return file.read().strip().split(sep)

def shape(f):
    return np.array(tuple(map(int,f))).reshape((9,9))

problems = read_file('100sudoku.txt')
initial_state = problems[0]
initial_state = shape(initial_state)

# 0 1 2 -> 0:3, i:j
# 3 4 5 -> 3:6, i:j
# 6 7 8 -> 6:9, i:j

print(initial_state)
print("\n")

start = time.clock()

s = Sudoku(initial_state)
print(s.fixed_cells)
s.random_fill()
print(initial_state)
gc = s.global_conflicts(initial_state)
print("GLOBAL_CONFLICTS: ", gc)


# uncomment for HILL_CLIMBING


final_state, steps = s.hill_climbing()
print("FINAL STATE: \n", final_state)
print("steps: %d, cost function: %d" % (steps, s.cost_function(final_state)))


# uncomment for simulated annealing

'''
final_state = s.simulated_annealing()
print("FINAL STATE: \n", final_state)
print(s.cost_function(final_state))
'''


'''
#TESTS
test = np.array([[4,2,7,1,3,5,6,9,8], 
                [6,8,9,2,4,7,1,3,5], 
                [3,5,1,6,8,9,2,4,7], 
                [1,3,2,4,6,8,5,7,9], 
                [5,6,4,7,9,2,3,8,1], 
                [7,9,8,5,1,3,4,2,6], 
                [2,1,6,8,7,4,9,5,3], 
                [8,4,3,9,5,1,7,6,2], 
                [9,7,5,3,2,6,8,1,4]])
print("\n TEST \n", test)

test2 = np.array([[4,2,7,1,0,0,0,0,8], 
                [6,8,9,2,0,7,1,3,5], 
                [3,5,1,0,8,9,2,4,7], 
                [0,0,0,4,6,8,5,0,9], 
                [5,0,0,7,9,2,0,8,1], 
                [7,0,8,5,1,0,4,2,6], 
                [0,1,6,8,7,4,9,5,3], 
                [0,4,0,9,0,1,7,6,2], 
                [9,0,5,3,2,6,8,1,4]])

p = Sudoku(test2)
p.random_fill()
final_state = p.hill_climbing()
#s.cost_function(test)
'''


tclock = time.clock() - start
print("exec time:", tclock)


# if count = 3 -> 3 conflicts
# if count = 2 -> 1 conflict
# if count = 1 -> ignore

'''
define hill-climbing
- randomize value of cases based on unit constraint
- define possible actions
- get results for each potential state based on action
- minimize the global conflicts for the next state
- repeat until a plateau is reached 
'''
