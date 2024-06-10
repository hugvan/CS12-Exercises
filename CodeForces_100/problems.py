def p01():
    _ = input()
    l = list(map(int, input().split()))
    for i in reversed(l):
        print(i, end=" ")
    print()

def p02():
    _ = input()
    candies = list(map(int, input().split()))
    left, right = map(int, input().split())
    print(sum(candies[left:right+1]))

def p03():
    for _ in range(int(input())):
        word = input()
        print(word if len(word) <= 10 else f"{word[0]}{len(word) - 2}{word[-1]}")

def p04():
    first = input().lower()
    second = input().lower()

    if first < second: print("-1")
    elif first == second: print("0")
    elif first > second: print("1")

def p05():
    seq = input()
    count = 0
    team: str|None = None
    for i in seq:
        count = 1 if team is None or team != i else count+1
        team = i
        if count >= 7:
            print("YES")
            return
    print("NO")

def p08():
    customers, timespan, b_time = map(int, input().split())
    prev_end = 0
    b_count = 0
    for idx in range(customers + 1):
        if idx == customers: #after last customer
            new_start, length = timespan, 0
        else:
            new_start, length = map(int, input().split())
        b_count += (new_start - prev_end)// b_time
        prev_end = new_start + length
    print(b_count)

def p09():
    length = int(input())
    cards = input()
    eights = cards.count("8")
    print(min(eights, length // 11))


# p10 - p12  do not exist?

def p13():
    from math import ceil

    area = int(input())
    for num in reversed(range(1, ceil(area ** 0.5) + 1)):
        if area % num == 0:
            print(2 * (num + area // num))
            break

def p14():
    num = input()
    count = len([n for n in num if n == "4" or n == "7"])
    print("YES" if count == 4 or count == 7 else "NO")

def p15():
    num = int(input())
    divisors = [4, 7, 47, 74, 447, 474, 477, 747, 774] #44, 77, 444, 777, 744

    for lucky in divisors:
        if num % lucky == 0:
            print("YES")
            return
    print("NO")

def p16(): # too easy, semiprimes
    ...

def p17():
    from math import gcd
    max_w, max_h, x, y = map(int, input().split())
    c = gcd(x, y)
    low_x, low_y = x // c, y // c
    print(min(max_w // low_x, max_h // low_y))

def p19():
    length = int(input())
    peaks = list(map(int, input().split()))
    c_indexes: list[int] = []
    for idx, peak in enumerate(peaks):
        if idx == 0 or idx == length - 1:
            continue
        if peaks[idx - 1] < peak and peaks[idx + 1] < peak:
            c_indexes.append(idx)
    
    if not c_indexes:
        print("0")
        return

    for num in reversed(range(2, len(c_indexes))):
        if length % num != 0:
            #not divisible
            continue
        
        day_length = length // num
        last_box = 0
        for c_idx in c_indexes:
            box = c_idx // day_length
            if box - last_box > 1:
                #skipped a box
                break
            last_box = box
        else:
            print(num)
            break
    else:
        print(1)

def p24():
    ... #bubble sort

def p25():
    input()
    seq = list(map(int, input().split()))
    print(sorted(enumerate(seq), key=lambda tup: tup[1])[0][0])

p25()

def p26():
    ... #selection sort