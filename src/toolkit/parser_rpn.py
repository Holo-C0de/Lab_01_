from .errors import CalculationError

#Приоритеты операций
PRIORITIES = {
        "+":1,
        "-":1,
        "*":2,
        "/":2,
        "//":2,
        "%":2,
        "u-":3,
        "u+":3
    } 

def to_rpn(tokens: list[tuple[str, str]]) -> list[str]:
    """
    Переводит токены в обратную польскую нотацию (RPN).

    Идёт по токенам и расставляет их в такой порядок, чтобы потом
    можно было вычислить выражение слева направо без скобок и без
    учёта приоритетов. Операторы временно хранятся в стеке, а в
    результат попадают, когда их приоритет позволяет выполнить их
    раньше следующих. Скобки задают границы: внутри них порядок
    восстанавливается отдельно. Унарные плюс и минус превращаются
    в ``u+`` и ``u-``, чтобы на вычислении их не путать с обычными.

    Args:
        tokens: Список токенов, полученный из ``tokenize``.

    Returns:
        Список строк в RPN — числа и операторы в порядке вычисления.

    Raises:
        CalculationError: Если скобки не сходятся: есть лишняя ``)``
            или лишняя ``(``.
    """
    
    output = [] #выходной список
    op_stack = [] #стопка операторов

    for type_t, value in tokens: #type_t - ("NUMBER", "OPERATOR", "UNARY", "LPAREN", "RPAREN"), value - ('2', '+', '(' и др)
        if type_t == "NUMBER":
            output.append(value)
            continue

        if type_t == "OPERATOR" and value in PRIORITIES:
            while len(op_stack) != 0 and op_stack[-1] != "(" and PRIORITIES[op_stack[-1]] >= PRIORITIES[value]:
                output.append(op_stack.pop())
            op_stack.append(value) #кладём текущий оператор в стопку, чтобы он там подождал следующий токен
            continue

        if type_t == "LPAREN" and value == "(":
            op_stack.append(value)
            continue
    
        if type_t == "RPAREN" and value == ")":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            if len(op_stack) == 0 or op_stack[-1] != "(":
                raise CalculationError("Несбалансированные скобки: лишняя )")
            op_stack.pop()
            continue

        if type_t == "UNARY":
            if value == "+":
                oper = "u+"
            else:
                oper = "u-"
            while len(op_stack) != 0 and op_stack[-1] != "(" and PRIORITIES[op_stack[-1]] > PRIORITIES[oper]:
                output.append(op_stack.pop())
            op_stack.append(oper)
            continue

    while op_stack:
        el = op_stack.pop()
        if el == "(":
            raise CalculationError("Несбалансированные скобки: лишняя (")
        output.append(el)
    return output


def evaluate(tokens: list[str]) -> float:
    """
    Вычисляет выражение, записанное в обратной польской нотации.

    Идёт по токенам слева направо. Числа отправляет в стек. На
    операторе снимает из стека нужное число операндов — один для
    ``u+`` и ``u-``, два для ``+ - * / // %`` — и возвращает
    результат обратно в стек. К концу в стеке должно остаться
    ровно одно число: это и является ответом.

    Args:
        tokens: Список строк в RPN, полученный из ``to_rpn``.

    Returns:
        Результат вычисления в виде числа.

    Raises:
        ZeroDivisionError: При делении на ноль.
        CalculationError: Если после вычисления в стеке не ровно одно
            число — выражение было некорректным.
    """
    stack = []
    for value in tokens: #Идём по токенам
        if value in ("u+", "u-"): #Блок для унарных операндов
            if len(stack) < 1:
                raise CalculationError("Некорректное выражение: недостаточно операндов")

            a = stack.pop()
            
            if value == "u+":
                result = a

            elif value == "u-":
                result = -a

            stack.append(result)

        elif value in ("+", "-", "*", "/", "//", "%"):
            if len(stack) < 2:
                raise CalculationError("Некорректное выражение: недостаточно операндов")
           
            #По правилу ОПН нужно взять два числа(правое число и левое число)
            b = stack.pop() #правое число(операнд)
            a = stack.pop() #левое число(операнд)

            #Блок для использования операторов
            if value == "+":
                result = a + b

            elif value == "-":
                result = a - b

            elif value == "*":
                result = a * b

            elif value == "/":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a / b

            elif value == "//":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a // b

            elif value == "%":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a % b
    
            stack.append(result)
        else: #токен оказался числом
            if "." in value: #В числе есть плавающая точка
                stack.append(float(value))
            else:
                stack.append(int(value))
    if len(stack) != 1: #Обработка ошибки в стеке больше чем один элемент
        raise CalculationError("Некорректное выражение: в стеке должно остаться ровно одно значение")
    
    return stack.pop()
