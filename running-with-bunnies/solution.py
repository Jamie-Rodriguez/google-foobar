#!/usr/bin/env python2.7
from copy import deepcopy
from itertools import permutations

'''
    Example graph visualised:
    This was difficult to draw - I couldn't put arrows so the convention is for
    a bidirectional graph between nodes A and B seen below:
                3
            ----->                                     3
        (A)        (B)    Is expressed as:    (A) ------ (B)
            <-----                                5
              5
    i.e. the weight/cost is placed closer to the destination node.

                          (start)
                      9 ..---n---.. 9
                   .--""'   / \   '""--.
                 ."      9 |   | 9      ".
               ."          |   |          ".
            2 /           /     \           \ 2
             /  3        |       |        2  \
        (0) .------------+-------+------------. (1)
           .'`--.       /         \       .--' .
         3 :  3  ".    |           |    ."  2  ; 2
           |       "-. |           | .-"       |
           |          )-.         .-(          |
           "         |   ".     ."   |         "
            \       /      "-.-"      \       /
            ".     |      .-' '-.      |     ."
             \   2 |    ."       ".    | -1  /
           2  \   /  .-"           "-.  \   / -1
               ".|.-"  2          -1  "-.|."
             (2) ".                     ." (bulkhead)
                 2 "--..           ..--" -1
                       '""-------""'

    It's not clear if the test graphs could have disconnected edges or they
    will *always* be complete digraphs...
    From the wording it seems implied the graphs will always be complete
    digraphs but it is not explicit.
    If not, how is a disconnected edge expressed? Infinity? -1? None?

    One immediately obvious thing to check for - if the graph has negative
    cycles, then we can just gather infinite time and it is possible to rescue
    all bunnies! Easy case!

    Otherwise, next we need to find the shortest paths to/from each and every
    combination of nodes...

    The Bellman-Ford algorithm is able to detect negative cycles, but it won't
    give us all shortest-distances for *all* node combinations - only for a
    single source node :( we would have to run Bellman-Ford on all nodes.

    I found that Floyd-Warshall algorithm can do this though. It looks quite
    simple to implement too.

    Floyd-Warshall can detect negative cycles in it's inner loop by checking
    for negative numbers on the diagonal of the path matrix
    https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm#Behavior_with_negative_cycles

    General idea:
        1. Run Floyd-Warshall on graph to set shortest time from/to every node
           combination
        2. If negative cycles are detected, we can rescue all bunnies and are
           finished.
        3. If not, we need to do an exhaustive search to find which path
           rescues the most bunnies:
               - Get all possible permutations of all possible subsets of
                 bunnies, returning the largest set i.e. the most bunnies that
                 we can save
               - This is fine as the problem statements says:
                     > There are at most 5 bunnies...

    I still think there may be a smarter way to search step 3. I could not come
    up with a more efficient search myself and couldn't find a definitive
    answer either way.
    Maybe you could marginally improve search by using a depth-first search to
    explore the permutations and prune combinations as soon as they are found
    to be invalid (exceed the time limit).
    But would be the same time complexity.
'''


# Assumption: 'graph' is a square matrix
def floyd_warshall(graph): # type: (list[list[int]]) -> list[list[int]] | None
    # The total value/"distance" of taking the shortest path from
    # distances[source][target]
    distances = deepcopy(graph)
    n = len(graph) # number of vertices
    # For next_node[source][target] = node,
    # The fastest way from 'source' to 'target' is by taking 'node'
    next_node = [[None for _ in range(n)] for _ in range(n)]

    # Initialise with just going directly to the target node
    # If an alternative, shorter path is found, it will be updated
    for i in range(n):
        for j in range(n):
            if i == j: # Don't initialise the diagonal
                next_node[i][j] = None
            # See above note, it's not clear if we can assume all graphs will
            # be complete digraphs...
            # If not, it's not given how a disconnected edge is expressed
            # either...
            # I will assume it's by the value Infinity
            elif graph[i][j] == float('inf'):
                next_node[i][j] = -1
            else:
                next_node[i][j] = j

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    next_node[i][j] = next_node[i][k]
            # Negative cycle
            if distances[i][i] < 0:
                return None

    return distances


def solution(times, times_limit): # type: (list[list[int]], int) -> list[int]
    shortest_times = floyd_warshall(times)
    num_bunnies = len(times) - 2
    # Just to make the code easier to read
    start = 0
    bulkhead = len(times) - 1

    # Negative cycles present - we can rescue all bunnies
    if not shortest_times:
        return list(range(num_bunnies))

    '''
        We must exhaustively test *all permutations* of *all subsets* of
        bunnies :'(
        i.e. every single possible bunny path permutation
        Might be able to do this (a little) more efficiently by using depth-first
        search to explore all permutations, but stop searching a path further if
        we already exceed the time limit.
        But problem states:
            > There are at most 5 bunnies...
        So it's worth it just to do this a simpler yet more inefficient way
    '''
    # reverse() so that we can get the largest subset of bunnies first and exit
    for subset_size in reversed(range(1, num_bunnies + 1)):
        for bunnies in permutations(range(1, num_bunnies + 1), r=subset_size):
            time_elapsed = 0

            # for i in range(len(bunnies)):
            for i, bunny in enumerate(bunnies):
                if i == 0: # go from start -> bunny(i)
                    time_elapsed += shortest_times[start][bunny]
                else:
                    time_elapsed += shortest_times[bunnies[i - 1]][bunny]

            # go from last bunny -> bulkhead
            time_elapsed += shortest_times[bunnies[-1]][bulkhead]

            if time_elapsed <= times_limit:
                # Bunnies are offset by 1 in the adjacency matrix
                return sorted(list(bunny - 1 for bunny in bunnies))

    # If we hit here, there is no solution
    # None can be saved :(
    return []


# ============================ Official test-cases ============================
assert solution([[0, 2, 2, 2, -1],
                 [9, 0, 2, 2, -1],
                 [9, 3, 0, 2, -1],
                 [9, 3, 2, 0, -1],
                 [9, 3, 2, 2, 0]],
                1) == [1, 2]
assert solution([[0, 1, 1, 1, 1],
                 [1, 0, 1, 1, 1],
                 [1, 1, 0, 1, 1],
                 [1, 1, 1, 0, 1],
                 [1, 1, 1, 1, 0]],
                3) == [0, 1]
