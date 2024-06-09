def p01():
    _ = input()
    l = list(map(int, input().split()))
    for i in reversed(l):
        print(i, end=" ")
    print()

p01()