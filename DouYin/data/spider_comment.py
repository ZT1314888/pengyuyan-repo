import time,urllib
import csv,pandas
import execjs,requests
import urllib.parse

headers = {
    "cookie": "enter_pc_once=1; UIFID_TEMP=30ff7b230d01f3ed4fd5546706fc508e0725b8a99e0ba4197a991a959864baf0aab46357ea51cd224262d18f6190155c2021990485b217d256f8b46eee938a516a4f960aa9d289516688b00d23f8ea0a; hevc_supported=true; odin_tt=096ffdffb10b8bbe040ac30cc9b174c786ada4655d35c91a6ad9efcc248782cef6710426d2472a588a9960c7d1bff571c8cf21e922c00da19838016b30ddf506aa018d5ce39bbacb6351246fdeb4b568; passport_csrf_token=69b4a6a752f79493f20f55adf8a12e05; passport_csrf_token_default=69b4a6a752f79493f20f55adf8a12e05; __security_mc_1_s_sdk_crypt_sdk=c6312097-4ccb-84d7; bd_ticket_guard_client_web_domain=2; is_dash_user=1; UIFID=30ff7b230d01f3ed4fd5546706fc508e0725b8a99e0ba4197a991a959864baf02e5406c247f0d7afd99f8348d6d20585b22018b231ce486834f368b0f80d19254014abb2ed5de54944f66786191638a0f209fb408c514d6600625cbe58e7c14c8567e4a7fbf46945930dd51e750bfe00878ab772be88487fe7e323e2e7b919b0c8c430eaf546fd28ee7e5f096acd21167e061a8b160e1509081070435da333a3; download_guide=%223%2F20250924%2F0%22; SEARCH_RESULT_LIST_TYPE=%22single%22; WallpaperGuide=%7B%22showTime%22%3A1758704122152%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A35%2C%22cursor2%22%3A10%7D; IsDouyinActive=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A4.25%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; strategyABtestKey=%221758786720.446%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.299%7D; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRzFtSTIyN054Q0JYSWRDbCswdlhHWENpN2xvbzQ4N0NYS251bEJjbElUZG5qaXdiRkpOZVJiY2pZZDdGdWVjQldKUE5iRFR1Nnc3VnVEY1ZkcDY1OUE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; gulu_source_res=eyJwX2luIjoiMzczYjUwZjEwMjE1MTQ5YzM3YTMxYjVjNjA1ZDk0Y2JmYTI2YzkwZWE5MGIxMTNiN2JhMmU1ZTVjNjAyOTJhZiJ9; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f27303732363732333d323d303234272927676c715a75776a716a666a69273f2763646976602778; bit_env=cIxiYefD09Jo8uwih5XYTFdfEaTlv7yFfboajQ0yDWL8b-AJgJfpIq09kbxfK1Kuh5h44sTBEI88LD6C7-uD_gDgueOr6vXrCJQCZ8ZeqNL_0Pb8jgwlQGXLh0DEx4FlLjMf8V7L-fA_i7S1HKJMXO-ZdCJQ1w2anF6yf7xSE88Z5FFS9b-eBTB_1XNAXnjwupmk0UQH-d7tXfABl6s-gmTsJsmLKZyTtzDPK_DtawuOS28-rml1VZwRUpnmePnj3C29QdWhOv9uohH-pQihWIjfALAg7QdQoKhiE-UaCmIeAimVuj5xvJazRHXlSNoNivrZyocPecHtSHX3OCW8QQ_9IwhTEwWWM4sFCE6wENb_lRRweImpoMFbPN-CtzP1QSGs_rARblRbnC2iyisYr5AqLgv-1ydNZvy9U60xghB27iH94psC2uZsMyHbQNm8o9oztd_tfYiJ0uxSPoiKBZz20HuHz2NbiCsxRZedavemQNKFYI1S6Pu8j82arPlrKU9neIi8n2_Ms_z9Gw-kfNIW2p6r9WjbO7PcwkaoWos%3D; passport_auth_mix_state=bguqtdfxkofqlh3ua284w9c1v7i950gz; biz_trace_id=1129c853; ttwid=1%7CCJBZs_Vp_Cmgf8UYtTpDoE8Ir_180cZGbjEKVG3Vd-w%7C1758786745%7Ce58569ae57b8fd3cd5a084ec24d6d5d5aa9194e6fa6ff2fad389182ea6a3d352",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "accept": "application/json, text/plain, */*"
}

def get_time(ctime):
    time_local = time.localtime(ctime)
    time_format = time.strftime("%Y.%m.%d", time_local)
    return str(time_format)

def get_json(aweme_id,cursor):
    url = f"https://www-hj.douyin.com/aweme/v1/web/comment/list/?aid=6383&aweme_id={aweme_id}&count=20&cursor={cursor}"
    query = urllib.parse.urlparse(url).query
    a_bogus = execjs.compile(open('XB.js').read()).call('sign',query,headers.get('user-agent'))
    video_url = url + '&X-Bogus=' + a_bogus
    time.sleep(1)
    # params = {
    #     "aweme_id": "7553658713983274300",
    #     "cursor": "0",
    #     "count": "10",
    #     "platform": "PC",
    #     "downlink": "4.25",
    # }
    response = requests.get(video_url, headers=headers)
    return response.json()

def parseData(feed,aweme_id):
    ip_label = feed.get('ip_label')
    try:
        username = feed['user']['nickname']
    except:
        username = '暂无用户名'

    commit_dict = {
        '用户id' : feed['user']['uid'],
        '用户名' : username,
        '评论时间' : get_time(feed['create_time']),
        'IP地址' : ip_label,
        '评论内容' : feed.get('text',''),
        '点赞数量' : feed.get('digg_count',''),
        'aweme_id' : aweme_id
    }
    print(commit_dict)
    writer.writerow(commit_dict)

def spider_comment(aweme_id):
    cursor = 0
    page = 1

    while True:
        response = get_json(aweme_id,cursor)
        try:
            if response['comments'] is None :
               break
            feeds = response['comments']
            for feed in feeds:
                parseData(feed,aweme_id)
            if response['has_more'] == 0:
                break

            cursor +=  20
            page+=1

            if page > 20:
                break
        except Exception as e:
            print(f'爬取失败:{e}')
            continue

if __name__ == '__main__':
    header = ['用户id','用户名','评论时间','IP地址','评论内容','点赞数量','aweme_id']
    f = open('comment_data.csv', 'a', encoding='utf-8', newline='')
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    df = pandas.read_csv('data.csv')
    for index,row in df.iterrows():
        spider_comment(row['视频id'])