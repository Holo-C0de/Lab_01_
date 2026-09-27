from .errors import CalculationError
from .parser_rpn import evaluate, to_rpn
from .tokenizer import tokenize


def calculate(expression: str) -> float:
    """
    Вычисляет арифметическое выражение и возвращает результат.

    Args:
        expression: Строка с арифметическим выражением. Может содержать
            числа, операторы ``+ - * / // %``, скобки, пробелы и унарные
            знаки ``+`` и ``-``.

    Returns:
        Результат вычисления выражения в виде числа.

    Raises:
        CalculationError: Если выражение пустое или содержит синтаксическую
            ошибку (неизвестный символ, лишние скобки, два оператора
            подряд, недостаток операндов).
        ZeroDivisionError: Если в выражении встречается деление на ноль.

    Алгоритм:
        1. Проверка входного выражения на пустоту.
        2. Токенизация — сохранение токенов в ``tokens``.
        3. Перевод токенов в обратную польскую нотацию (RPN).
        4. Вычисление RPN через стек.
    """
    if len(expression.strip()) == 0: #Блок 1
        raise CalculationError("Пустое выражение")
    
    tokens = tokenize(expression) #Блок 2
    
    rpn = to_rpn(tokens) #Блок 3

    result = evaluate(rpn) #Блок 4

    return result 
    