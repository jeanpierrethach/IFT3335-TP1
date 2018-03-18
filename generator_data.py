import os
import csv
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)

CSV_FORMAT = "csv"

def output_csv(args, data):
    r_dir = os.path.join(SCRIPT_DIR, args.results_dir)
    base_filename = "data_" + args.heuristic
    field_names = ['initial_state', 'heuristic', 'final_state', 'cost', 'explored', 'time']

    with open(os.path.join(r_dir, base_filename + "." + CSV_FORMAT), "w") as f:
        csv_out = csv.writer(f, lineterminator='\n')
        csv_out.writerow(field_names)
        for line in data:
            csv_out.writerow(line)

def display_avg_stats(args):
    r_dir = os.path.join(SCRIPT_DIR, args.results_dir)
    base_filename = "data_" + args.heuristic
    df = pd.read_csv(os.path.join(r_dir, base_filename + "." + CSV_FORMAT), usecols=['cost', 'explored', 'time'])
    data = df.values
    mean = np.mean(data, axis=0)
    print('avg cost:',mean[0])
    print('avg explored:',mean[1])
    print('avg time:',mean[2])
    print('solution found: %f %%' % (len([x for x in data[:,0] if x == 0]) / len(data[:,0]) * 100))