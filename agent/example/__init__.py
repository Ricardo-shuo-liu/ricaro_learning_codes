"""example — 一个用于演示 Python 包结构的示例包。

用法示例::

    import example
    print(example.greet("World"))
    print(example.Calculator().add(1, 2))
"""

from .core import Calculator, greet
from .utils import clamp, chunked, is_palindrome

__version__ = "0.1.0"

__all__ = [
    "Calculator",
    "greet",
    "clamp",
    "chunked",
    "is_palindrome",
    "__version__",
]
