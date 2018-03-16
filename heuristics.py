import numpy as np
import random
import math
from utils import min_random_tie, probability
from itertools import combinations
from operator import itemgetter

digits = [1,2,3,4,5,6,7,8,9]

class Sudoku():
    def __init__(self, initial_state):
        self.state = initial_state
        self.fixed_cells = list(zip(*np.where(self.state != 0)))

    def hill_climbing(self):
        explored = []
        combinations = list(self.squares_combinations())
        
        while True:
            possible_states = []

            for c in combinations:
                ns = self.swap(c[0], c[1])
                possible_states.append((ns, self.global_conflicts(ns)))

            # TODO could remove since possible_states will never be empty
            #if not possible_states:
            #    return self.state, len(explored)

            minimum_state = min(possible_states, key=itemgetter(1))
            rc = min_random_tie(minimum_state, possible_states)

            if possible_states[rc][1] >= self.global_conflicts(self.state):
                return self.state, len(explored)

            self.state = possible_states[rc][0]
            explored.append(possible_states[rc][0])

    def hill_climbing_reduced(self):
        explored = []
        
        while True:
            possible_states = []
            combinations = list(self.squares_combinations_reduced_conflicts())

            for c in combinations:
                ns = self.swap(c[0], c[1])
                possible_states.append((ns, self.global_conflicts(ns)))

            if not possible_states:
                return self.state, len(explored)

            minimum_state = min(possible_states, key=itemgetter(1))
            rc = min_random_tie(minimum_state, possible_states)

            if possible_states[rc][1] >= self.global_conflicts(self.state):
                return self.state, len(explored)

            self.state = possible_states[rc][0]
            explored.append(possible_states[rc][0])

    def simulated_annealing(self):
        T = 3.0
        alpha = 0.99
        epoch = 4000

        cost_overtime = []
        steps = []

        combinations = list(self.squares_combinations())

        for i in range(epoch):
            # TODO could remove since T will never be 0
            #if T == 0:
            #    return self.state
            possible_states = []
            for c in combinations:
                state = self.swap(c[0], c[1])
                possible_states.append(state)

            # TODO could remove since possible_states will never be empty
            #if not possible_states:
            #    return self.state, cost_overtime, steps

            next_state = random.choice(possible_states)
            delta_e = self.cost_function(next_state) - self.cost_function(self.state)

            # next state is accepted if is better than current state with respect
            # of cost function or probability
            if delta_e < 0 or probability(math.exp(-delta_e/T)):
                self.state = next_state

            cost_overtime.append(self.cost_function(self.state))
            steps.append(i)
            T = alpha * T

        return self.state, cost_overtime, steps
    
    def squares_combinations(self):
        '''
        Combinations of non fixed squares with non fixed squares for each unit.
        Generator of tuple of squares indexes. Ex: ((0,0),(0,1))
        '''
        for i,j in ((x,y) for x in range(3) for y in range(3)):
            all_squares = ((x,y) for x in range(i*3,i*3+3) for y in range(j*3,j*3+3))
            permissible_squares = (x for x in all_squares if x not in set(self.fixed_cells))
            for c in combinations(permissible_squares, 2):
                yield c

    def squares_combinations_reduced_conflicts(self):
        '''
        Combinations of non fixed squares with non fixed squares for each unit
        and ignores combinations that will necessarily generate conflicts 
        if they are swapped in their respective rows and columns.
        Generator of tuple of squares indexes. Ex: ((0,0),(0,1))
        '''
        rows = []
        cols = []
        for i in range(9):
            rows.append(set(self.state[i]))
            cols.append(set(self.state[:,i]))
        for i,j in ((x,y) for x in range(3) for y in range(3)):
            all_squares = ((x,y) for x in range(i*3,i*3+3) for y in range(j*3,j*3+3))
            permissible_squares = (x for x in all_squares if x not in set(self.fixed_cells))
            for c in combinations(permissible_squares, 2):
                # if the value of the square isn't present in the row and column of the other square
                if self.state[c[0][0], c[0][1]] not in rows[c[1][0]] and \
                   self.state[c[0][0], c[0][1]] not in cols[c[1][1]] and \
                   self.state[c[1][0], c[1][1]] not in rows[c[0][0]] and \
                   self.state[c[1][0], c[1][1]] not in cols[c[0][1]]:
                    yield c

    '''
    TODO simulated annealing heuristic, could use the squares combinations reduced conflicts too?

    OR take squares which has conflicts and make combinations with only the ones that reduce the conflicts
    which would be like the hill climbing, but still allow to randomly pick the next state instead of taking
    the minimum
    '''


    def cost_function(self, state):
        '''
        Returns the cost which represents the sum for each row and column
        of the sum of numbers from 1 through n^2 that are NOT present.
        The cost function of the optimal solution should equal to 0.
        '''    
        total = 0
        set_digits = set(digits)
        for i in range(9):
            total += len(set_digits - set(state[i])) 
            total += len(set_digits - set(state[:,i]))
        return total

    def swap(self, s1, s2):
        '''
        Returns a new state with swapped squares values.
        '''
        new_state = np.copy(self.state)
        i,j = s1
        m,n = s2
        new_state[i,j], new_state[m,n] = new_state[m,n], new_state[i,j]
        return new_state

    def random_fill(self):
        '''
        Randomly assign numbers into blank squares to generate a filled state 
        and takes in account the unit constraint.
        '''
        for i,j in zip(*np.where(self.state == 0)):
            current_unit = self.state[i//3*3:i//3*3+3,j//3*3:j//3*3+3].ravel()
            possible_values = np.setdiff1d(digits, current_unit)
            self.state[i,j] = random.choice(possible_values)
    
    def global_conflicts(self, state):
        '''
        Return the sum of the conflicts for each row and column of the state.
        The global score of the optimal solution should equal to 0.
        '''
        global_score = 0
        for i in range(9):
            _,r_counts = np.unique(state[i], return_counts=True)
            _,c_counts = np.unique(state[:,i], return_counts=True)

            # sum is used to make each key of number repeated 3 times count as 3 conflicts
            # len is used to make each key of number repeated 2 times count as 1 conflict 
            r_count_3 = sum(x for x in r_counts if x == 3)
            r_count_2 = len([x for x in r_counts if x == 2])
            c_count_3 = sum(x for x in c_counts if x == 3)
            c_count_2 = len([x for x in c_counts if x == 2])
            global_score += r_count_3 + r_count_2 + c_count_3 + c_count_2
        return global_score

    # TODO add this goal test for each algorithm since we want to stop when it reaches 0
    '''
    def test_goal(self, state):
        return self.global_conflicts(state) == 0
    '''
