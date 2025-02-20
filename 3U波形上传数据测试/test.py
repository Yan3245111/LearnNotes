from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft
import numpy as np
import math


# 先跳过64个字节
# 2个字节一个点 123456 A路 7-12 B路
# 后32个点是包尾
# 解析的数据是无符号的，所以需要判断是否是有符号的 大于32767则-655535

data_a = list()  # 时间波形
data_b = list()

# a = '55aa'
# num = int(a, 16)
# print(num)


with open("pdw_get_test.csv", "r") as f:
    data = f.read()
    data = data[128: -64]
    # print(data[5000:5200])
    d_len = len(data)
    # print(d_len)
    for i in range(int(d_len / 4)):
        res = i % 12
        one_str = data[i * 4: (i + 1) * 4]
        # print(res, i, one_str)
        try:
            one_data = int(data[i * 4: (i + 1) * 4], 16)
            one_data = one_data - 65535 if one_data > 32767 else one_data
        except ValueError:
            pass
        if res < 6:
            data_a.append(one_data)
        else:
            data_b.append(one_data)

# print(len(data_a), len(data_b))
# print(f"data_a={data_a[:1000]}")
# print(f"data_b={data_b[:1000]}")
plt.plot(data_a)
plt.plot(data_b)
plt.show()
data_x = list()

# 前后数据转换 频率波形 做傅里叶转换
for i in range(12000):
    a = data_a[i]
    b = data_b[i]
    x = complex(a, b)
    data_x.append(x)
# print(f"c_data={data_x[200: 301]}")
fft_x = fft(data_x)
fft_c = fft_x.copy()
# print(f"fft_data={fft_x[:100]}")
fft_x[:6000] = fft_c[6000:]
fft_x[6000:] = fft_c[:6000]
# print(f"fft_data={fft_x[:20]}")

np_fft = np.abs(fft_x)
# print(f"fft_abs={np_fft[:100]}")
res_fft = list()
for i in np_fft:
    res_fft.append(math.log10(i))
# print(f"res_fft={res_fft[:100]}")
plt.plot(res_fft)
plt.show()
