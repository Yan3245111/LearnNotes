# 一共32位

a = 1
print(bin(a))

b = a << 1
print(bin(b))
c = a >> 1
print(bin(c))

print(b >> (2 - 1) & 1)
# 注释：bit是按照从后往前数的， 第1位是最后一次
# 0b 0000 00001  :1 是第一位，0是第二位这样数的

a = 7   # 3bit   衰减2   （32 - 3）
b = 7   # 6bit   衰减1   （32 - 3 - 6）
c = 1   # 1bit   衰减3   （32 - 3 - 6 - 1）
d = 1   # 6bit   衰减4   （32 - 3 - 6 - 1 - 6）
f = 1   # 6bit  360 = 0  移相1  （32 - 3 - 6 - 1 - 6 - 6）
g = 1   # 8bit           移相2   (32 - 3 - 6 - 1 - 6 - 8 - 6)


def reverse_bit(data: int, length: int) -> int:
    j = 0
    for i in range(length):
        j = j << 1
        j = j | (data & 1)
        data = data >> 1
    return j


res = 0b11100001010000010000010000000010

# res2 = 0b 100 1010000 1 000001 00000 00 100000 00
res2 = 0b11101000001000001000000010000000


def joint1():
    res1 = (a << (32 - 3))
    res1 += (b << (32 - 3 - 6))
    res1 += (c << (32 - 3 - 6 - 1))
    res1 += (d << (32 - 3 - 6 - 1 - 6))
    res1 += (f << (32 - 3 - 6 - 1 - 6 - 6))
    res1 += (g << (32 - 3 - 6 - 1 - 6 - 8 - 7))

    print(bin(res))
    print(bin(res1))


a = 1   # 3bit   衰减2   （32 - len(a)）            100
b = 0   # 6bit   衰减1   （32 - 3 - len(a)）        100 000100
c = 1   # 1bit   衰减3   （32 - 3 - 6 - len(a)）    100 000100 1
d = 0   # 6bit   衰减4   （32 - 3 - 6 - 1 - len(a)）100 000100
f = 0   # 6bit  360 = 0  移相1  （32 - 3 - 6 - 1 - 6 - len(a)）
g = 0   # 7bit           移相2   (32 - 3 - 6 - 1 - 6 - 8 - len(a))


def joint2():
    a_res = reverse_bit(a, 3)
    b_res = reverse_bit(b, 6)
    c_res = reverse_bit(c, 1)
    d_res = reverse_bit(d, 6)
    f_res = reverse_bit(f, 6)
    g_res = reverse_bit(f, 7)
    print(a_res, b_res, c_res, d_res, f_res, g_res)

    h_res = a_res << (32 - 3)
    print(bin(h_res))
    h_res += b_res << (32 - 3 - 6)
    print(bin(h_res))
    h_res += c_res << (32 - 3 - 6 - 1)
    # print(bin(h_res))
    h_res += d_res << (32 - 3 - 6 - 1 - 6)
    # print(bin(h_res))
    h_res += f_res << (32 - 3 - 6 - 1 - 6 - 6)
    # print(bin(h_res))
    h_res += g_res << (32 - 3 - 6 - 1 - 6 - 8 - 7)
    print(bin(h_res), len(bin(h_res)))
    print(h_res)


def joint3():
    # a_res = reverse_bit(a, 3)
    # b_res = reverse_bit(b, 6)
    # c_res = reverse_bit(c, 1)
    # d_res = reverse_bit(d, 6)
    # f_res = reverse_bit(f, 6)
    # g_res = reverse_bit(f, 7)

    h_res = g << (32 - 7)
    h_res += f << (32 - 8 - 6)
    h_res += d << (32 - 8 - 8 - 6)
    h_res += c << (32 - 8 - 8 - 6 - 1)
    h_res += b << (32 - 8 - 8 - 6 - 1 - 6)
    h_res += a << (32 - 8 - 8 - 6 - 1 - 6 - 3)

    print(bin(h_res), len(bin(h_res)))


if __name__ == '__main__':
    joint3()

