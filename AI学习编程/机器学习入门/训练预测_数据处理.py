import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder


data = {
    "age": [25, 30, None, 35, 40, 21, 18, 50, 22, 100],
    "fare": [100, 50, 80, None, 120, 60, 88, 30, 50, 110], # 费用
    "sex": ["male", "female", "male", "female", "male", "male", "male", "female", "male", "female"],
    "embarked": ["S", "C", "S", "Q", "S", "S", "C", "S", "Q", "S"], # 登录港口
    "survived": [0, 1, 0, 1, 1, 0, 0, 1, 0, 0]
}

df = pd.DataFrame(data)
x = df.drop("survived", axis=1)  # 删除survived这列, 提取所有特征
y = df["survived"]  # 标签/标准答案
# 训练用的特征，测试用的特征，训练用的真实结果，测试用的真实结果
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# print(x_train)
# print(x_test)
# print(y_train)
print(y_test)


numberic_features = ["age", "fare"]  # 数字类型
categorical_features = ["sex", "embarked"]  # 分类类型

# 补缺失值 用中位数 数据缩放标准化 作用：处理数字列，空值补中位数，然后把数字缩放到统一范围，均值0，方差1
numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])

# 补缺失值 用众数 再独热编码 作用：处理分类列，空值补出现最多的值，然后把文字变为0/1矩阵，例如male=[1, 0]，female=[0, 1]
categorical_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])

# 组合流程 数字走数字流程，分类走分类流程
preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, numberic_features), 
                                                ("cat", categorical_transformer, categorical_features)])

# 把预处理和模型放在一起
full_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", RandomForestClassifier())])

full_pipeline.fit(x_train, y_train)
y_pred = full_pipeline.predict(x_test)
print(y_pred)

# 用自己写的数据集进行预测
new_data = pd.DataFrame({
    "age": [100],
    "fare": [30],
    "sex": ["female"],
    "embarked": ["C"]
})

res = full_pipeline.predict(new_data)
print(res)
