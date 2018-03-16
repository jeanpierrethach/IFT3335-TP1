import matplotlib.pyplot as plt
import numpy as np

def plot_2D_grid(x, y, x_label, y_label, title, format, args):
    plt.plot(x, y, format)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    if args.heuristic == 'sa':
        plt.xticks(np.arange(0, 4000, 1000.0))
        plt.yticks(np.arange(0, 140, 20.0))
        plt.savefig('simulated_annealing.png')
    elif args.heuristic == 'hc' or 'hch':
        plt.xticks(np.arange(0, max(x)+1, 2.0))
        plt.yticks(np.arange(min(y), max(y)+1, 1.0))
        plt.savefig('hill_climbing.png')
    
    plt.show()
    plt.close()
    
