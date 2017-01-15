#!/usr/bin/env python3

# école supélec contrale - 2016 - Mélanie Bérard
# devoir maison 1 - connect
# www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect/

# METHOD 2 : en introduisant des variables qui codent la présence de connecteurs sur le contact entre deux tuiles adjacentes

"""
         j = 0     j = 1     j = 2

             x0        x1        x2
            ----      ----      ----  
           |    |    |    |    |    | 
i = 0   x3 |    | x4 |    | x5 |    | x6
            ----      ----      ----  
             x7        x8        x9
            ----      ----      ----  
           |    |    |    |    |    | 
i = 1   x10|    | x11|    | x12|    | x13
            ----      ----      ----  
             x14       x15       x16
            ----      ----      ----  
           |    |    |    |    |    | 
i = 2   x17|    | x18|    | x19|    | x20 
            ----      ----      ----  
             x21       x22       x23
"""

from CentraleSupelec import CSP
from connect_with_common import PossibleTiles, rotate, CONNECTION


def top_index(i, j, n):
    """
    :param i: for i in [0, ..., n]
    :param j: for j in [0, ..., n - 1]
    """
    return (2*n + 1)*i + j


def left_index(i, j, n):
    """
    :param i: for i in [0, ..., n - 1]
    :param j: for j in [0, ..., n]
    """
    return (2*n + 1)*i + j + n


def solve(grid):
    n = len(grid)
    # Get the list of possible rotated tiles from common_connect.py
    possible_tiles = PossibleTiles()
    tiles = possible_tiles.values
    domains = create_unary_constraints(grid, n)
    P = CSP(domains)
    create_binary_constraints(grid, n, P)
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


def create_unary_constraints(grid, n):
    domains = [set(CONNECTION) for _ in range(2 * n * (n + 1))]
    for i in range(n):
        domains[left_index(i, 0, n)].discard(1)
        domains[left_index(i, n, n)].discard(1)
        for connection in CONNECTION:
            if not possible_rotation(grid[i][0], False, 2, bool(connection), 8):
                domains[left_index(i, 1, n)].discard(connection)
            if not possible_rotation(grid[i][n - 1], connection, 2, False, 8):
                domains[left_index(i, n - 1, n)].discard(connection)
    for j in range(n):
        domains[top_index(0, j, n)].discard(1)
        domains[top_index(n, j, n)].discard(1)
        for connection in CONNECTION:
            if not possible_rotation(grid[0][j], False, 1, bool(connection), 4):
                domains[top_index(1, j, n)].discard(connection)
            if not possible_rotation(grid[n - 1][j], connection, 1, False, 4):
                domains[top_index(n - 1, j, n)].discard(connection)
    return domains


def create_binary_constraints(grid, n, P):
    # Add row constraint 
    for i in range(n):
        for j in range(1, n - 1):
            left_connector = left_index(i, j, n)
            right_connector = left_index(i, j + 1, n)
            left_tile, tile, right_tile = grid[i][j - 1], grid[i][j], grid[i][j + 1]
            relations = left_right_relations(left_tile, tile, right_tile)
            P.addConstraint(left_connector, right_connector, relations)
    # Add column constraint
    for i in range(1, n - 1):
        for j in range(n):
            top_connector = top_index(i, j, n)
            bottom_connector = top_index(i + 1, j, n)
            top_tile, tile, bottom_tile = grid[i - 1][j], grid[i][j], grid[i + 1][j]
            relations = top_bottom_relations(top_tile, tile, bottom_tile)
            P.addConstraint(top_connector, bottom_connector, relations)
    # Add inside tile constraint
    for i in range(n):
        for j in range(n):
            tile = grid[i][j]
            top = top_index(i, j , n)
            left = left_index(i, j, n)
            bottom = top_index(i + 1, j , n)
            right = left_index(i, j + 1, n)
            positions = [[1, 2], [2, 4], [4, 8], [8, 1]]
            connectors = [[top, left], [left, bottom], [bottom, right], [right, top]]
            for k in range(len(positions)):
                relations = consecutive_sides_relations(tile, positions[k][0], positions[k][1])
                P.addConstraint(connectors[k][0], connectors[k][1], relations)


def possible_rotation(tile, constraint_1, position_1, constraint_2, position_2):
    """
    :param constraint: True or False (correspond to a connection bit equal to 1 or 0) 
    :param position: at this position the tile must have a connection equal to constraint
    :return bool: True or False
    """
    possible_tiles = PossibleTiles()
    for rotated_tile in possible_tiles.values[tile]:
        if (rotated_tile & position_1 > 0) == constraint_1 and\
            (rotated_tile & position_2 > 0) == constraint_2:
            return True
    return False


def possible_connection_between_tiles(tile_1, tile_2, position_1, position_2, constraint):
    possible_tiles = PossibleTiles()
    for rotated_tile_1 in possible_tiles.values[tile_1]:
        if (rotated_tile_1 & position_1 > 0) == constraint:
            for rotated_tile_2 in possible_tiles.values[tile_2]:
                if (rotated_tile_2 & position_2 > 0) == constraint:
                  return True
    return False


def left_right_relations(left_tile, tile, right_tile):
    relations = set([])
    for left_connection in CONNECTION:
        if possible_connection_between_tiles(left_tile, tile, 8, 2, bool(left_connection)):
            for right_connection in CONNECTION:
                if possible_rotation(tile, bool(left_connection), 2, bool(right_connection), 8):
                    relations.add((left_connection, right_connection))
    return relations

def top_bottom_relations(top_tile, tile, bottom_tile):
    relations = set([])
    for top_connection in CONNECTION:
        if possible_connection_between_tiles(top_tile, tile, 4, 1, bool(top_connection)):
            for bottom_connection in CONNECTION:
                if possible_rotation(tile, bool(top_connection), 1, bool(bottom_connection), 4):
                    relations.add((top_connection, bottom_connection))
    return relations


def consecutive_sides_relations(tile, position_1, position_2):
    relations = set([])
    for connection_1 in CONNECTION:
        for connection_2 in CONNECTION:
            if possible_rotation(tile, bool(connection_1), position_1, bool(connection_2), position_2):
                relations.add((connection_1, connection_2))
    return relations


def solution_to_grid(solution, grid, tiles, n):
    output = []
    for i in range(n):
        row = []
        for j in range(n):
            tile  = 1 * solution[top_index(i, j, n)]
            tile += 2 * solution[left_index(i, j, n)]
            tile += 4 * solution[top_index(i + 1, j, n)]
            tile += 8 * solution[left_index(i, j + 1, n)]
            row.append(tile)
        output.append(row)
    return output

