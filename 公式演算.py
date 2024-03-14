import math


# 3U 正弦滑变PRI NUM
# pw = (math.sin((i - 1) / (num - 1) * 2 * math.pi) *  100 * pri_range / 2 + pri) * 0.9
print(math.pi)

def cal_pw_and_pri(no: int, pw: int = 90000, num: int = 3, pri: int = 100000, pri_range: int = 50):
    result = 1e12
    copy_num = 0
    copy_sin = 0
    for i in range(1, num + 1):
        _sin = math.sin((i - 1) / (num - 1) * 2 * math.pi)
        compare_data = (_sin * 100 * pri_range / 200 + pri) * 0.9
        print(_sin, result)
        if result > compare_data:
            result = compare_data
            copy_num = i
            copy_sin = _sin
    # PW
    if no == 0:
        if pw > result:
            pw = result
            print(f"PW超出最小值，实际PW={pw}")
        else:
            print(f"PW值未超出最小值，PW={pw}")
    # NUM
    elif no == 1:
        if pw > result:
            num = copy_num
            print(f"实际NUM={num}, result={result}")
    # RANGE
    elif no == 2:
        if pw > result:
            _range = (pw / 0.9 - pri) * 200 / 100 / copy_sin
            print(f"实际RANGE={_range}")
    # PRI
    elif no == 3:
        if pw > result:
            pri = pw / 0.9 - copy_sin * 100 * pri_range / 200
            print(f"实际PRI={pri}", copy_sin, pw, result, pri_range)


if __name__ == '__main__':
    cal_pw_and_pri(no=0)
