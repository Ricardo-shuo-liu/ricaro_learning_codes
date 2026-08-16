"""命令行入口：python -m example ..."""

from __future__ import annotations

import argparse
import sys

from .core import Calculator, greet
from .utils import chunked, clamp, is_palindrome


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="example",
        description="example 包的命令行演示工具",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_greet = sub.add_parser("greet", help="输出问候语")
    p_greet.add_argument("name", nargs="?", default="World", help="要问候的名字")

    p_calc = sub.add_parser("calc", help="四则运算: a op b")
    p_calc.add_argument("a", type=float)
    p_calc.add_argument("op", choices=["+", "-", "*", "/"])
    p_calc.add_argument("b", type=float)

    p_pal = sub.add_parser("palindrome", help="判断是否为回文")
    p_pal.add_argument("text", help="要检查的文本")

    p_chunk = sub.add_parser("chunk", help="把字符串按长度分块")
    p_chunk.add_argument("text")
    p_chunk.add_argument("size", type=int)

    p_clamp = sub.add_parser("clamp", help="把数值限制到区间")
    p_clamp.add_argument("value", type=float)
    p_clamp.add_argument("low", type=float)
    p_clamp.add_argument("high", type=float)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "greet":
        print(greet(args.name))
    elif args.command == "calc":
        calc = Calculator()
        result = {
            "+": calc.add,
            "-": calc.subtract,
            "*": calc.multiply,
            "/": calc.divide,
        }[args.op](args.a, args.b)
        print(f"{args.a:g} {args.op} {args.b:g} = {result:g}")
    elif args.command == "palindrome":
        print("是回文" if is_palindrome(args.text) else "不是回文")
    elif args.command == "chunk":
        for i, part in enumerate(chunked(args.text, args.size)):
            print(f"[{i}] {''.join(part)}")
    elif args.command == "clamp":
        print(clamp(args.value, args.low, args.high))
    return 0


if __name__ == "__main__":
    sys.exit(main())
