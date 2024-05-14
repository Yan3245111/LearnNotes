import math
import matplotlib.pyplot as plt


pri = 100
pri_range = 20
pri_num = 3
pri_pw = 50

pri_list = list()

# PW要小于所有点的百分之90，不然pw就等于最小点的百分之90
# 输入PW


def input_pw():
	res_pw = 0
	for i in range(pri_num):
		res_pri = pri + pri * pri_range / 100 / 2 * math.sin(((i - 1) / pri_num) * 2 * math.pi)
		pri_list.append(res_pri)
		if pri_pw < res_pri * 0.9:
			continue
		else:
			res_pw = res_pri * 0.9
	print(f"input pw={pri_pw}, out pw={res_pw}")


def input_pri():
	# 输入pri，找到最小值然后
	res = 0
	for i in range(1, pri_num + 1):
		# res_pri = pri + pri * pri_range / 100 / 2 * math.sin(((i - 1) / pri_num) * 2 * math.pi)
		res_pri = pri * (pri_range / 100 / 2 * math.sin(((i - 1) / pri_num) * 2 * math.pi) + 1)
		pri_list.append(res_pri)
		if pri_pw < res_pri * 0.9:
			continue
		else:
			res = pri_pw / 0.9 / (pri_range / 100 / 2 * math.sin(((i - 1) / pri_num) * 2 * math.pi) + 1)
	print(f"输入pri={pri_list}, 输出res_pri={res}")


def input_pri_range():
	res_range = 0
	for i in range(pri_num):
		res_pri = pri + pri * pri_range / 100 / 2 * math.sin(((i - 1) / pri_num) * 2 * math.pi)
		pri_list.append(res_pri)
		if pri_pw < res_pri * 0.9:
			continue
		else:
			res_range = (pri_pw / 0.9 - pri) / math.sin(((i - 1) / pri_num) * 2 * math.pi) * 200 / pri
			# print(pri_pw, res_pri, res_pri * 0.9)
	print(f"pri_list={pri_list}, res_range={res_range}")


# 和Num无关
def input_pri_num():
	res_num = 0
	for i in range(pri_num):
		res_pri = pri + pri * pri_range / 100 / 2 * math.sin(((i - 1) / pri_num) * 2 * math.pi)
		pri_list.append(res_pri)
		if pri_pw < res_pri * 0.9:
			continue
		else:
			print(pri_pw, res_pri, res_pri * 0.9)
	print(f"pri_list={pri_list}, input_num={pri_num}, res_num={res_num}")


def open_pwd():
	with open("111.pdw", "rb") as f:
		for i in range(100):
			one_line = f.readline()
			print(len(one_line), one_line)
			if not one_line:
				break
	f.close()


if __name__ == '__main__':
	open_pwd()
	print(0xd0)
	# input_pri()
	# input_pri_range()
	# input_pri_num()
