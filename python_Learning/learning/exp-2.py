import functools
import argparse

if __name__ == "__main__":
    f = functools.partial(int,base=2)
    r = f('1000000')
    print(r)