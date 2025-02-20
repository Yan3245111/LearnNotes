import pandas as pd

df = pd.read_csv("1.csv")
print(df["A"])


# 读取 CSV 文件  取某列中形同元素的所有行 方法1
def get_group_one_title():
    # 指定你要查找的值
    value_to_find = 'A'  # 替换为你想查找的值
    # 使用布尔索引提取所有匹配的行
    matching_rows = df[df['A'] == value_to_find]
    print(matching_rows)

# 方法2
def get_group_one_title1():
    # 根据某一列分组
    grouped = df.groupby('A')
    # 获取某个特定组的所有行
    matching_rows = grouped.get_group(1)  # 替换为你想查找的值
    print(len(matching_rows))
    print(matching_rows)
    a = matching_rows["A"].iloc[1]
    print(a)


# 读取 CSV 文件 新增一列
def insert_new_col():
    # 初始化 num 列
    df['num'] = 0
    # 按行添加
    for i in range(len(df)):
        df.at[i, 'num'] = i + 1
    # 保存到新的 CSV 文件
    df.to_csv('updated_file.csv', index=False)


# 取第0行，NumAtt列的值
def get_row_value(row_id: int):
    value = df.at[row_id, "A"]


# 获取某一列形同数据
def get_unique():
    all_a = df["A"].unique()
    print(all_a)


# 快速查询
def find_one_value():
    df = pd.read_csv("YWC10M.csv")
    df1 = df.set_index(['ROW_ID', 'FREQ'])
    att1 = df1.at[(0, 200), "ATT1"]
    att2 = df1.at[(0, 200), "ATT2"]
    print(att1, att2)


if __name__ == '__main__':
    find_one_value()
