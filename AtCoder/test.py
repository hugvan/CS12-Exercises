from functools import cache

def repdigits_at_most(n: int) -> list[int]:

    repdigits: list[int] = []
    stringified = str(n)
    digits = len(stringified)
    leading_digit = int(stringified[0])

    for digit in range(1, digits):
        repdigits.extend([int(str(x) * digit) for x in range(1, 10)])
    
    for leading in range(1, leading_digit):
        repdigits.append(int(str(leading) * digits))
    
    if n >= int(str(leading_digit) * digits):
        repdigits.append(int(str(leading_digit) * digits))
    
    return repdigits

@cache
def repdigit_decompose(n: int, depth: int = 0) -> list[int]:
    if n <= 0 or depth > 10:
        return []


    stringified = str(n)
    digits = len(stringified)

    biggest = repdigits_at_most(n)[-1]
    
    candidates: list[list[int]] = []
    candidates.append([biggest, *repdigit_decompose(n- biggest, depth + 1)])
    
    for digit in range(1, digits):
        fixer = int("9" * digit)
        candidates.append([fixer, *repdigit_decompose(n- fixer, depth + 1)])
    
    return min(candidates, key=len)

from random import randint

print(x := randint(100000,1000000) ,repdigit_decompose(x))