import numpy as np
import pandas as pd
import pymysql
from config import Config

conn = pymysql.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    db=Config.DB_NAME,
)

cursor = conn.cursor()

def save_video_info():
    sql = ('insert into videodata(username,fansCount,description,aweme_id,publishTime,'
           'duration,likeCount,collectCount,commentCount,shareCount,downloadCount)'
           'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
    df = pd.read_csv('data.csv')
    # df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        cursor.execute(sql, tuple(row))
    conn.commit()
    cursor.close()
    conn.close()

# save_video_info()

def save_comment_info():
    sql = ('insert into commentdata(userid,username,commentTime,userIP,content,likeCount,aweme_id)'
           'values(%s,%s,%s,%s,%s,%s,%s)')
    df = pd.read_csv('comment_data.csv')
    df = df.dropna(subset=['评论内容'])
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        # row_data = tuple(None if pd.isna(x) else x for x in row)
        cursor.execute(sql, tuple(row))
    conn.commit()
    cursor.close()
    conn.close()

save_comment_info()