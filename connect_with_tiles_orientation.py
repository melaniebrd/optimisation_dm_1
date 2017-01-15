#!/usr/bin/env python3

# école supélec contrale - 2016 - Mélanie Bérard
# devoir maison 1 - connect
# www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect/

# METHOD 1 : en introduisant des variables qui codent les orientation des tuiles

from CentraleSupelec import CSP
from connect_with_common import PossibleTiles, rotate, ROTATIONS, NUMBER_OF_ROTATION


def solve(grid):
    n = len(grid)
    # Get the list of possible rotated tiles from connect_with_common.py
    possible_tiles = PossibleTiles()
    tiles = possible_tiles.values
    domains = create_unary_constraints(grid, tiles, n)
    P = CSP(domains)
    create_binary_constraints(grid, tiles, n, P)
    # Find the solutions with the CSP class
    solutions = P.solve()
    # print the output
    first_solution = next(solutions, None)
    solution_grid = []
    is_unique = True
    if first_solution:
        solution_grid = solution_to_grid(first_solution, grid, tiles, n)
        if next(solutions, None):
            is_unique = False
    return (solution_grid, is_unique)


def create_unary_constraints(grid, tiles, n):
    domains = [set(ROTATIONS) for _ in range(n * n)]
    # Top and bottom row unary constraints
    for j in range(n):
        for rotation in ROTATIONS:
            if has_connector_at_position(tiles[grid[0][j]], rotation, 1):
                domains[j].discard(rotation)
            if has_connector_at_position(tiles[grid[n - 1][j]], rotation, 4):
                domains[n*(n-1) + j].discard(rotation)
    # Left and right column unary constraints
    for i in range(n):
        for rotation in ROTATIONS:
            if has_connector_at_position(tiles[grid[i][0]], rotation, 2):
                domains[n*i].discard(rotation)
            if has_connector_at_position(tiles[grid[i][n - 1]], rotation, 8):
                domains[n*i + n - 1].discard(rotation)
    return domains


def create_binary_constraints(grid, tiles, n, P):
    # Add all the binary constraints into P using P.addConstraint(...)
    for i in range(n):
        for j in range(n):
            # Find the possible rotations for the tile (i, j)
            if(j != n - 1):
                left_tile = tiles[grid[i][j]]
                right_tile = tiles[grid[i][j+1]]
                # Rotation to connect the tile and the one on the right side
                relation = {(lr, rr) for lr in ROTATIONS for rr in ROTATIONS if left_right_connected(left_tile, right_tile, lr, rr)}
                #print("i = %s -- j = %s -- relations left-right = %s" % (i, j, relation))
                P.addConstraint(i*n + j, i*n + j + 1, relation)
            if(i != n - 1):
                top_tile = tiles[grid[i][j]]
                bottom_tile = tiles[grid[i + 1][j]]
                # Rotation to connect the tile and the one at the bottom
                relation = {(tr, br) for tr in ROTATIONS for br in ROTATIONS if top_bottom_connected(top_tile, bottom_tile, tr, br)}
                #print("i = %s -- j = %s -- relations top-bottom = %s" % (i, j, relation))
                P.addConstraint(i*n + j, (i+1)*n + j, relation)


def has_connector_at_position(tile, rotation, position):
    """
    :param rotation: number in [0, 1, 2, 3]
    :param position: number in [1, 2, 4, 8]
    """
    return tile[rotation] & position > 0

def left_right_connected(left_tile, right_tile, left_rotation, right_rotation):
    """
    Checks if with left_rotation and right_rotation, the left_tile and right_tile are connected by a 0 or 1
    :param left_tile, right_tile: ex [1, 2, 4, 8] list of tiles values after 0, 1, 2 and 3 rotations 
    :param left_rotation, right_rotation: number in [0, 1, 2, 3]
    """
    return not (has_connector_at_position(left_tile, left_rotation, 8) != has_connector_at_position(right_tile, right_rotation, 2))

def top_bottom_connected(top_tile, bottom_tile, top_rotation, bottom_rotation):
    """
    Checks if with top_rotation and bottom_rotation, the top_tile and bottom_tile are connected by a 0 or 1
    :param top_tile, bottom_tile: ex [1, 2, 4, 8] list of tiles values after 0, 1, 2 and 3 rotations 
    :param ltop_rotation, bottom_rotation: number in [0, 1, 2, 3]
    """
    return not (has_connector_at_position(top_tile, top_rotation, 4) != has_connector_at_position(bottom_tile, bottom_rotation, 1))

def solution_to_grid(solution, grid, tiles, n):
    output = [[tiles[grid[i][j]][solution[i*n+j]] for j in range(n)] for i in range(n)]
    return output


