#!/usr/bin/env python2.7

'''
    Manually calculating the stair combinations for integer 3 <= n <= 9
    n = 3, solution(3) = 1, {2, 1}
    n = 4, solution(4) = 1, {3, 1}
    n = 5, solution(5) = 2, {4, 1}, {3, 2}
    n = 6, solution(6) = 3, {5, 1}, {4, 2}, {3, (3) -> {2, 1}}
    n = 7, solution(7) = 4, {6, 1}, {5, 2}, {4, 3}, {4, (3) -> {2, 1}}
    n = 8, solution(8) = 5, {7, 1}, {6, 2}, {5, 3}, {5, (3) -> {2, 1}}, {4, (4) -> {3, 1}}
    n = 9, solution(9) = 7, {8, 1}, {7, 2}, {6, 3}, {5, 4}, {5, (4) -> {3, 1}}, {4, (5) -> {3, 2}}
'''
'''
    This problem is called counting the 'partitions with distinct parts'
    https://en.wikipedia.org/wiki/Partition_(number_theory)#Odd_parts_and_distinct_parts
    From http://oeis.org/A008289
        Q(n, k) = Q(n-k, k) + Q(n-k, k-1)
            for n>k>=1, with Q(1, 1)=1, Q(n, 0)=0 (n>=1).
    - Paul D. Hanna, Mar 04 2005

    We need to subtract 1 from the total because this formula also includes the partition {n},
    which in the problem definition isn't a valid staircase:
        > "Every staircase consists of at least two steps"
'''
def calc_num_staircases_memoised(n): # type: (int) -> int
    cache = [[-1 for j in range(n + 2)] for i in range(n + 2)]

    def calc_num_staircases(height, remaining): # type: (int, int) -> int
        if cache[height][remaining] != -1:
            return cache[height][remaining]

        if remaining == 0:
            return 1
        if remaining < height:
            return 0

        '''
            Call graph for n = 3

                      (1, 3): 2
                    /            \
                  /                \
                /                    \
            (2, 2): 1             (2, 3): 1
            /        \           /         \
        (3, 0): 1  (3, 2): 0  (3, 1): 0  (3, 3): 1
                                         /       \
                                        /         \
                                    (4, 0): 1  (4, 3): 0
        '''
        num_staircases = calc_num_staircases(height + 1, remaining - height) + calc_num_staircases(height + 1, remaining)
        cache[height][remaining] = num_staircases

        return num_staircases

    return calc_num_staircases(1, n) - 1

# def calc_num_staircases(n, max_height=0):
#     # type: (int, int) -> int
#     print "n:", n, "max_height:", max_height
#     if n in [1, 2]:
#         if n < max_height:
#             print " return 1"
#         return 1 if n < max_height else 0

#     count = 0

#     left = n
#     right = 0
#     while right < n:
#         left -= 1
#         right += 1

#         if left < max_height:
#             count += calc_num_staircases(right, left)
#             print " count: ", count

#     print " return count: ", count
#     return count

def solution(n): # type: (int) -> int
    return calc_num_staircases_memoised(n)


# ============================ Official test-cases ============================
assert solution(3) == 1, 'solution(3) failed!'
assert solution(200) == 487067745, 'solution(200) failed!'

# =========== My own, unofficial test cases to help debug behaviour ===========
assert solution(3) == 1, 'solution(3) failed!'
assert solution(4) == 1, 'solution(4) failed!'
assert solution(5) == 2, 'solution(5) failed!'
assert solution(6) == 3, 'solution(6) failed!'
assert solution(7) == 4, 'solution(7) failed!'
assert solution(8) == 5, 'solution(8) failed!'
assert solution(9) == 7, 'solution(9) failed!'
