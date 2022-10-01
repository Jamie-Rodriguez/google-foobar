#!/usr/bin/env python2.7
from typing import List, Tuple, Optional
from collections import deque

def neighbors(map, coord):
    # type: (List[List[int]], Tuple[int, int]) -> List[Tuple[int, int]]
    adjacent = []

    # The problem definition in Read-Me states:
    # "The height and width of the map can be from 2 to 20."
    if coord[0] > 0:
        adjacent.append((coord[0] - 1, coord[1]))
    if coord[0] < len(map) - 1:
        adjacent.append((coord[0] + 1, coord[1]))
    if coord[1] > 0:
        adjacent.append((coord[0], coord[1] - 1))
    if coord[1] < len(map[coord[0]]) - 1:
        adjacent.append((coord[0], coord[1] + 1))

    return adjacent

def bfs(map, num_walls):
    # type: (List[List[int]], int) -> Optional[int]
    # Assumes 'map' is n rows, where each and every row is *always*
    # m = len(map[0]) columns
    # i.e. a square matrix, and not a staggered array of arrays
    # As per Read-Me problem description
    num_rows = len(map)
    # Not strictly necessary, but a little more safe
    num_columns = len(map[num_rows - 1])
    # Problem description in Read-Me:
    # "The door out of the station is at the top left (0,0) and the door into
    # an escape pod is at the bottom right (w-1,h-1)."
    start = (0, 0)
    end = (num_rows - 1, num_columns - 1)

    # The current, minimum number of walls we have gone through to reach
    # arbitrary square: wall_count_last_visit[r][c].
    # We initialise all squares to 'num_walls' so that the search will
    # then prioritise going through *less* walls than this number,
    # and conversely will never go through more walls than this number
    wall_count_last_visit = [[num_walls for _ in range(num_columns)] for _ in range(num_rows)]
    # Tuples of
    #     (coordinate, number of walls we have gone through, number of steps taken so far)
    queue = deque()
    queue.appendleft((start, 0, 0))

    while queue:
        (current, current_wall_count, num_steps) = queue.pop()
        (current_row, current_column) = current

        if map[current_row][current_column] == 1:
            current_wall_count += 1

        # If current_wall_count > num_walls, then we've gone through too many walls!
        if current == end and current_wall_count <= num_walls:
            return num_steps + 1

        for (next_row, next_column) in neighbors(map, current):
            # Did we find a new path that goes through less walls than our search so far?
            if current_wall_count <= wall_count_last_visit[next_row][next_column]:
                wall_count_last_visit[next_row][next_column] = current_wall_count
                queue.appendleft(((next_row, next_column), current_wall_count, num_steps + 1))

    # I made this case return None, but if we wanted to strictly adhere to the
    # type signature
    #     def solution(map): (List[List[int]]) -> int
    # Then we could return -1 or 0 or something instead
    # The problem definition already states that all mazes are solvable anyway
    # (see
    #     > The map will always be solvable,
    #     > though you may or may not need to remove a wall.
    # ),
    # so this case will not even be tested...
    return None

def solution(map): # type: (List[List[int]]) -> int
    num_walls = 1 # How many walls we are allowed to remove
    return bfs(map, num_walls)


# ============================ Official test-cases ============================
assert solution([[0, 1, 1, 0],
                 [0, 0, 0, 1],
                 [1, 1, 0, 0],
                 [1, 1, 1, 0]]) == 7
assert solution([[0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1],
                 [0, 1, 1, 1, 1, 1],
                 [0, 0, 0, 0, 0, 0]]) == 11

# =========== My own, unofficial test cases to help debug behaviour ===========
assert solution([[0, 0],
                 [0, 1]]) == 3
# Although the Read-Me states that "The map will always be solvable",
# It isn't too hard to account for this
assert solution([[0, 1],
                 [1, 1]]) == None
assert solution([[0, 1, 0],
                 [0, 1, 1],
                 [0, 1, 0]]) == 5
assert solution([[0, 1, 1],
                 [0, 1, 0]]) == 4
assert solution([[0, 1, 0, 0, 0, 1],
                 [0, 0, 0, 1, 0, 0]]) == 7
assert solution([[0, 1, 0, 0, 0],
                 [0, 1, 0, 1, 0],
                 [0, 0, 0, 1, 1],
                 [0, 0, 1, 1, 0]]) == 12
assert solution([[0, 0, 0, 0],
                 [1, 1, 1, 0],
                 [0, 0, 0, 0],
                 [0, 1, 0, 1],
                 [0, 0, 0, 0]]) == 8
assert solution([[0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 1, 1, 0],
                 [0, 1, 1, 0, 0],
                 [0, 1, 1, 0, 0]]) == 9
