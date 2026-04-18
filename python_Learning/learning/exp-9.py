import inspect

def test():
    # 这行代码想知道：我现在在第几行？
    frame = inspect.currentframe()
    print("我现在在第", frame.f_lineno, "行")

test()


def my_print():
    # 我想知道：是谁在哪一行调用了我？
    caller_frame = inspect.stack()[1]
    print(f"被调用自：第 {caller_frame.lineno} 行")

# 第 9 行调用
my_print()

# 第 11 行调用
my_print()
