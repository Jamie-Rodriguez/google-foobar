#!/usr/bin/env python2.7

def solution(s): # type: (str) -> int
    # Can do this problem just by looking at the '>'s and looking rightward for '<' characters
    # Or vice versa
    # Every 'collision' will always count as 2 salutes (1 each)
    num_facing_right = 0 # number of '>' characters
    total_salutes = 0 # number of collisions * 2

    # We can iterate to the right and accumulate the current number of seen '>' characters
    # When we see a '<', we calculate the number of salutes that will be made with the '>'s to the left of it - i.e. the '>' we have already counted!
    #     = number of seen '>'s * 2
    # and add it to the total
    for char in s:
        if char == '-':
            continue
        if char == '>':
            num_facing_right += 1
        if char == '<': # Compute salutes time!
            total_salutes += 2 * num_facing_right

    return total_salutes


# ============================ Official test-cases ============================
assert solution('>----<') == 2, "solution('>----<') failed!"
assert solution('<<>><') == 4, "solution('<<>><') failed!"

# =========== My own, unofficial test cases to help debug behaviour ===========
assert solution('--->-><-><-->-') == 10, "solution('--->-><-><-->-') failed!"
assert solution('>') == 0, "solution('>') failed!"
