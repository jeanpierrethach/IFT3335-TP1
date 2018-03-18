import numpy as np
import unittest
from heuristics import Sudoku

class TestSudokuMethods(unittest.TestCase):

    def test_swap(self):
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

    def test_global_conflicts(self):
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
        self.assertEqual(gc, 25)
        print("test_global_conflicts: passed")

    def test_no_global_conflicts(self):
        p0 = np.array([[1,9,8,5,2,6,3,4,7],
                    [7,2,5,3,4,1,6,9,8],
                    [3,4,6,9,7,8,2,1,5],
                    [9,8,1,2,5,7,4,6,3],
                    [5,6,4,1,3,9,8,7,2],
                    [2,3,7,6,8,4,1,5,9],
                    [4,7,3,8,1,5,9,2,6],
                    [8,1,9,7,6,2,5,3,4],
                    [6,5,2,4,9,3,7,8,1]])
        s = Sudoku(p0)
        gc = s.global_conflicts(s.state)
        self.assertEqual(gc, 0)
        print("test_no_global_conflicts: passed")
        
    def test_cost_function(self):
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
        self.assertEqual(cost, 24)
        print("test_cost_function: passed")

    def test_cost_function_optimal(self):
        p0 = np.array([[1,9,8,5,2,6,3,4,7],
                    [7,2,5,3,4,1,6,9,8],
                    [3,4,6,9,7,8,2,1,5],
                    [9,8,1,2,5,7,4,6,3],
                    [5,6,4,1,3,9,8,7,2],
                    [2,3,7,6,8,4,1,5,9],
                    [4,7,3,8,1,5,9,2,6],
                    [8,1,9,7,6,2,5,3,4],
                    [6,5,2,4,9,3,7,8,1]])
        s = Sudoku(p0)
        cost = s.cost_function(s.state)
        self.assertEqual(cost, 0)
        print("test_cost_function_optimal: passed")

    def test_nb_worse_scenario_squares_combinations(self):
        p0 = np.zeros((9,9))
        s = Sudoku(p0)
        combinations = len(list(s.squares_combinations()))
        self.assertEqual(combinations, 324)
        print("test_nb_worse_scenario_squares_combinations: passed")

    def test_squares_combinations(self):
        # possible combinations
        # unit1 = 28, unit2 = 21, unit3 = 15
        # unit4 = 10, unit5 = 6,  unit6 = 3
        # unit7 = 1,  unit8 = 0,  unit9 = 0
        p0 = np.array([[4,0,0,1,0,0,0,0,8], 
                    [0,0,0,2,0,0,1,0,0], 
                    [0,0,0,0,0,0,0,0,7], 
                    [0,0,2,4,6,8,5,0,9], 
                    [5,0,0,0,0,2,0,8,1], 
                    [7,0,8,5,0,0,4,0,6], 
                    [6,1,0,0,7,6,6,5,3], 
                    [3,4,0,9,5,1,9,7,2], 
                    [9,2,5,3,2,4,8,1,4]])
        
        s = Sudoku(p0)
        self.assertEqual(len(list(s.squares_combinations())), 84)
        print("test_squares_combinations: passed")

    def test_squares_combinations_reduced_conflicts(self):
        # possible combinations
        # [((0, 0), (2, 1)), ((0, 1), (2, 0)), 
        #  ((0, 2), (2, 1)), ((1, 0), (2, 1)), 
        #  ((1, 1), (2, 2)), ((1, 2), (2, 1)), 
        #  ((0, 5), (1, 3))]
        p0 = np.array([[1,3,4,4,6,3,2,9,8], 
                    [2,6,8,5,0,0,0,0,0], 
                    [5,7,9,0,0,0,0,0,0], 
                    [6,0,0,0,0,0,0,0,0], 
                    [9,0,0,0,0,0,0,0,0], 
                    [8,0,0,0,0,0,0,0,0], 
                    [4,0,0,0,0,0,0,0,0], 
                    [2,0,0,0,0,0,0,0,0], 
                    [9,0,0,0,0,0,0,0,0]])
        s = Sudoku(p0)
        s.fixed_cells = []

        self.assertEqual(len(list(s.squares_combinations_reduced_conflicts())), 7)
        print("test_squares_combinations_reduced_conflicts: passed")

    def test_random_fill(self):
        '''
        Verifies if each unit contains the set from 1 to 9
        after randomly filling the blank squares.
        '''
        p0 = np.array([[4,0,7,1,0,0,0,0,8], 
                    [0,8,9,2,0,7,1,0,5], 
                    [3,5,1,0,8,9,0,4,7], 
                    [0,0,0,4,6,8,5,0,9], 
                    [5,0,0,7,9,2,0,8,1], 
                    [7,0,8,5,1,0,4,0,6], 
                    [0,1,0,0,7,0,0,5,3], 
                    [0,4,0,9,0,1,0,0,2], 
                    [9,0,5,3,2,0,8,1,4]])
        s = Sudoku(p0)
        s.random_fill()

        for i,j in ((x,y) for x in range(0,9,3) for y in range(0,9,3)):
            current_unit = s.state[i//3*3:i//3*3+3,j//3*3:j//3*3+3].ravel()
            self.assertEqual(len(set(current_unit)), len(current_unit))
        print("test_random_fill: passed")


if __name__ == '__main__':
    unittest.main()