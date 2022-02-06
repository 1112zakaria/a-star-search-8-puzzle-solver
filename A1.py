#!/usr/bin/env python3
####################################################
# COMP3106 - Introduction to Artificial Intelligence
# Assignment 1

# February 2022, Zakaria Ismail

# Copyright (c) 2022 by Cisco Systems, Inc. 
# All rights reserved.
####################################################

# Libraries
import doctest
import pandas

"""
Notes:
    - use NumPy package
    - standard packages allowed
"""

def astar_search(init_state, goal_state, move_cost) -> str:
    """
    Solves eight-puzzle problem of a 3x3 board using A* search.

    Args:
        - init_state ('List[str]'): initial state list
        - goal_state ('List[str]'): goal state list
        - move_cost ('List[int]'): cost list of the four moves
    Returns:
        - optimal_path ('str'): string describing optimal path
            of the 'blank square'
    Tests:
        >>> astar_search([0,8,7,1,2,6,3,4,5], [1,8,7,2,0,6,3,4,5],[1,1,1,1])
        'rd'
        >>> astar_search([1,8,7,3,0,2,4,5,6], [1,8,7,2,0,6,3,4,5], [1,1,1,1])
        'druuld'
        >>> astar_search([1,6,0,2,7,8,3,4,5], [1,8,7,2,0,6,3,4,5], [1,1,2,2])
        'urdlur'
        >>> astar_search([1,6,0,2,7,8,3,4,5], [1,8,7,2,0,6,3,4,5], [3,3,1,1])
        'ruldru'
        >>> astar_search([8,0,7,1,4,3,2,5,6], [1,8,7,2,0,6,3,4,5], [1,1,1,1])
        'urddrulurdl'
        >>> astar_search([8,0,7,1,4,3,2,5,6], [1,8,7,2,0,6,3,4,5], [1,1,2,2])
        'urddrulurdl'
    """
    return 0

def id_astar_search(init_state, goal_state, move_cost) -> str:
    """
    Solves eight-puzzle problem of a 3x3 board using iterative
    deepening A* search.

    Args:
        - init_state ('List[str]'): initial state list
        - goal_state ('List[str]'): goal state list
        - move_cost ('List[int]'): cost list of the four moves
    Returns:
        - optimal_path ('str'): string describing optimal path
            of the 'blank square'
    Tests:
        >>> id_astar_search([0,8,7,1,2,6,3,4,5], [1,8,7,2,0,6,3,4,5],[1,1,1,1])
        'rd'
        >>> id_astar_search([1,8,7,3,0,2,4,5,6], [1,8,7,2,0,6,3,4,5], [1,1,1,1])
        'druuld'
        >>> id_astar_search([1,6,0,2,7,8,3,4,5], [1,8,7,2,0,6,3,4,5], [1,1,2,2])
        'urdlur'
        >>> id_astar_search([1,6,0,2,7,8,3,4,5], [1,8,7,2,0,6,3,4,5], [3,3,1,1])
        'ruldru'
        >>> id_astar_search([8,0,7,1,4,3,2,5,6], [1,8,7,2,0,6,3,4,5], [1,1,1,1])
        'urddrulurdl'
        >>> id_astar_search([8,0,7,1,4,3,2,5,6], [1,8,7,2,0,6,3,4,5], [1,1,2,2])
        'urddrulurdl'
    """
    return 0

if __name__ == "__main__":
    header = """
    ####################################################
    # COMP3106 - Introduction to Artificial Intelligence
    # Assignment 1

    # February 2022, Zakaria Ismail

    # Copyright (c) 2022 by Cisco Systems, Inc. 
    # All rights reserved.
    ####################################################
    """
    print(header)
    doctest.testmod()
    