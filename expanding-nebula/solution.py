#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# UTF-8 for the mathematical symbols in comments
from collections import defaultdict

'''
    I'm not sure if there's an intelligent way to backtrack through time,
    more efficient then brute-force

    Some preliminary calculations:
    Max grid size: 50 × 9
    Maximum possible states: 2 ^ (50 × 9)
        - very big number!
    As the solution can be up to 10^9, some memoisation will probably have to
    be used

    If g(t + 1) = True ("O")
    Possible states for g(t) = 4:
        O. .O .. ..
        .. .. O. .O

    If g(t + 1) = False (".")
    Possible states for g(t) = 12:
        .. OO O. O. .O .O .. .O O. OO OO OO
        .. .. O. .O O. .O OO OO OO .O O. OO

    For the next column in the same row we know it's possible states have to
    match their left column with the states of the right column of the previous
    coordinate

    e.g. if we have
        O.O
        .O.
        O.O
    g[0][0] previous possible states:
        O. .O .. ..
        .. .. O. .O
    now g[0][1] can only be:
        .. OO O. .O .O .. .O OO
        .. .. .O O. .O OO OO .O

    Ideas/Questions:
        - It may be more efficient to go down the shorter dimension though, as
          we know it will have a maximum of 9 rows.

        - This may help narrow down possible states earlier than going across
          the rows, which can be up to 50.

        - Could using a bitmap representation help?

        - The readme calculates the possibilities using horizontal and vertical
          reflections - is this always true? Could we use it to save
          time/memory?
            - Maybe it is true, but isn't practical as you will get the
              reflections on the bruteforce pass anyway

    The plan:
      1. Generate all permutations of the first column, save the columns as
         binary-encoded numbers
         - Note that each column of size c generates a c + 1 × 2 vector
      2. Generate all possible columns (c + 1 × 2) of the second column
         - Don't include the columns that don't match
           - Match right column preimage of left column with left column of the
             right preimage
      3. Continue 1. and 2., working from left to right
'''

def transpose(m): # type: (list[list[int]]) -> list[list[int]]
    return map(list, zip(*m))

# Can take list[bool] or list[0 | 1]
# col: list[0 | 1]
# Example: [False, False, True, False] -> 0b0100 = 4
def column_to_int(col): # type: (list[bool]) -> int
    result = 0

    for i, gas in enumerate(col):
        result |= ((1 if gas else 0 )<< i)

    return result

POSSIBLE_PREIMAGES = {
    True: [
        [[1, 0],
         [0, 0]],
        [[0, 1],
         [0, 0]],
        [[0, 0],
         [1, 0]],
        [[0, 0],
         [0, 1]]
    ],
    False: [
        [[0, 0],
         [0, 0]],
        [[1, 1],
         [0, 0]],
        [[1, 0],
         [1, 0]],
        [[1, 0],
         [0, 1]],
        [[0, 1],
         [1, 0]],
        [[0, 1],
         [0, 1]],
        [[0, 0],
         [1, 1]],
        [[0, 1],
         [1, 1]],
        [[1, 0],
         [1, 1]],
        [[1, 1],
         [0, 1]],
        [[1, 1],
         [1, 0]],
        [[1, 1],
         [1, 1]]
    ]
}

# Input: bitmap-encoded column
# Output: column, previous column state -> next neighbour column of previous column state
# The columns are encoded as a bitmap representation, contained inside an int
# i.e. column .0.. -> 0b0100 = 4
def create_possible_column_pairs(column): # type: (list[int]) -> dict[tuple[int, int], list[int]]
    # A 'column pair' is a pair of columns, the left one being the source
    # column, and the right one being the possible right-side neighbour column
    possible_column_pairs = []

    for i, gas in enumerate(column):
        new_cols = []
        # Consider rewriting to use bitwise operations instead
        # Might be harder to understand though
        if i == 0:
            new_cols = POSSIBLE_PREIMAGES[gas]
        else:
            for pcp in possible_column_pairs:
                for p in POSSIBLE_PREIMAGES[gas]:
                    if pcp[-1] == p[0]:
                        new_cols.append(pcp + [ p[1] ])

        possible_column_pairs = new_cols

    list_of_possible_column_pairs = []

    for col_pair in possible_column_pairs:
        list_of_possible_column_pairs.append(
            list(map(column_to_int, transpose(col_pair))))

    # Now we have a list of all possible previous columns (shape: n + 1, 2)
    # Encode the data into a map
    # (postimage column, preimage left column) -> preimage right column
    possible_columns_encoded_map = {}
    for pair in list_of_possible_column_pairs:
        key = (column_to_int(column), pair[0])
        value = pair[1]

        if key in possible_columns_encoded_map:
            possible_columns_encoded_map[key].append(value)
        else:
            possible_columns_encoded_map[key] = [value]

    return possible_columns_encoded_map


def solution(g): # type: (list[list[bool]]) -> int
    # This is the transpose i.e. a list of columns
    list_of_columns = transpose(g)

    encoded_columns = list(map(column_to_int, list_of_columns))

    num_possibilities = 1 << ( len(g) + 1 )
    # (column, previous column state) -> next neighbour column of previous column state
    valid_possible_cols = defaultdict(set) # type: dict[int, set[list[int]]]

    # Construct the map
    for column in list_of_columns:
        pairs_map = create_possible_column_pairs(column)

        for k, v in pairs_map.items():
            valid_possible_cols[k].update(v)


    counts = { i: 1 for i in range(num_possibilities) }

    for column in encoded_columns:
        next_columns = defaultdict(int)
        for preimage_col in range(num_possibilities): # for every possible preimage
            for next_preimage_col in valid_possible_cols[(column, preimage_col)]: # every valid preimage for column
                next_columns[next_preimage_col] += counts[preimage_col]

        counts = next_columns

    return sum(counts.values())


# ============================ Official test-cases ============================
assert solution([[True, True, False, True, False, True, False, True, True, False],
                 [True, True, False, False, False, False, True, True, True, False],
                 [True, True, False, False, False, False, False, False, False, True],
                 [False, True, False, False, False, False, True, True, False, False]]) == 11567
assert solution([[True, False, True],
                 [False, True, False],
                 [True, False, True]]) == 4
assert solution([[True, False, True, False, False, True, True, True],
                 [True, False, True, False, False, False, True, False],
                 [True, True, True, False, False, False, True, False],
                 [True, False, True, False, False, False, True, False],
                 [True, False, True, False, False, True, True, True]]) == 254
