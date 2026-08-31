import sys
import select

readable, _, _ = select.select([sys.stdin], [], [], 2.5)
if readable:
    # 有输入，读取stdin
    # line = sys.stdin.readline()
    line = readable[0].readline()
    print("收到输入：", line.strip())
else:
    # 0.25秒没有输入，程序继续往下跑，不会阻塞等待
    print("超时，无输入")