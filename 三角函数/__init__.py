import math

# x = 5
# math.acos(x)  # 返回x的反余弦 弧度值。
# math.asin(x)  # 返回x的反正弦 弧度值。
# math.degrees(x)  # 将弧度转换为角度, 如 degrees(math.pi/2) ，shu 返回90.0
# math.radians(x)  # 将角度转换为弧度


angle = 50
a_sin = math.sin(math.radians(angle))
print(a_sin)

fan_angle = math.degrees(math.asin(a_sin))
print(fan_angle)


# 弧度 角度转换
a_hu = math.radians(angle)
print(a_hu)
a_angle = math.degrees(a_hu)
print(a_angle)


# sin 求数字的正弦，如果是角度的话，需要先转成弧度math.radians
hu = math.radians(40)
print("hu", hu)
sin = math.sin(hu)
print("sin", sin)
# asin 求反正弦，然后使用math.degrees求角度
a_sin = math.asin(sin)
print("a_sin", a_sin)
a_angle = math.degrees(a_sin)
print("a_angle", a_angle)
