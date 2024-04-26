# lambda函数使用
func = lambda x, y: x * y
print(func(3, 4))

hello = lambda d=1, f=2: print(d - f)
hello()


# 切片使用
a_list = [1, 2, 3, 4]
h, *hh, hhh = a_list
print(*hh)

# for使用
for x, y in [(1, 2), (3, 4)]:
    print(x, y)


# 变量注释
def hello(items: list):
    """
    :param items:
    :type items:
    """
    print(items)


# 冒泡排序
def bubble_sort():
    num_list = [5, 2, 1, 10, 23, 4, 13]
    for i in range(1, len(num_list)):
        for j in range(0, len(num_list) - 1):
            if num_list[j] > num_list[i]:
                num_list[j], num_list[j + 1] = num_list[j + 1], num_list[j]
    print(num_list)


if __name__ == '__main__':
    bubble_sort()
