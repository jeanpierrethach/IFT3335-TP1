import argparse
import time

from utils import read_file, shape
from plots import *
from heuristics import *

def parse_args():
        parser = argparse.ArgumentParser()

        parser.add_argument('--heuristic', type=str,
                            required=True,
                            choices=['hc', 'hcr', 'sa'],
                            help='hc for Hill Climbing, hcr for Hill Climbing reduced, sa for simulated_annealing')
        parser.add_argument('--filename', type=str,
                            default='100sudoku.txt',
                            help='The filename containing sequence of 81 digits. (default: %(default)s)')
        parser.add_argument('--verbose', 
                            action='store_true',
                            help='Boolean flag indicating if statements should be printed to the console.')

        args = parser.parse_args()
        return args

if __name__ == '__main__':
    args = parse_args()
    problems = read_file(args.filename)

    x = []
    y = []

    for p in problems:
        start = time.clock()
        
        initial_state = shape(p)
        s = Sudoku(initial_state)
        s.random_fill()

        if args.heuristic == 'hc':
            final_state, steps = s.hill_climbing()
            if args.verbose:
                print("steps: %d, conflicts: %d" % (steps, s.global_conflicts(final_state)))
            x.append(s.global_conflicts(final_state))
            y.append(steps)
        elif args.heuristic == 'hcr':
            final_state, steps = s.hill_climbing_reduced()
            if args.verbose:
                print("steps: %d, conflicts: %d" % (steps, s.global_conflicts(final_state)))
            x.append(s.global_conflicts(final_state))
            y.append(steps)
        elif args.heuristic == 'sa':
            final_state, cost_overtime, steps = s.simulated_annealing()
            if args.verbose:
                print("cost function: %d" % s.cost_function(final_state))
            x.append(steps)
            y.append(cost_overtime)

        tclock = time.clock() - start
        if args.verbose:
            print("execution time:", tclock)
    
    # TODO create file for useful data

    if args.heuristic == 'hc':
        plot_2D_grid(x, y, 'conflicts', 'steps', 'Hill Climbing', 'ro', args)
    elif args.heuristic == 'hcr':
        plot_2D_grid(x, y, 'conflicts', 'steps', 'Hill Climbing reduced', 'ro', args)
    elif args.heuristic == 'sa':   
        plot_2D_grid(x, y, 'iteration', 'cost', 'Simulated Annealing', 'b-', args)