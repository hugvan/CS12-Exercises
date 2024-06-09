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

p09()


