#!/usr/bin/env python3

# école supélec contrale - 2016 - c. dürr
# devoir maison 1 - connect
# www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect/

import sys
import time
from random import randint

from connect_with_tiles_connection import solve as solve_with_tiles_connection
from connect_with_tiles_orientation import solve as solve_with_tiles_orientation
from grid_samples import GRIDS


def generate():
    """Generates a random grid
    """
    # generate random connections, place 0 at the border
    lr = [[randint(0, 1) for j in range(n-1)] + [0] for i in range(n)]
    tb = [[randint(0, 1) for j in range(n)]  for i in range(n-1)]
    tb += [[0] * n]
    for i in range(n):
        for j in range(n):
            # encoding of the cell
            c = tb[i - 1][j] + 2*lr[i][j - 1] + 4*tb[i][j] + 8*lr[i][j]
            cc = c | (c << 4)
            # normalized orientation
            p = min((cc >> i) & 15 for i in range(4))
            print(hex(p)[-1], end='')
        print()


def read_line():
    return list(int(x, 16) for x in sys.stdin.readline().strip())


def read_grid():
    """reads a grid from stdin
    """
    grid = [read_line()]
    n = len(grid[0])
    for _ in range(n - 1):
        grid.append(read_line())
    return grid


# For the running time tests
def read_test_line(line):
    return list(int(x, 16) for x in line.strip())


# For the running time tests
def read_test_grid(grid):
    new_grid = []
    n = len(grid[0])
    for i in range(n):
        new_grid.append(read_test_line(grid[i]))
    return new_grid


def prettyprint(grid):
    """ reads a grid from stdin and pretty prints it.
    """
    n = len(grid)
    for i in range(n):
        # top row of cell
        for j in range(n):
            if grid[i][j] & 1:
                print("  x   ", end='')
            else:
                print("  -   ", end='')
        print()
        # center row of cell
        for j in range(n):
            if grid[i][j] & 2:
                print("x o", end='')
            else:
                print("- o", end='')
            if grid[i][j] & 8:
                print(" x ", end='')
            else:
                print(" - ", end='')
        print()
        # bottom row of cell
        for j in range(n):
            if grid[i][j] & 4:
                print("  x   ", end='')
            else:
                print("  -   ", end='')
        print()

def solve(grid, solve_type):
    if solve_type == "o":
        (grid_solution, is_unique) = solve_with_tiles_orientation(grid)
    elif solve_type == "c":
        (grid_solution, is_unique) = solve_with_tiles_connection(grid)
    if len(grid_solution) > 0:
        # Print solution
        prettyprint(grid_solution)
        for i in range(len(grid_solution)):
            print("".join(["%x" % grid_solution[i][j] for j in range(len(grid_solution))]))
        if is_unique:
            print("# la solution est unique")
        else:
            print("# la solution n'est pas unique")
    else:
        print("# il n'y a pas de solution")


def help():
    print("Usage: ./connect.py <arguments>")
    print("  -g <n>           to generate a grid of dimension n*n")
    print("  -p               to pretty print a grid given in stdin")
    print("  -s               to solve a grid given in stdin")
    print("  -t               to solve the grids in the sample file")


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == "-g":
        n = int(sys.argv[2])
        generate()
    elif len(sys.argv) == 2 and sys.argv[1] == "-p":
        prettyprint(read_grid())
    elif len(sys.argv) == 3 and sys.argv[1] == "-s":
        solve_type = sys.argv[2]
        solve(read_grid(), solve_type)
    elif len(sys.argv) == 2 and sys.argv[1] == "-t":
        solve(read_test_grid(grid), "o")
        solve(read_test_grid(grid), "c")
    else:
        help()

