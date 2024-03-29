import argparse
import time

from utils import read_file, shape, maybe_make_directory, array2str
from plots import plot_2D_grid_hc, plot_2D_grid_hcr, plot_2D_grid_sa
from generator_data import output_csv, display_avg_stats
from heuristics import Sudoku

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
        parser.add_argument('--img_output_dir', type=str,
                            default='./graphs_output',
                            help='Relative or absolute directory path to output image graphs.')
        parser.add_argument('--results_dir', type=str,
                            default='./results',
                            help='Relative or absolute directory path to data results.')                    

        args = parser.parse_args()

        maybe_make_directory(args.img_output_dir)
        maybe_make_directory(args.results_dir)
        return args

def run_hill_climbing(args, s):
    final_state, steps = s.hill_climbing()
    if args.verbose:
        print("steps: %d, conflicts: %d" % (steps, s.global_conflicts(final_state)))
    return final_state, steps, s.global_conflicts(final_state)

def run_hill_climbing_reduced(args, s):
    final_state, steps = s.hill_climbing_reduced()
    if args.verbose:
        print("steps: %d, conflicts: %d" % (steps, s.global_conflicts(final_state)))
    return final_state, steps, s.global_conflicts(final_state)

def run_simulated_annealing(args, s):
    final_state, cost_overtime, steps = s.simulated_annealing()
    if args.verbose:
        print("cost function: %d" % s.cost_function(final_state))
    return final_state, steps, cost_overtime

if __name__ == '__main__':
    args = parse_args()
    problems = read_file(args.filename)

    x = []
    y = []
    data = []

    heuristics_options = {
        "hc": run_hill_climbing,
        "hcr": run_hill_climbing_reduced,
        "sa": run_simulated_annealing
    }

    for p in problems:
        start = time.clock()
        
        initial_state = shape(p)
        s = Sudoku(initial_state)
        s.random_fill()
        final_state, steps, score = heuristics_options[args.heuristic](args, s)
        x.append(steps)
        y.append(score)

        tclock = time.clock() - start
        if args.verbose:
            print("execution time:", tclock)

        if args.heuristic == "sa":
            data.append((p, args.heuristic, array2str(final_state.flatten()), s.cost_function(final_state), len(steps), tclock))
        else:
            data.append((p, args.heuristic, array2str(final_state.flatten()), score, steps, tclock))

    output_csv(args, data)

    plots_options = {
        "hc": plot_2D_grid_hc,
        "hcr": plot_2D_grid_hcr,
        "sa": plot_2D_grid_sa
    }

    plots_options[args.heuristic](x, y, args.img_output_dir)

    display_avg_stats(args)