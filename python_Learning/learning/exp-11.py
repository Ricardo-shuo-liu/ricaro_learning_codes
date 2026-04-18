import inspect

def my_print():
    stack = inspect.stack()

    print("==== stack 全部内容 ====")
    for i, frame in enumerate(stack):
        print(f"stack[{i}] → 函数名：{frame.function}，行号：{frame.lineno}")

    print("\n我们真正需要的是：调用者的位置 → stack[1]")
    caller = stack[1]
    print(f"调用来自：第 {caller.lineno} 行")

# ----------------------

def test1():
    my_print()  # 第 18 行

def test2():
    my_print()  # 第 21 行

test1()
print("-" * 30)
test2()
