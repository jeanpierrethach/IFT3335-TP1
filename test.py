import numpy as np
from heuristics import *

def test_swap():
    p0 = np.array([[4,2,7,1,0,0,0,0,8], 
                  [6,8,9,2,0,7,1,3,5], 
                  [3,5,1,0,8,9,2,4,7], 
                  [0,0,0,4,6,8,5,0,9], 
                  [5,0,0,7,9,2,0,8,1], 
                  [7,0,8,5,1,0,4,2,6], 
                  [0,1,6,8,7,4,9,5,3], 
                  [0,4,0,9,0,1,7,6,2], 
                  [9,0,5,3,2,6,8,1,4]])
    desired_state = np.array([[2,4,7,1,0,0,0,0,8], 
                              [6,8,9,2,0,7,1,3,5], 
                              [3,5,1,0,8,9,2,4,7], 
                              [0,0,0,4,6,8,5,0,9], 
                              [5,0,0,7,9,2,0,8,1], 
                              [7,0,8,5,1,0,4,2,6], 
                              [0,1,6,8,7,4,9,5,3], 
                              [0,4,0,9,0,1,7,6,2], 
                              [9,0,5,3,2,6,8,1,4]])

    s = Sudoku(p0)

    sq1 = (0,0)
    sq2 = (0,1)
    
    new_state = s.swap(sq1,sq2)
    np.testing.assert_array_equal(new_state, desired_state)
    print("test_swap: passed")

def test_global_conflicts():
    p0 = np.array([[4,2,7,1,3,4,6,9,8],  #1
                   [6,8,9,2,6,7,1,3,5],  #1
                   [3,5,1,5,8,9,2,4,7],  #1
                   [6,1,5,4,6,8,5,3,9],  #2
                   [3,4,2,7,9,2,7,8,1],  #2
                   [7,9,8,5,1,3,4,2,6],  #0
                   [7,1,6,8,7,4,9,5,3],  #1
                   [3,4,2,9,5,1,7,6,2],  #1
                   [9,8,5,3,2,6,8,1,4]]) #1
                   #5 3 2 1 1 1 1 1 0    25

    s = Sudoku(p0)
    gc = s.global_conflicts(s.state)
    assert(gc == 25)
    print("test_global_conflicts: passed")
    

def test_cost_function():
    p0 = np.array([[4,2,7,1,3,4,6,9,8],  #1
                   [6,8,9,2,6,7,1,3,5],  #1
                   [3,5,1,5,8,9,2,4,7],  #1
                   [6,1,5,4,6,8,5,3,9],  #2
                   [3,4,2,7,9,2,7,8,1],  #2
                   [7,9,8,5,1,3,4,2,6],  #0
                   [7,1,6,8,7,4,9,5,3],  #1
                   [3,4,2,9,5,1,7,6,2],  #1
                   [9,8,5,3,2,6,8,1,4]]) #1
                   #4 3 2 1 1 1 1 1 0    24
    s = Sudoku(p0)
    cost = s.cost_function(s.state)
    assert(cost == 24)
    print("test_cost_function: passed")

def test_nb_worse_scenario_squares_combinations():
    p0 = np.zeros((9,9))
    s = Sudoku(p0)
    combinations = len(list(s.squares_combinations()))
    assert(combinations == 324)
    print("test_nb_worse_scenario_squares_combinations: passed")
    
def test_squares_combinations():
    pass

def test_squares_combinations_reduced_conflicts():
    pass


if __name__ == '__main__':
    test_swap()
    test_global_conflicts()
    test_cost_function()
    test_nb_worse_scenario_squares_combinations()
    test_squares_combinations()