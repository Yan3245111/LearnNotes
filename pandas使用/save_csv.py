import pandas as pd
import numpy as np


csv_path = "1.csv"
s = pd.Series([1, "hello", 2, 3])
print(s)
dates = pd.date_range("20130303", periods=6)
print(dates)

# columns=表头 index=表号 列表方式
df = pd.DataFrame(np.random.randn(6, 3), index=dates, columns=list("ABC"))
print(df)
# 参数为字典
df1 = pd.DataFrame(
    {"A": 1,
     "B": "hello",
     "C": [1, 2, 3],
     "D": "2012"}
)
print(df1)

# 更新列数据，如果只有一个参数，则只更新此列的第一个数据
df1["B"].update(["what", "what", "what"])
print(df1)

# 保存文件，index 选择存储是否有下标，header 选择是否存储表头，以“,”作为分隔符
df1.to_csv(csv_path, header=True, sep=',', index=False)

# 切片：行为单位
print(df1[:2])

# 切片：列
print(df1["A"])

# 切片：行，列
print(df1.loc[:2, ["A", "B"]])

# 切片：按照列的下标切片
print(df1.iloc[2])

# 切片：按照列行的下标切片  第0行 第2行，的第0列和第1列
print(df1.iloc[[0, 2], [0, 1]])

# 切片：获取明确数值
print(df1.iloc[0, 3])
print(df1.iat[0, 3])

# 切片:赋值 整列
df1["E"] = [4, 5, 6]
print(df1)
# 切片：赋值
df1.iat[1, 1] = 2
print(df1)


# 一行一行存储数
f_path = '1.csv'

fd = pd.DataFrame(columns=["1", "2", "3"])
fd.loc[len(fd)] = [1, 2, 3]
fd.loc[len(fd)] = [4, 5, 6]
fd.to_csv(f_path, sep=',', index=False)

