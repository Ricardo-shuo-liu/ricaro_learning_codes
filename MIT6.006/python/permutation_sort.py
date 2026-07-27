def permutation_sort(A):
    for B in permutations(A):
        if is_sorted(B):
            return B
