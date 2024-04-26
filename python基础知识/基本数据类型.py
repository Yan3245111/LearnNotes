# int, float, list, dict, tuple, string, set

# 不可变数据类型：int, float, tuple, string
# 可变数据类型：dict, list, set
# 判断条件：不可变数据类型变量更改值的时候，内存地址也跟着改变，可变数据类型内值更改的时候，内存地址不变
a = 1
print(id(a))
a = 2
print(id(a))

b = [1, 2]
print((id(b)))
b[0] = 3
print(id(b))


# list增删改查
b.append(3)
print(b)  # [3, 2, 3]
b.insert(0, 1)
print(b)  # [1, 3, 2, 3]

b.remove(1)
print(b)  # [3, 2, 3]
ddd = b.pop(0)
print(b)  # [2, 3]
print(2222, ddd)  # 3

b[0] = 4
print(b)  # [4, 3]

res = [i for i in b if i == 4]
print(res)


# dict增删改查
c = {1: 2, 3: 4}
print(c)

c[5] = 6
print(c)  # {1: 2, 3: 4, 5: 6}

hhhhh = c.pop(1)
print(c)  # {3: 4, 5: 6}
print(11111, hhhhh)  # pop可以取回删除的k对应的值

c[3] = 3
print(c)  # {3: 3, 5: 6}

del c[3]
print(c)

for k, v in c.items():
    if k == 3:
        print(k, v)
    if v == 6:
        print(k, v)
print(c.get(4))     # None
print(c.get(4, 1))  # 没有key则返回默认值1

# set集合，set里面不存在重复元素
set_list = [1, 2, 3, 4]
print(set(set_list))
set_list[0] = 2
print(set(set_list))
