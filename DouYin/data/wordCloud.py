import jieba
import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from config import Config
from data.csv_to_sql import cursor

conn = pymysql.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    db=Config.DB_NAME,
)

cursor = conn.cursor()

import matplotlib
matplotlib.use('Tkagg')

def video_title_wordcloud():
    sql = 'select description from videodata'
    cursor.execute(sql)
    data = cursor.fetchall()


    text = ''
    for row in data:
        if row[0]:
            text += row[0]

    data_cut = jieba.cut(text,cut_all=False)
    word_text = ' '.join(data_cut)

    wordcloud = WordCloud(
        width = 800,
        height = 400,
        background_color = 'white',
        font_path = 'STHUPO.TTF',
        max_words = 300,
        max_font_size = 100,
        min_font_size = 10,
        collocations = False,
        prefer_horizontal = 0.8,
    )
    wordcloud.generate(word_text)

    plt.figure(figsize=(12, 10))
    plt.imshow(wordcloud,interpolation='bilinear')

    plt.axis('off')
    plt.show()
    plt.savefig('')

# video_title_wordcloud()

def comment_wordcloud():
    sql = 'select content from commentdata'
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for row in data:
        if row[0]:
            text += row[0]

    data_cut = jieba.cut(text, cut_all=False)
    word_text = ' '.join(data_cut)

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        font_path='STHUPO.TTF',
        max_words=300,
        max_font_size=100,
        min_font_size=10,
        collocations=False,
        prefer_horizontal=0.8,
    )
    wordcloud.generate(word_text)

    plt.figure(figsize=(12, 10))
    plt.imshow(wordcloud, interpolation='bilinear')

    plt.axis('off')
    plt.show()
    plt.savefig('')


comment_wordcloud()