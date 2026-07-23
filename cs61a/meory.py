def meo(fn):
    cache = {}
    def memoized(n):
        if n not in cache:
            cache[n] = fn(n)
            return cache[n]
        return cache[n]
    return memoized

@meo
def fib(n):
    if n == 0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

