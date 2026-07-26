from typing import Tuple
def get_max_length(A:Tuple):
    max = 0
    save_space = 0
    for i in range(len(A)-1):
        if A[i] <= A[i+1]:
             max+=1
        else:
            if max>save_space:
                save_space = max
            max = 0
    return save_space
def count_long_subarray(A:Tuple):
    max_len = get_max_length(A)
    impor = 0
    count = 0
    for i in range(len(A) - 1):
        if A[i] <= A[i+1]:
            impor += 1

            if impor==max_len:
                count+=1
        else:
            impor = 0
    return count
