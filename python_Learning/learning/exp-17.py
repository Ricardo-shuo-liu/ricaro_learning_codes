import threading
import time

obj = threading.local()

def worker(name):
    # 给【本线程专属】的obj.x赋值
    obj.x = name
    print(f"[{name}] 设置 obj.x = {obj.x}")

    # 强制sleep，两个线程同时处于存活状态，都保留自己的x
    time.sleep(2)

    # sleep完再次读取，还是自己的值，没有被另外一个线程覆盖
    print(f"[{name}] sleep结束，obj.x = {obj.x}")


t1 = threading.Thread(target=worker, args=("线程1",))
t2 = threading.Thread(target=worker, args=("线程2",))

t1.start()
t2.start()

t1.join()
t2.join()
