import inspect

def main():
    frame = inspect.currentframe()
    return frame

frame = main()

print("-----",frame.f_code.co_name,frame.f_code.co_filename,frame.f_lineno)
