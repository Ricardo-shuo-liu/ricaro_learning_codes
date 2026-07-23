def list_partitions(n,m):
    if n <0 or m==0:
        return []
    else:
        exact_match = []
        if n==m:
            exact_match = [[m]]
        with_m = [ p + [m] for p in list_partitions(n-m,m)]
        without_m = list_partitions(n,m-1)
        return exact_match + with_m + without_m

