#!/usr/bin/env python2.7
from typing import List

def solution(l, t): # type: (List[int], int) -> List[int]
    left = 0
    right = 0
    total = 0

    while (left <= len(l)):
        # If the right pointer goes through the entire array,
        # this means the sum of numbers in range [left, right] are less than t.
        # Break out of loop in this case.
        if right >= len(l):
            break

        total += l[right]

        if total == t:
            return [left, right]

        right += 1

        if total > t:
            left += 1
            right = left
            total = 0

    return [-1, -1]


# ============================ Official test-cases ============================
assert solution([1, 2, 3, 4], 15) == [-1, -1], 'solution([1, 2, 3, 4], 15) failed!'
assert solution([4, 3, 10, 2, 8], 12) == [2, 3], 'solution([4, 3, 10, 2, 8], 12) failed!'

# =========== My own, unofficial test cases to help debug behaviour ===========
assert solution([4, 3, 5, 7, 8], 12) == [0, 2], 'solution([4, 3, 5, 7, 8], 12) failed!'
assert solution([1, 2, 4, 3, 5, 7, 8], 12) == [2, 4], 'solution([1, 2, 4, 3, 5, 7, 8], 12) failed!'
assert solution([1, 12, 4], 12) == [1, 1], 'solution([1, 12, 4], 12) failed!'
