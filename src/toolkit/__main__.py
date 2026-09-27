import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def main() -> None:
    """
    Точка входа CLI.

    Разбирает аргументы командной строки и вызывает соответствующую
    функцию ядра: calculate для подкоманды calc, convert для convert.
    Пользовательские ошибки выводятся в stderr, код возврата — 2.
    """
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Набор консольных утилит: калькулятор и конвертер",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Подкоманда calc
    calc_parser = subparsers.add_parser(
        "calc", help="Вычислить арифметическое выражение"
    )
    calc_parser.add_argument(
        "expression", help="Выражение, например: 2+3*4"
    )

    # Подкоманда convert
    convert_parser = subparsers.add_parser(
        "convert", help="Конвертировать величину"
    )
    convert_parser.add_argument(
        "value", type=float, help="Числовое значение"
    )
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, help="Исходная единица"
    )
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, help="Целевая единица"
    )

    args = parser.parse_args()

    try:
        if args.command == "calc":
            result = calculate(args.expression)
            print(result)
        elif args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
            print(result)
    except ToolkitError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    except ZeroDivisionError as e:
        print(e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()