from functools import lru_cache
import time
@lru_cache
def say_hi(name: str, salutation: str = "Ms."):

    return f"Hello {salutation} {name}"
a = time.time()
say_hi("wang")
b = time.time()
print(b-a)
a = time.time()
say_hi("wang")
b = time.time()
print(b-a)