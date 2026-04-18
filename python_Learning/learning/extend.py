import inspect

def my_print(*args):
    # 我被谁调用了？
    caller = inspect.stack()[1]
    print(f"[{caller.filename}:{caller.lineno}] {args}")
