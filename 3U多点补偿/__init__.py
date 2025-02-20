import matplotlib.pyplot as plt

freq = list()
ampl = list()
step = 1100000
num = int((1150000000 - 50000000) / step + 1)

with open("1100.csv", "r") as fp:
    for i in range(45):
        one_line = fp.readline()
        if one_line.startswith('DATA'):
            for j in range(num):
                one_line = fp.readline()
                one_data = one_line.split(',')
                freq.append(int(one_data[0]))
                ampl.append(float(one_data[1]))
            break

print(freq[0], freq[-1])
plt.xlabel('freq')
plt.ylabel('power')
plt.xlim((freq[0], freq[-1]))
plt.plot(freq, ampl)
plt.show()
