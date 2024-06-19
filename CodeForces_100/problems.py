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

def p26():
    ... #selection sort

def p37():
    input()
    seq = list(map(int, input().split())) 
    coins, zeroes, neg_ones= 0, 0, 0
    
    for s in seq:
        if s != 0: 
            coins += abs(s) - 1
            if s < 0: neg_ones += 1 
        else:
            coins += 1
            zeroes += 1
    
    if neg_ones % 2 != 0 and zeroes == 0:
        coins += 2
    
    print(coins)

def p38():
    def helper(state: str, sum_before: int|None) -> bool:        
        current_sum = 0
        for idx, s in enumerate(state):
            digit = int(s)
            current_sum += digit

            if current_sum == sum_before and idx + 1 == len(state):
                return True

            if sum_before is not None and current_sum > sum_before:
                return False

            elif (sum_before is None or current_sum == sum_before) and helper(state[idx+1:], current_sum):
                return True
        
        return False
    
    input()
    print("YES" if helper(input(), None) else "NO")

def p39():
    MAX = 10**6
    minimum_costs: dict[str, int] = {"A": MAX,  "B": MAX,  "C": MAX,
                                     "AB": MAX, "BC": MAX, "AC": MAX,
                                     "ABC": MAX }
    
    for _ in range(int(input())):
        cost, vitamins = input().split()
        cost = int(cost)
        vitamins = ''.join(sorted(vitamins))
        minimum_costs[vitamins] = min(cost, minimum_costs[vitamins])
    
    
    def helper(tally_cost: int, vitamins: str) -> int:
        if set(vitamins) == {"A", "B", "C"}:
            return tally_cost

        ret: list[int] = []
        for vit_key, cost in minimum_costs.items():
            if cost == MAX or not(set(vit_key) - set(vitamins)):
                continue


            helper_ret = helper(tally_cost + cost, "".join(set(vit_key + vitamins)) )
            if helper_ret != -1:
                ret.append(helper_ret)

        return min(ret) if ret else -1

    
    print(helper(0, ""))

def p40():
    # TLE, try prefix sum instead
    _, queries = map(int, input().split())
    candies = list(map(int, input().split()))
    for _ in range(queries):
        l, r = map(int, input().split())
        print(sum(candies[l:r+1]))

def p42():
    from math import ceil
    bench_num = int(input())
    standers = int(input())
    benches: list[int] = []

    max_sitters = 0
    for i in range(bench_num):
        sitters = int(input())
        benches.append(sitters)
        max_sitters = max(max_sitters, sitters)
    
    hidable = 0
    for sitters in benches:
        hidable += max_sitters - sitters
    
    print(max_sitters + ceil(max(0, standers - hidable) / bench_num), max_sitters + standers)

def p44():
    from functools import cache

    @cache
    def helper(len_left: int) -> int:
        if len_left <= 0:
            return 0
        
        if len_left == 1 or len_left == 2:
            return len_left
        
        count = 0
        for x in (1, 2):
            count += helper(len_left - x)
        return count
    
    print(helper(int(input())))

def p47():
    
    num = int(input())
    if num == 0: 
        print("0 0 0")
        return
    
    if num == 1:
        print("1 0 0")
        return
    
    last_nums = [1, 0, 0, 0]
    while last_nums[0] < num:
        f = last_nums[0] + last_nums[1]
        last_nums = [f] + last_nums[:-1]
    
    print(last_nums[2], last_nums[2], last_nums[3])

def p48():
    from functools import cache

    num, mod = map(int, input().split())

    if num == 1:
        print(1)
        return

    l1, l2 = 1, 2
    for _ in range(num -2):
        l1, l2 = l2, (l1 % mod + l2 % mod) % mod    
    
    print(l2)

p48()