#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# UTF-8 for the mathematical symbols in comments
from math import factorial
from fractions import gcd
from typing import Iterator

'''
    Brute-force search = O(s^(w * h))
    So it's not really feasible...
    There has to be a trick to this...

    * a lot of Googling later *

    This problem is Burnside's lemma, a special case of the Pólya enumeration
    theorem.

    There is a LOT of group theory background required to solve it, so there
    will be many group theory terms referenced in the description and code.

    Easier to understand description of Burnside's lemma on Stack Overflow
        https://stackoverflow.com/a/42661013

    Burnside's lemma equates the number of orbits of the symmetry group
        G = Sw × Sh
    acting on the set of configurations
        X = ([w] × [h] → [s])
    to the sum
        1/|G| ∑_[g ∈ G] |Xg|,
    where
        Xg = {x | g.x = x} is the set of elements fixed by g

    The Burnside's lemma formula by itself is not really sufficient to solve
    the problem though, nor is it efficient for large sets (X) or groups (G).

    Example problem:
    The sides of a square are to be colored by either red or blue. How many
    different arrangements are there if a coloring that can be obtained from
    another by rotation is considered identical?
    https://brilliant.org/wiki/burnsides-lemma

    Another Example problem:
    The number of rotationally distinct colourings of the faces of a cube using
    three colours
    https://en.wikipedia.org/wiki/Burnside%27s_lemma#Example_application
    https://en.wikipedia.org/wiki/Cycle_index#The_cycle_index_of_the_face_permutations_of_a_cube

    The conjugacy classes give how many different rotations are possible for a
    given *type* of rotation. See the example problems above for visual
    examples of rotations.

    In plain(er) English, we need to sum over the conjugacy classes,
    multiplying each term (i.e. conjugacy class) by the number of group
    elements that remain fixed/unaffected by the conjugacy class/rotations.

    This article by Brilliant gives a *brilliant* explanation of conjugacy
    classes, and it should be obvious why it's used in our calculation:
    https://brilliant.org/wiki/conjugacy-classes

    Conjugacy class size formula in symmetric group:
    https://groupprops.subwiki.org/wiki/Conjugacy_class_size_formula_in_symmetric_group

    We need a way to programmatically ascertain the number of elements fixed by
    G for each conjugacy class in our Disorderly Escape problem specifically.

    Chris Locke gives a formula:
        https://project-eutopia.github.io/Google_foobar_challenge
    using a visual proof.

    For a general m × n box, the number of elements fixed is
        s ^ GCD(m, n)

    This was the only part I could not derive myself :( thank you Chris! :D
'''


# From David Eppstein
def partitions(n): # type: (int) -> Iterator[list[int]]
	# base case of recursion: zero is the sum of the empty list
	if n == 0:
		yield []
		return

	# modify partitions of n - 1 to form partitions of n
	for p in partitions(n - 1):
		yield [1] + p
		if p and (len(p) < 2 or p[1] > p[0]):
			yield [p[0] + 1] + p[1:]

# Calculate conjugacy class size for symmetric group, formula from:
# https://groupprops.subwiki.org/wiki/Conjugacy_class_size_formula_in_symmetric_group
# > To compute the size of the class, you'll divide n! by the product of the
# > partition terms (because circular permutations of the cycles are equivalent)
# > and also by the product of the number of symmetries between cycles of the
# > same size (product of the factorials of the multiplicities).
# https://stackoverflow.com/a/42661013
def conjugacy_class_size(partition): # type: (list[int]) -> int
    n = sum(partition)

    # integer -> number of times integer appears in partition
    freqs = {}

    for p in partition:
        if p in freqs:
            freqs[p] = freqs[p] + 1
        else:
            freqs[p] = 1

    denominator = 1

    for num, f in freqs.items():
        denominator *= (num ** f) * factorial(f)

    # Answer will always be an int
    return int(factorial(n) / denominator)


def solution(w, h, s): # type: (int, int, int) -> str
    # number of permutations of rows × the number of permutations of columns
    size_group = factorial(w) * factorial(h)

    partitions_w = list(partitions(w))
    partitions_h = list(partitions(h))

    total = 0

    for col_partition in partitions_h:
        for row_partition in partitions_w:
            n_fixed_points_exponent = 0

            for m in col_partition:
                for n in row_partition:
                    n_fixed_points_exponent += gcd(m, n)

            total += (conjugacy_class_size(col_partition)
                      * conjugacy_class_size(row_partition)
                      * (s ** n_fixed_points_exponent))

    return str(total / size_group)


# ============================ Official test-cases ============================
assert solution(2, 3, 4) == '430'
assert solution(2, 2, 2) == '7'
