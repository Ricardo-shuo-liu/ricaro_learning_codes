"""The ucb module contains functions specific to 61A projects at UC Berkeley."""

from __future__ import print_function

import code
import functools
import inspect
import re
import signal
import sys

def main(fn):
    """Call fn with command line arguments. Used as a decorator."""
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:]
        fn(*args)
    return fn

_PREFIX = ''
def trace(fn):
    """A decorator that prints a function's name, args, and return values."""
    @functools.wraps(fn)
    def wrapped(*args, **kwds):
        global _PREFIX
        reprs = [repr(e) for e in args]
        reprs += [f"{k}={repr(v)}" for k, v in kwds.items()]
        print(f"{_PREFIX}-> {fn.__name__}({', '.join(reprs)})")
        _PREFIX += '|  '
        result = fn(*args, **kwds)
        _PREFIX = _PREFIX[:-3]
        print(f"{_PREFIX}<- {fn.__name__} returned {repr(result)}")
        return result
    return wrapped

def interact():
    """Start an interactive interpreter session in the current environment."""
    code.interact(local=dict(globals(), **locals()))