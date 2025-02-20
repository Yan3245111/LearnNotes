import os
import pandas as pd

all_data = list()
step = 1100000

path = "C:/Users/Radsim/Desktop/3U线性调频数据/240819"
num = int((1150000000 - 50000000) / step + 1)
one_line = list()

for i in range(79):
    if i == 78:
        file = str((i + 1) * 500000) + ".0.csv"
        file_path = path + '/' + file
    else:
        file = str((i + 1) * 500000 + 100000) + ".0.csv"
        file_path = path + '/' + file
        print(file)
    if os.path.exists(file_path):
        with open(file_path, "r") as fp:
            for j in range(50):
                line = fp.readline()
                if line.startswith('DATA'):
                    for x in range(num):
                        line = fp.readline()
                        if line:
                            one_data = line.split(',')
                            # print(float(one_data[1]))
                            one_line.append(int(one_data[0]))
                            one_line.append(float(one_data[1]))
                            # print(one_line)
                            all_data.append(one_line)
                            one_line = list()
                    break
    else:
        print(1)
# print(all_data)
data_frame = pd.DataFrame(all_data)
data_frame.to_csv("all_data.csv", header=True, sep=',', index=False)

# 24136%U052745 证书编号

# print(len(all_data))
