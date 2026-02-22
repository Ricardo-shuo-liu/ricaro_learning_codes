import functools

def longfast(x:int):
    return x**2
def add(x:int,y:int):

    return x + y

def is_True(x):
    return x=="A"

if __name__ == "__main__":
    list_result = map(longfast,[1,2,3,4])
    print(list(list_result))
    result = functools.reduce(add,[1,2,3,4])
    print(result)

    print(list(filter(is_True,["A",'B'])))