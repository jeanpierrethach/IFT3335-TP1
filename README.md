# IFT3335-TP1

Implementation of search problems heuristics for Sudoku.

Authors: Jean-Pierre T., Sofiene F. *- University of Montreal*

## Setup
#### Dependencies:
* Python 3.5+
* Python packages: numpy, matplotlib

## Usage
### Basic Usage

1. Run the command with specific arguments:
```
python main.py <arguments>
```
*Example*:
```
python main.py --heuristic hcr
```

#### Arguments
* `--heuristic`: Heuristics for search problems. hc = Hill Climbing, hcr = Hill Climbing reduced, sa = Simulated Annealing. *Example*: `--heuristic hc`
* `--filename`: Filename containing sequence of 81 digits. *Default*: `100sudoku.txt`
* `--verbose`: Boolean flag indicating if statements should be printed to the console. (Optional)

## References

The project includes the work of Peter Norvig:

Solve Every Sudoku Puzzle
#### http://norvig.com/sudoku.html

