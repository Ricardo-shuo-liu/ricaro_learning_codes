def large(s,n):
    if s == []:
        return []
    elif s[0] > n:
        return large(s[1:],n)
    else:
        first = s[0]
        with_f = [first] + large(s[1:],n-first)
        without_f = large(s[1:],n)

        if sum(with_f) > sum(without_f):
            return with_f
        else:
            return without_f
