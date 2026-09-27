from .errors import CalculationError


def tokenize(expression:str) -> list[tuple[str, str]]:
    """
    Разбивает строку выражения на токены.

    Проходит по строке слева направо и формирует список токенов.
    Каждый токен — это пара ``(тип, значение)``, где тип — один из
    ``NUMBER``, ``OPERATOR``, ``UNARY``, ``LPAREN``, ``RPAREN``.
    Унарность ``+`` и ``-`` определяется по типу предыдущего токена.

    Args:
        expression: Строка с арифметическим выражением.

    Returns:
        Список токенов вида [(тип, значение), ...], где тип и значение — строки.

    Raises:
        CalculationError: Если в строке есть неизвестный символ.
    """
    tokens = []
    i = 0 #позиция курсора в строке(выражении)
    n = len(expression) #Длина строки
    prev_type = None #Записывает тип предыдущего токена(символа)
    while i < n:
        ch_t = expression[i] #текущий символ
        
        if ch_t == " ": #если взяли пробел, пропускаем
            i += 1
            continue

        if ch_t.isdigit():
            num = ch_t
            i+=1
            while i < n and (expression[i].isdigit() or expression[i] == "."):
                num += expression[i]
                i+=1
            tokens.append(("NUMBER", num))
            prev_type = "NUMBER"
            continue

        if ch_t == "/" and  i + 1 < n and expression[i + 1] == "/": # Блок для нахождения //
            """
            ch_t == "/" — текущий символ /
            i + 1 < n — следующий индекс не выходит за пределы строки
            expression[i + 1] == "/" — следующий символ тоже /
            """
            tokens.append(("OPERATOR", "//"))
            prev_type = "OPERATOR" #Запись, что предыдущий символ был оператором
            i += 2 #сдвиг курсора на 2 знака, тк // - это два символа
            continue
        
        if ch_t in "+-*/%()": #проверка на оператор(+-*/%) и определение скобок
            if ch_t == "(":
                tokens.append(("LPAREN", ch_t))
                prev_type = "LPAREN"
                i += 1
                continue
                
            elif ch_t == ")":
                tokens.append(("RPAREN", ch_t))
                prev_type = "RPAREN"
                i += 1
                continue

            else: #ветка для (+ - * / %) и учёт унарности
                if ch_t in "+-" and (prev_type in (None, "OPERATOR", "LPAREN", "UNARY")): #Проверка на унарный знак
                    tokens.append(("UNARY", ch_t))
                    prev_type = "UNARY"

                else:
                    tokens.append(("OPERATOR", ch_t))
                    prev_type = "OPERATOR"
                i += 1
                continue
        

        raise CalculationError(f"Неизвестный символ: {ch_t}")
    return tokens
