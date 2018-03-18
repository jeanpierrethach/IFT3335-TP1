import os
import csv

SCRIPT_DIR = os.path.dirname(__file__)

def output_csv(args, data):
    r_dir = os.path.join(SCRIPT_DIR, args.results_dir)
    base_filename = "data_" + args.heuristic
    format = "csv"
    field_names = ['initial_state', 'heuristic', 'final_state', 'cost', 'explored', 'time']

    with open(os.path.join(r_dir, base_filename + "." + format), "w") as f:
        csv_out = csv.writer(f, lineterminator='\n')
        csv_out.writerow(field_names)
        for line in data:
            csv_out.writerow(line)