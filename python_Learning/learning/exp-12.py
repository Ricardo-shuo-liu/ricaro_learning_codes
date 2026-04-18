import inspect

def my_func(name: str, age=18, *args, **kwargs):
    pass

# 偷看函数长啥样
sig = inspect.signature(my_func)
print(sig)  # (name: str, age=18, *args, **kwargs)


import inspect

def hello():
    print("我是秘密代码")

# 偷看源码
print(inspect.getsource(hello))


import inspect

def func(): pass
class A: pass

print(inspect.isfunction(func))   # True
print(inspect.isclass(A))         # True


import inspect

def f(a, b=2, *args, c=10, **kwargs):
    pass

spec = inspect.getfullargspec(f)
print(spec)


import inspect

s = "hello"
# 把字符串所有成员都列出来
members = inspect.getmembers(s)
for name, val in members:
    print(name)


