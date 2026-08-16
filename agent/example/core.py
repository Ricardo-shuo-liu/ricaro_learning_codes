"""核心业务逻辑模块。"""


def greet(name: str = "World") -> str:
    """返回一条友好的问候语。"""
    name = name.strip() or "World"
    return f"Hello, {name}!"


class Calculator:
    """一个简单的四则运算计算器示例类。"""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("除数不能为 0")
        return a / b
