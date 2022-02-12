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
import heapq
import pdb
import logging
from shutil import move
import sys

log = logging.getLogger(__name__)

"""
Notes:
    - use NumPy package
    - standard packages allowed
    - tree search or graph search?

Approach for astar_search():
    - 1. start at goal state
    - 2. perform tree search, expanding towards all NON-VISITED possible 
        states
        -> Expand the top most element in the expanded priority queue
        - if a visited state is encountered, with lower f(n) value, replace
    - 3. maintain priority queue of expanded state, popping the lowest
        f(n) valued one at each iteration and adding to visited
    - 4. maintain map of visited states
    - 5. f(n) = g(n) + h(n)
        - g(n) = path cost, h(n) = Manhattan distance
    - 6. Function ends when goal state is added to visited map

    ERROR:
        - you are only supposed to add child states if they
            were not explored and not in expanded
        - if child state is in expanded w/ higher cost than
            new child state, then replace
        -> YOU FUCKING IDIOT! YOU MESSED UP THE ORDER OF THE 
            OF THE LIST.
"""

"""
Approach for IDA*:
    - for each smallest f-cost exceeding the current cutoff cost value
        until the goal is found:
        - 1. Expand the nodes of the current root
        - 2. If an expanded node exceeds the cutoff, do not add it to the
            frontier queue
            - record the smallest expanded node cost
        - 3. Repeat until the frontier is empty and return the smallest
            exceeding cutoff

Revised approach:
    - until a solution is reached, keep calling search method (returns next_offset, goal_obj):
        curr_offset = max_offset
        goal_obj = None
        1. Check if current state is goal state
            a. Return None, goal_state if True
        2. If function cost of state is greater than curr_offset,
            curr_offset = state.fn
        3. Expand tree, for each new_state,
            a. If max_offset < new_state.fn < curr_offset,
                curr_offset = new_state.fn
            b. If new_state.fn <= max_offset,
                o,g = search()
                i. If max_offset < o < curr_offset
                    curr_offset = o
                ii. If g is not None and goal_obj is not None and g.fn < goal_obj.fn or g is not None
                        goal_obj = g
        4. Return curr_offset, goal_obj

    ERRORS:
        - Program never gets past searching the first node
            SOLUTION: fix offset incrementing section
        
"""

class GameState():
    """
    Game state object.

    Tests:
        >>> GameState.init_globals([1,8,7,2,0,6,3,4,5], [1,1,1,1])

        >>> a = GameState([1,8,7,2,0,6,3,4,5], 0)
        >>> a._GameState__get_manhattan_distance()
        0
    """
    move_cost_map = {}
    goal_state = None
    goal_coords = None
    index_map = {
            0: (0,0),
            1: (0,1),
            2: (0,2),
            3: (1,0),
            4: (1,1),
            5: (1,2),
            6: (2,0),
            7: (2,1),
            8: (2,2)
    }

    def __init__(self, state, direction=None, parent_state=None):
        """
        Initializes GameState object.

        Potential speedup: defining location of 0-index
        """
        self.state = state
        self.path_cost = 0
        self.parent_key = None
        if parent_state:
            # Assumption: if parent_state is defined, then so is direction
            self.path_cost = parent_state.get_path_cost() + GameState.move_cost_map[direction]
            self.parent_key = parent_state.get_key()
        self.direction = direction
        self.function_cost = self.path_cost + self.__get_manhattan_distance()

        # Find 0 index
        for i in range(len(self.state)):
            if self.state[i] == 0:
                self.zero_index = i
        self.zero_coord = self.__get_coordinate(self.zero_index)

    @classmethod
    def init_globals(cls, goal_state, move_cost):
        cls.move_cost_map = {
            "u": move_cost[0],
            "d": move_cost[1],
            "l": move_cost[2],
            "r": move_cost[3]
        }
        cls.goal_state = goal_state
        cls.goal_coords = {}
        for index in range(len(goal_state)):
            val = goal_state[index]
            cls.goal_coords[val] = GameState.__get_coordinate(index)

    @classmethod
    def __get_coordinate(cls, index):
        """
        Maps an index between 0-8 to an (x,y)-coordinate.
        """
        return GameState.index_map[index]

    def __get_manhattan_distance(self):
        dist = 0
        for index in self.state:
            val = self.state[index]
            curr_coord = self.__get_coordinate(index)
            goal_coord = GameState.goal_coords[val]
            dist += abs(curr_coord[0]-goal_coord[0]) + abs(curr_coord[1]-goal_coord[1])
        return dist
    
    def expand_tree(self):
        """
        Returns list of expanded nodes.

        Note: this chunk of code bothers me...
        """
        expanded_nodes = []
        if self.zero_coord[0] > 0:
            # Move left
            s_cpy = self.state.copy()
            s_cpy[self.zero_index], s_cpy[self.zero_index-3] = \
                s_cpy[self.zero_index-3], s_cpy[self.zero_index]
            expanded_nodes += [GameState(s_cpy, 'l', self)]
        if self.zero_coord[0] < 2:
            # Move right
            s_cpy = self.state.copy()
            s_cpy[self.zero_index], s_cpy[self.zero_index+3] = s_cpy[self.zero_index+3], s_cpy[self.zero_index]
            expanded_nodes += [GameState(s_cpy, 'r', self)]
        if self.zero_coord[1] > 0:
            # Move up
            s_cpy = self.state.copy()
            s_cpy[self.zero_index], s_cpy[self.zero_index-1] = s_cpy[self.zero_index-1], s_cpy[self.zero_index]
            expanded_nodes += [GameState(s_cpy, 'u', self)]
        if self.zero_coord[1] < 2:
            # Move down
            s_cpy = self.state.copy()
            s_cpy[self.zero_index], s_cpy[self.zero_index+1] = s_cpy[self.zero_index+1], s_cpy[self.zero_index]
            expanded_nodes += [GameState(s_cpy, 'd', self)]
        return expanded_nodes

    def get_key(self):
        """
        Potential improvement: use int instead of tuple
        """
        return tuple(self.state)
    
    def get_direction(self):
        return self.direction
    
    def get_state(self):
        return self.state
    
    def get_function_cost(self):
        return self.function_cost

    def get_path_cost(self):
        return self.path_cost

    def get_parent_key(self):
        return self.parent_key

    def __eq__(self, other):
        if not isinstance(other, GameState):
            raise NotImplementedError
        return self.function_cost == other.get_function_cost()

    def __gt__(self, other):
        if not isinstance(other, GameState):
            raise NotImplementedError
        return self.function_cost > other.get_function_cost()

    def __lt__(self, other):
        if not isinstance(other, GameState):
            raise NotImplementedError
        return self.function_cost < other.get_function_cost()

    def __str__(self):
        return f"{self.state}, path_cost: {self.path_cost}, f_n: {self.function_cost}, dir: {self.direction}\n"
    
    def __repr__(self):
        return str(self)


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
    GameState.init_globals(goal_state, move_cost)
    log.debug(f"move_map: {GameState.move_cost_map}")
    visited_map = {}
    expanded_map = {}
    expanded_queue = [GameState(init_state.copy(), direction=None, parent_state=None)]

    # For each root GameState in expanded_queue, expand and add new GameStates
    #   to expanded_queue
    root = expanded_queue[0]
    expanded_map[root.get_key()] = root
    while root.get_state() != goal_state:
        # Add root to visited and pop
        visited_map[root.get_key()] = heapq.heappop(expanded_queue)
        del expanded_map[root.get_key()]
        
        expanded_states = root.expand_tree()

        for state in expanded_states:
            state_key = state.get_key()     # get tuple of state list
            if state_key not in visited_map and state_key not in expanded_map:
                # Add new state to expanded queue (frontier)
                heapq.heappush(expanded_queue, state)
                expanded_map[state_key] = state
            elif state_key in expanded_map and expanded_map[state_key].get_function_cost() > state.get_function_cost():
                # Replace existing state in frontier w/ improved version
                expanded_queue.remove(expanded_map[state_key])
                expanded_map[state_key] = state
                expanded_queue.sort()   # lazy solution compared to "trickling down" swapped node
                                        # heapq API didn't include this functionality for some reason...
                heapq.heappush(expanded_queue, state)
        if init_state == [1,6,0,2,7,8,3,4,5]:
            #log.debug(f"root: {root}\nfrontier: {expanded_queue}\n")
            pass
        root = expanded_queue[0]

    log.debug(f"final root: {root}")
    path_string = ""
    curr_state = root
    if init_state == [1,6,0,2,7,8,3,4,5]:
        #pdb.set_trace()
        pass
    while curr_state.get_parent_key() is not None:
        path_string = curr_state.get_direction() + path_string
        curr_state = visited_map[curr_state.get_parent_key()]
    return path_string

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
    # if init_state == [1,8,7,3,0,2,4,5,6]:
    #     pdb.set_trace()
    GameState.init_globals(goal_state, move_cost)
    init_obj = GameState(init_state, direction=None, parent_state=None)
    offset = 0
    goal_obj = None
    while goal_obj is None:
        offset, goal_obj = search(init_obj, goal_state, offset)
    log.debug(goal_obj)

    return 0

def search(state_obj, goal_state, max_offset):
    """
    Searches for goal_state recursively and smallest
    function cost that exceeds max_offset
    """
    curr_offset = None
    goal_obj = None
    
    if state_obj.get_state() == goal_state:
        return max_offset, state_obj
    
    if state_obj.get_function_cost() > max_offset:
        curr_offset = state_obj.get_function_cost()
    
    for new_state in state_obj.expand_tree():
        fn = new_state.get_function_cost()
        if fn <= max_offset:
            o,g = search(new_state, goal_state, max_offset)
            if g is not None and goal_obj is not None and g.get_function_cost() < goal_obj.get_function_cost() \
                or g is not None:
                goal_obj = g
            if curr_offset is None or max_offset < o < curr_offset:
                curr_offset = o
        
        if curr_offset is None or max_offset < fn < curr_offset:
            curr_offset = fn

    return curr_offset, goal_obj

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
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(message)s')
    doctest.testmod()
    