#!/usr/bin/env python2.7

'''
    Rephrasing the question because it was hard to understand from the
    description in readme.txt:
    We want to know how long (and if it's possible?) to reach the state of
        num(Mach bombs) = x, num(Facula bombs) = y
    From the initial state of
        num(Mach bombs) = 1, num(Facula bombs) = 1

    For each iteration we make the choice of
        new num Mach bombs = old num Mach bombs + old num Facula bombs
    or
        new num Facula bombs = old num Mach bombs + old num Facula bombs

    It's intuitive to see that if we iterate past either x or y, then a
    solution is not possible.

    Exploring the computation tree 4 levels deep:
                                                         (1, 1)
                                              /                          \
                             (1, 2)                                                  (2, 1)
                         /            \                                          /            \
               (1, 3)                      (3, 2)                      (2, 3)                      (3, 1)
              /      \                    /      \                    /      \                    /      \
        (1, 4)        (4, 3)        (3, 5)        (5, 2)        (2, 5)        (5, 3)        (3, 4)        (4, 1)
        /    \        /    \        /    \        /    \        /    \        /    \        /    \        /    \
    (1, 5) (5, 4) (4, 7) (7, 3) (3, 8) (8, 5) (5, 7) (7, 2) (2, 7) (7, 2) (5, 8) (8, 5) (3, 7) (7, 4) (4, 5) (5, 1)

    Notice that the tree is symmetrical, we only have to compute half the nodes
    in the worst case.
    However halving the runtime may not be significant enough...

    Could it be more efficient?

    Observations:
        - We can deduce if x > y, then on the previous iteration,
          x = x + y happened, and the inverse logic is also true.
        - We can see that x != y, except for the base case of x = 1, y = 1

    Perhaps working backwards from the goal state is an easier (and more
    efficient) approach.
    - This worked well but failed test case 3 (hidden). I suspect it is failing
      for exceeding a time limit when testing on large numbers e.g.
      solution('1', '1000000000') shows it is quite slow.
      For solution('1', '1000000000'), you would be iterating a billion times!

    This idea of going back up through the tree still seems on the right track
    though, but can we somehow speed up the iteration process a bit more?
    How can we skip some (hopefully many) iterations?

    The current iteration mechanism is:
        while mach >= 1 and facula >= 1:
            if mach == 1 and facula == 1:
                return str(count)

            if mach == facula:
                return 'impossible'

            if mach > facula:
                mach -= facula
            else:
                facula -= mach

            count += 1

    We iterate by subtracting from either 'mach' or 'facula'...
    ...what if we think of division as a series of subtractions?

    Could the use of division speed up this iteration mechanism?

    After staring at the previously-seen computation tree above for a while I
    noticed that we can skip some nodes if we do:
        if mach > facula:
            count += mach / facula # integer division!
            mach %= facula
        else:
            count += facula / mach # integer division!
            facula %= mach

    This allows us skip successive subtractions to the same bomb-type.
    (successive *subtractions* form the perspective of going back up the
    tree)
    Successive subtractions/additions to the same bomb-type can also be seen in
    the tree I drew as two or more traverses in the same direction.
'''
def solution(x, y): # type: (str, str) -> str
    if x == y:
        return 'impossible'

    '''
        Note: On versions of Python older than 2.4, there is a difference
        between int and long!
        int should be automatically promoted to long as required on
        Python 2.7.13 - the environment listed on constraints.txt.
        See PEP 237 - Unifying Long Integers and Integers
    '''
    mach = int(x)
    facula = int(y)

    count = 0

    while mach >= 1 and facula >= 1:
        # If one of the bomb-types == 1, then it is definitely in the tree and
        # there is only one more computation to do.
        # It's actually the same process as the addition to 'count' below,
        # but here we can simplify it as we know that min(mach, facula) == 1.
        if mach == 1 or facula == 1:
            count += max(mach, facula)
            return str(count - 1)

        # Is there a more elegant way of writing this?
        # Could do
        #     count += max(mach, facula) / min(mach, facula)
        # but the new assignment to mach or facula is not so simple.
        # Perhaps if we did something like always make the smaller element be
        # the first element, but I think it makes the meaning of the code a bit
        # harder to understand.
        if mach > facula:
            count += mach / facula # integer division!
            mach %= facula
        else:
            count += facula / mach # integer division!
            facula %= mach

    return 'impossible'


# ============================ Official test-cases ============================
assert solution('2', '1') == '1', "solution('2', '1') failed!"
assert solution('4', '7') == '4', "solution('4', '7') failed!"

# =========== My own, unofficial test cases to help debug behaviour ===========
# This example is described in readme.txt,
# I guess it's 'official', though not explicitly written as one...
assert solution('2', '4') == 'impossible', "solution('2', '4') failed!"
