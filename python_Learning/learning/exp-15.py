import inspect
def inspect_():
    frame = inspect.currentframe()
    frame = frame.f_back
    print(frame.f_lineno)
    print(frame.f_code.co_name)
    module = inspect.getmodule(frame)
    if module is None:
        return None
    source = inspect.getsource(module)
    print(source)
inspect_()