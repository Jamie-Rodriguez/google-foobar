#!/usr/bin/env python2.7
from typing import List, Tuple

# Note: Always representing abstract 'grid-coordinate' type by Tuple[int, int]

def neighbors(map, coord): # type: (List[List[int]], Tuple[int, int]) -> List[Tuple[int, int]]
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

def bfs(map, start, end):
    # type: (List[List[int]], Tuple[int, int], Tuple[int, int]) -> int
    # Tuples of (coordinate, number of steps taken so far, have we removed a wall yet?)
    open = [(start, 1, False)]

    # This map/dictionary should be a 2-D array,
    # since it is mapping from a 2D-coordinate -> *some data*.
    # But then I would have to initialise the 2D array to the correct sizing,
    # which I can't be bothered doing :^)

    # No support for enums here...
    NO_WALL = 0
    WALL = 1
    BOTH = 2
    # Records *how* the node was visited
    # This is important because we need to consider the case of the path having a wall in it, or not
    traversals = { start: NO_WALL }

    while open:
        (current, num_steps, been_through_wall) = open.pop()

        if current == end:
            return num_steps

        for next in neighbors(map, current):
            # Has 'next' previously been traversed
            # AND is 'next' the opposite of 'current'?
            if (next in traversals and traversals[next] in [NO_WALL, WALL]):
                if traversals[next] != (WALL if been_through_wall else NO_WALL):
                    traversals[next] = BOTH
                    been_through_wall_next = True if map[next[0]][next[1]] == WALL else been_through_wall
                    open.insert(0, (next, num_steps + 1, been_through_wall_next))
            elif next not in traversals:
                # If neighbour is a wall and we've already gone through a wall, skip
                if (map[next[0]][next[1]] == WALL
                        and been_through_wall):
                    continue

                if map[next[0]][next[1]] == WALL:
                    traversals[next] = WALL
                else:
                    traversals[next] = WALL if been_through_wall else NO_WALL

                been_through_wall_next = True if map[next[0]][next[1]] == WALL else been_through_wall
                open.insert(0, (next, num_steps + 1, been_through_wall_next))


def solution(map): # type: (List[List[int]]) -> int
    # Assumes 'map' is n rows, where each and every row is *always* m = len(map[0]) columns
    # As per Read-Me problem description
    num_rows = len(map)

    # Problem description in Read-Me:
    # "The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1)."
    start = (0, 0)
    # Not strictly necessary, but a little more safe
    end = (num_rows - 1, len(map[num_rows - 1]) - 1)

    return bfs(map, start, end)


# ============================ Official test-cases ============================
assert solution([[0, 1, 1, 0],
                 [0, 0, 0, 1],
                 [1, 1, 0, 0],
                 [1, 1, 1, 0]]) == 7, 'solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]) failed!'
assert solution([[0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1],
                 [0, 1, 1, 1, 1, 1],
                 [0, 0, 0, 0, 0, 0]]) == 11, 'solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]) failed!'

# =========== My own, unofficial test cases to help debug behaviour ===========
assert solution([[0, 0],
                 [0, 1]]) == 3, 'solution([[0, 0], [0, 1]]) failed!'
# Although the Read-Me states that "The map will always be solvable",
# It isn't too hard to account for this
assert solution([[0, 1],
                 [1, 1]]) == None, 'solution([[0, 1], [1, 1]]) failed!'
assert solution([[0, 1, 0],
                 [0, 1, 1],
                 [0, 1, 0]]) == 5, 'solution([[0, 1, 0], [0, 1, 1], [0, 1, 0]]) failed!'
assert solution([[0, 1, 1],
                 [0, 1, 0]]) == 4, 'solution([[0, 1, 1], [0, 1, 0]]) failed!'
assert solution([[0, 1, 0, 0, 0, 1],
                 [0, 0, 0, 1, 0, 0]]) == 7, 'solution([[0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0]]) failed!'
assert solution([[0, 1, 0, 0, 0],
                 [0, 1, 0, 1, 0],
                 [0, 0, 0, 1, 1],
                 [0, 0, 1, 1, 0]]) == 12, 'solution([0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 1, 1, 0]) failed!'
assert solution([[0, 0, 0, 0],
                 [1, 1, 1, 0],
                 [0, 0, 0, 0],
                 [0, 1, 0, 1],
                 [0, 0, 0, 0]]) == 8, 'solution([[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 0]]) failed!'
assert solution([[0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 1, 1, 0],
                 [0, 1, 1, 0, 0],
                 [0, 1, 1, 0, 0]]) == 9, 'solution([[0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 1, 1, 0, 0]]) failed!'
