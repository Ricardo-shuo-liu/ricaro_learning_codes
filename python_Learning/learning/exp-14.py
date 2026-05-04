import warnings

# 基础用法
warnings.warn("这是一条警告信息")

# 带变量的警告（你代码里的用法）
action = "move"
warnings.warn(f"重复覆盖动作：{action}")
