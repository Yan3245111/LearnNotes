import pandas as pd 
from sklearn.impute import SimpleImputer  # 填充缺失值
from sklearn.preprocessing import StandardScaler  # 缩放到均值0，方差1
from sklearn.linear_model import LinearRegression  # 线性处理，得线性的才可以，像这个不是线性的训练就是错的
from sklearn.model_selection import train_test_split


# 缺失值填充 -中位数 -众数
df = pd.DataFrame({
    "age": [5, 15, 25, 35, None, 55, 65, 75, 85],
    "sex": ["male", None, "female", "female", "male", "male", "female", "male", "male"],
    "deposit": [0, 1000, 5000, 1e4, 30e4, 100e4, 20e4, 15e4, None]
})

imp_median = SimpleImputer(strategy="median")
df["age"] = imp_median.fit_transform(df[["age"]]).ravel()
df["deposit"] = imp_median.fit_transform(df[["deposit"]]).ravel()
# print("df age impute median\n", df["age"])

imp_most = SimpleImputer(strategy="most_frequent")
df["sex"] = imp_most.fit_transform(df[["sex"]]).ravel()
# print("df sex impute most\n", df["sex"])
print(f"impute after df={df}")

df["sex"] = df["sex"].map({"male": 1, "female": 0})

# 缩放
scale_transform = StandardScaler().fit_transform(df[["age"]]).ravel()

# 训练集，测试集
x = df.drop("deposit", axis=1)
y = df['deposit']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 模型训练 必须把字符串做01化，不然会报错/
model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
print(111111111111111)
print(y_test)
print(y_pred)