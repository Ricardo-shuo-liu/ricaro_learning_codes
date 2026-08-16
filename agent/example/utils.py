"""通用工具函数模块。"""

from collections.abc import Iterable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")


def clamp(value: float, low: float, high: float) -> float:
    """把 value 限制在 [low, high] 区间内。"""
    if low > high:
        low, high = high, low
    return max(low, min(high, value))


def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """把可迭代对象按指定大小切分成若干块。"""
    if size <= 0:
        raise ValueError("size 必须为正整数")
    bucket: list[T] = []
    for item in iterable:
        bucket.append(item)
        if len(bucket) == size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket


def is_palindrome(text: str) -> bool:
    """判断字符串是否为回文（忽略大小写与非字母数字字符）。"""
    cleaned = "".join(ch for ch in text.lower() if ch.isalnum())
    return cleaned == cleaned[::-1]
