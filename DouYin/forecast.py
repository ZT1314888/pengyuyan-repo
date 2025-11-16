import joblib
import pandas as pd

model = joblib.load('build_model/like_model.joblib')
scaler = joblib.load('build_model/likescaler.joblib')

def predict_likes(input_data):
    features =[
        input_data['duration'],
        input_data['collect'],
        input_data['comment'],
        input_data['share'],
        input_data['fans'],
        input_data['interaction_rate'],
        input_data['hour'],
    ]

    feature_names = ['视频时长', '收藏数量', '评论数量', '分享数量', '粉丝数量', '互动率', '发布小时']
    df = pd.DataFrame([features], columns = feature_names)

    scaler_features = scaler.transform(df)
    prediction = model.predict(scaler_features)

    return round(prediction[0],0)


example_data = {
    'duration': 360,
    'collect': 6000,
    'comment': 8000,
    'share': 5000,
    'fans': 600,
    'interaction_rate': 0.23,
    'hour': 19
}

print(predict_likes(example_data))


"""
多爬取数据信息，换题材
最后评估模型
"""