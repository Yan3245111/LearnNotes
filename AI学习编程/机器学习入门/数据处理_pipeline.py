import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer  # 填充缺失值
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder  # 缩放到均值0，方差1, 更改字符串为[0, 1] [1, 0]
from sklearn.ensemble import RandomForestClassifier  
from sklearn.model_selection import train_test_split


# 缺失值填充 -中位数 -众数
df = pd.DataFrame({
    "age": [5, 15, 25, 35, None, 55, 65, 75, 85],
    "sex": ["male", None, "female", "female", "male", "male", "female", "male", "male"],
    "deposit": [0, 1000, 5000, 1e4, 30e4, 100e4, 20e4, 15e4, None]
})

# 目标值里有None无法进行训练，必须先补值再训练，如果训练里也不提前补了，训练的时候就不需要重新补，直接写缩放就行
y_imputer = SimpleImputer(strategy="median")
df["deposit"] = y_imputer.fit_transform(df[["deposit"]]).ravel()

x = df.drop("deposit", axis=1)
y = df["deposit"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

# 提取数字和字符串
num_feature = ["age"]
str_feature = ["sex"]
# 数字和字符训练
num_transformer = Pipeline(steps=[("num", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
str_transformer = Pipeline(steps=[("str", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])

# 组合
result = ColumnTransformer(transformers=[("num", num_transformer, num_feature), 
                                        ("str", str_transformer, str_feature)])
res_transformer = Pipeline(steps=[("res", result), ("filter", RandomForestClassifier())])

# 学习
res_transformer.fit(x_train, y_train)
y_pre = res_transformer.predict(x_test)

print(y_test)
print(y_pre)