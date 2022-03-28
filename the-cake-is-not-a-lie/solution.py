#!/usr/bin/env python2.7

def solution(s): # type: (str) -> int
    for i in xrange(1, len(s)):
        substring = s[:i]
        n_occurrences = s.count(substring)
        # Cast to float to prevent implicit integer division in Python 2
        num_divisions = float(len(s)) / float(i)

        # Further iteration will only decrease the number of possible divisions
        if float(n_occurrences) == num_divisions:
            return int(num_divisions)

    # In case it's not possible to divide the string at all
    return 1


# ============================ Official test-cases ============================
assert solution('abcabcabcabc') == 4, "solution('abcabcabcabc') failed!"
assert solution('abccbaabccba') == 2, "solution('abccbaabccba') failed!"

# =========== My own, unofficial test cases to help debug behaviour ===========
assert solution('a') == 1, "solution('a') failed!"
assert solution('aaa') == 3, "solution('aaa') failed!"
assert solution('abab') == 2, "solution('abab') failed!"
assert solution('aba') == 1, "solution('aba') failed!"
assert solution('aab') == 1, "solution('aab') failed!"
assert solution('ababc') == 1, "solution('ababc') failed!"
