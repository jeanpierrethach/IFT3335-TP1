import os
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)

def plot_2D_grid_hc(x, y, img_output_dir):
    plt.plot(x, y, 'ro')
    plt.title('Hill Climbing')
    plt.xlabel('steps')
    plt.ylabel('conflicts')
    plt.xticks(np.arange(0, max(x)+1, 2.0))
    plt.yticks(np.arange(min(y), max(y)+1, 1.0))

    r_dir = os.path.join(SCRIPT_DIR, img_output_dir)
    plt.savefig(os.path.join(r_dir,'hill_climbing.png'))
    plt.show()
    plt.close()
    
def plot_2D_grid_hcr(x, y, img_output_dir):
    plt.plot(x, y, 'ro')
    plt.title('Hill Climbing reduced')
    plt.xlabel('steps')
    plt.ylabel('conflicts')
    plt.xticks(np.arange(0, max(x)+1, 2.0))
    plt.yticks(np.arange(min(y), max(y)+1, 1.0))

    r_dir = os.path.join(SCRIPT_DIR, img_output_dir)
    plt.savefig(os.path.join(r_dir,'hill_climbing_reduced.png'))
    plt.show()
    plt.close()
    
def plot_2D_grid_sa(x, y, img_output_dir):
    plt.plot(x, y, 'b-')
    plt.title('Simulated Annealing')
    plt.xlabel('iterations')
    plt.ylabel('cost')
    plt.xticks(np.arange(0, 4000, 1000.0))
    plt.yticks(np.arange(0, 140, 20.0))

    r_dir = os.path.join(SCRIPT_DIR, img_output_dir)
    plt.savefig(os.path.join(r_dir,'simulated_annealing.png'))    
    plt.show()
    plt.close()
    
