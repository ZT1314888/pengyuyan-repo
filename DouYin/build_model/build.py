import joblib
import pandas as pd
from pyexpat import features
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 数据显示
# import numpy as np
# np.set_printoptions(threshold=np.inf)

df = pd.read_csv('../data/data.csv')
time_column = df.iloc[:,5]
seconds = []

for time in time_column:
    minutes,seconds_val = map(int, time.split(':'))
    total_seconds = minutes * 60 + seconds_val
    seconds.append(total_seconds)

df['视频时长'] = seconds

# 特征数据
df['互动率'] = (df['评论数量']+df['分享数量']+df['收藏数量'])
df['发布时间'] = pd.to_datetime(df['发表时间'])
df['发布小时'] = df['发布时间'].dt.hour

# 选取特征和目标字段
features = df[[
    '视频时长','收藏数量','评论数量','分享数量','粉丝数量','互动率','发布小时'
]]

target = df['点赞数量']

# 数据标准化
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# print(features_scaled)

# 划分数据集
X_train,x_test,y_train,y_test = train_test_split(features_scaled,target,test_size=0.2,random_state=42)

# 创建模型
model = LinearRegression()
model.fit(X_train,y_train)

# 评估模型
y_pred = model.predict(x_test)
print(f'模型R2为:{r2_score(y_test,y_pred):.2f}')

joblib.dump(model, 'like_model.joblib')
joblib.dump(scaler, 'likescaler.joblib')