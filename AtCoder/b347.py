def a():
    _, k = map(int, input().split())
    nums = list(map(int, input().split()))

    for n in nums:
        if n % k == 0:
            print(n // k, end=" ")
    print()

def b():
    string = input()
    
    substrings: set[str] = set()

    for left in range(len(string)):
        for right in range(left, len(string)):
            substrings.add(string[left:right+1])
    
    print(len(substrings))

def c():
    _, a, b = map(int, input().split())
    plan_days = list(map(int, input().split()))
    
    print([d % (a+b) for d in plan_days])

c()