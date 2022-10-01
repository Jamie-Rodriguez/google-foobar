#!/usr/bin/env python2.7
from collections import deque

'''
    Initial observations:
        - We essentially want the throughput of the graph (how many bunnies are
          exiting per timestep)
        - The example graph looks like:
            /---\  4   /---\  4   /---\
            | 0 | ---> | 2 | ---> | 4 |
            \---/      \---/      \---/
                 \     ^    \     ^
                   \  / 5     \  / 6
                     x          x
                   /  \ 6     /  \ 4
                 /     V    /     V
            /---\      /---\      /---\
            | 1 | ---> | 3 | ---> | 5 |
            \---/  2   \---/  6   \---/
        - Note that each node essentially has a capacity, which is the outflow
          rate
              Example: In the example graph, node 2 can only take in up to 8
                  bunnies per timestep as it can only output 4 bunnies to each
                  node 4 and 5 = 8 total
        - Is the best approach to work backwards from the outputs?

    Searching the internet shows this type of graph is called a "Flow Network"
        https://en.wikipedia.org/wiki/Flow_network
    "The simplest and most common problem using flow networks is to find what
     is called the maximum flow, which provides the largest possible total flow
     from the source to the sink in a given graph."

    |       Inventor(s)      | Year | Time complexity (with n nodes and m arcs) |
    |:----------------------:|:----:|:-----------------------------------------:|
    | Dinic's algorithm      | 1969 |                  O(m n^2)                 |
    | Edmonds-Karp algorithm | 1972 |                  O(m^2 n)                 |
    | MPM algorithm          | 1978 |                   O(n^3)                  |
    | James B. Orlin         | 2013 |                   O(m n)                  |

    In James B. Orlin's paper "Max flows in O(nm) time, or better", he has a
    more detailed table than the one on Wikipedia - but too big to put here.
    (Appendix B "Transferring residual capacities from paths", Table 1)

    After reading Orlin's paper, the algorithm looks to be dependant on the
    sparsity of the graph in question.

    Orlin's later 2019 paper "A Fast Max Flow Algorithm", confirms this:
        "In 2013, Orlin proved that the max flow problem could be solved in
         O(n*m) time. His algorithm ran in O(n*m + m^1.94) time, which was the
         fastest for graphs with fewer than n^1.06 arcs. If the graph was not
         sufficiently sparse, the fastest running time was an algorithm due to
         King, Rao, and Tarjan."

    I am not sure there are any guarantees about the sparsity of the graphs in
    question, though they *probably* will be sufficiently sparse. It may just
    be easier to choose a simpler algorithm...

    Assuming that the graph will be *somewhat* sparse, the Edmonds-Karp
    algorithm is the most efficient choice from the table above.

    It may be worth revisiting this with Orlin's algorithms in the future.

    We can simplify the algorithm by first transforming the graph into a
    single-source, single-sink graph by appending a "supersource" and
    "supersink" respectively i.e.
                     /---\  4   /---\  4   /---\
                     | 0 | ---> | 2 | ---> | 4 |
      infinity /---> \---/      \---/      \---/
              /           \     ^    \     ^     \ infinity
    /--------\              \  / 5     \  / 6     \---> /------\
    | source |                x          x              | sink |
    \--------/              /  \ 6     /  \ 4     /---> \------/
              \           /     V    /     V     / infinity
      infinity \---> /---\      /---\      /---\
                     | 1 | ---> | 3 | ---> | 5 |
                     \---/  2   \---/  6   \---/
'''


# Assumption: 'graph' is a square matrix
def add_supersource_and_supersink(sources, sinks, graph):
    # type: (list[int], list[int], list[list[int]]) -> list[list[int]]
    supersource = []
    supersink = []
    for i in range(len(graph) + 2):
        # Supersink should never link to anything
        supersink.append(0)

        if i - 1 in sources:
            supersource.append(float('inf'))
        else:
            supersource.append(0)

    new_graph = []
    for i in range(len(graph)):
        new_graph.append([])

        for j in range(len(graph) + 2):
            # No nodes should connect TO supersource
            if j == 0:
                new_graph[i].append(0)
            elif j == len(graph) + 1:
                # Connect exits to supersink
                if i in sinks:
                    new_graph[i].append(float('inf'))
                else:
                    new_graph[i].append(0)
            # Else copy over previous connections
            else:
                # j - 1 because of the offset caused by the addition of the
                # supersource
                new_graph[i].append(graph[i][j - 1])

    new_graph.insert(0, supersource)
    new_graph.append(supersink)

    return new_graph

# Modifies 'previous_node'!
def breadth_first_search(graph, source, sink, previous_node):
    # type: (list[list[int]], int, int, list[int]) -> bool

    # Mutable state
    visited = [False] * len(graph)
    queue = deque()

    # Start search from source
    queue.appendleft(source)
    visited[source] = True

    while queue:
        current_node = queue.pop()

        for index, value in enumerate(graph[current_node]):
            # Easy way to check for neighbouring nodes: value > 0
            if (visited[index] == False) and (value > 0):
                queue.appendleft(index)
                visited[index] = True
                previous_node[index] = current_node

    # Did we reach the sink?
    return visited[sink]

# Modifies 'graph'!
def edmonds_karp(graph, source, sink):
    # type: (list[list[int]], int, int) -> int
    previous_node = [-1] * len(graph) # Mutated by breadth_first_search()
    max_flow = 0

    # While we can reach 'sink' from 'source'
    while breadth_first_search(graph, source, sink, previous_node):
        path_flow = float('Inf')

        # Get the maximum flow possible through the path - which is limited by
        # the minimum flow value along the path...
        # AKA the bottleneck
        curr_node = sink
        while curr_node != source:
            prev_node = previous_node[curr_node]
            path_flow = min(path_flow, graph[prev_node][curr_node])
            curr_node = prev_node

        max_flow += path_flow

        # Update the capacities:
        # Subtract the bottleneck flow from the forward-path
        # This ensures next time we search, we will find a path with a strictly
        # larger bottleneck.
        # However, we also *add* the bottleneck to the reverse-path. This
        # allows the next search to find alternative paths and redistribute the
        # flow optimally by "exchanging" flow from one edge to another when
        # travelling across a reverse edge.
        # Visual explanation at:
        # https://cp-algorithms.com/graph/edmonds_karp.html#ford-fulkerson-method
        # Where "larger bottleneck" means a path with a higher
        current = sink
        while current != source:
            prev_node = previous_node[current]
            graph[prev_node][current] -= path_flow
            graph[current][prev_node] += path_flow
            current = prev_node

    return max_flow

def solution(entrances, exits, path):
    # type: (list[int], list[int], list[list[int]]) -> int
    graph = add_supersource_and_supersink(entrances, exits, path)

    return edmonds_karp(graph, 0, len(graph) - 1)


# ============================ Official test-cases ============================
assert solution([0],
                [3],
                [[0, 7, 0, 0],
                 [0, 0, 6, 0],
                 [0, 0, 0, 8],
                 [9, 0, 0, 0]]) == 6, "solution(...) == 6 failed!"
assert solution([0, 1],
                [4, 5],
                [[0, 0, 4, 6, 0, 0],
                 [0, 0, 5, 2, 0, 0],
                 [0, 0, 0, 0, 4, 4],
                 [0, 0, 0, 0, 6, 6],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]) == 16, "solution(...) == 16 failed!"
