import csv
import random
import time

import requests

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "priority": "u=1, i",
    "referer": "https://www.douyin.com/search/%E5%93%AA%E5%90%922?aid=62246133-4418-4a46-9979-33d6a2c4969f&type=general",
    "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "uifid": "30ff7b230d01f3ed4fd5546706fc508e0725b8a99e0ba4197a991a959864baf02e5406c247f0d7afd99f8348d6d20585b22018b231ce486834f368b0f80d19254014abb2ed5de54944f66786191638a0f209fb408c514d6600625cbe58e7c14c8567e4a7fbf46945930dd51e750bfe00878ab772be88487fe7e323e2e7b919b0c8c430eaf546fd28ee7e5f096acd21167e061a8b160e1509081070435da333a3",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
}

cookies = {
    "enter_pc_once": "1",
    "UIFID_TEMP": "30ff7b230d01f3ed4fd5546706fc508e0725b8a99e0ba4197a991a959864baf0aab46357ea51cd224262d18f6190155c2021990485b217d256f8b46eee938a516a4f960aa9d289516688b00d23f8ea0a",
    "hevc_supported": "true",
    "dy_swidth": "1536",
    "dy_sheight": "864",
    "fpk1": "U2FsdGVkX1/B2vKpQg8+86j7Bx4a7pYMy1V45gMIvyjMfTB6T1xN+OpZ9G1Kl6jaMpQx4A6te3JHqEls7orTzg==",
    "fpk2": "7ceed19ee5ebdbf792f56329591ffc53",
    "s_v_web_id": "verify_mfl9t20n_HNa1lXGM_Z6DE_4mkb_8MQP_pstTwMppcSID",
    "odin_tt": "096ffdffb10b8bbe040ac30cc9b174c786ada4655d35c91a6ad9efcc248782cef6710426d2472a588a9960c7d1bff571c8cf21e922c00da19838016b30ddf506aa018d5ce39bbacb6351246fdeb4b568",
    "xgplayer_user_id": "990058994960",
    "passport_csrf_token": "69b4a6a752f79493f20f55adf8a12e05",
    "passport_csrf_token_default": "69b4a6a752f79493f20f55adf8a12e05",
    "__security_mc_1_s_sdk_crypt_sdk": "c6312097-4ccb-84d7",
    "bd_ticket_guard_client_web_domain": "2",
    "is_dash_user": "1",
    "UIFID": "30ff7b230d01f3ed4fd5546706fc508e0725b8a99e0ba4197a991a959864baf02e5406c247f0d7afd99f8348d6d20585b22018b231ce486834f368b0f80d19254014abb2ed5de54944f66786191638a0f209fb408c514d6600625cbe58e7c14c8567e4a7fbf46945930dd51e750bfe00878ab772be88487fe7e323e2e7b919b0c8c430eaf546fd28ee7e5f096acd21167e061a8b160e1509081070435da333a3",
    "strategyABtestKey": "%221758377108.339%22",
    "volume_info": "%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D",
    "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRzFtSTIyN054Q0JYSWRDbCswdlhHWENpN2xvbzQ4N0NYS251bEJjbElUZG5qaXdiRkpOZVJiY2pZZDdGdWVjQldKUE5iRFR1Nnc3VnVEY1ZkcDY1OUE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
    "ttwid": "1%7CCJBZs_Vp_Cmgf8UYtTpDoE8Ir_180cZGbjEKVG3Vd-w%7C1758377874%7Cff3688f42506e7f8a24542b46c9e316c34eb8c2d0896f3ee6a136ddcacd69519",
    "douyin.com": "",
    "xg_device_score": "7.86629764749857",
    "device_web_cpu_core": "20",
    "device_web_memory_size": "8",
    "architecture": "amd64",
    "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22",
    "download_guide": "%223%2F20250924%2F0%22",
    "__ac_nonce": "068d3b1fa00eb8ddde377",
    "stream_player_status_params": "%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22",
    "__ac_signature": "_02B4Z6wo00f016yL1kgAAIDDIsagf8RLJPOsq9LAAIP575",
    "SEARCH_RESULT_LIST_TYPE": "%22single%22",
    "csrf_session_id": "580fa10148854e931e65f47b1c585a67",
    "WallpaperGuide": "%7B%22showTime%22%3A1758704122152%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A16%2C%22cursor2%22%3A4%7D",
    "IsDouyinActive": "true",
    "home_can_add_dy_2_desktop": "%221%22"
}

url = "https://www.douyin.com/aweme/v1/web/search/item/"

def get_time(ctime):
    time_local = time.localtime(ctime)
    time_format = time.strftime("%Y.%m.%d", time_local)
    return str(time_format)

def get_json(keyword, offset, count):
    params = {
        "aid": '6383',
        "channel": "channel_pc_web",
        "search_channel": "aweme_general",
        "keyword": keyword,
        "search_source": "normal_search",
        "query_correct_type": "1",
        "is_filter_search": "0",
        "from_group_id": "",
        "disable_rs": "1",
        "offset": offset,
        "count": count,
        "need_filter_settings": "0",
        "search_id": "20250924170048729042A688292E395F53",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "20",
        "version_code": "190600",
        "version_name": "19.6.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "140.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "140.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "150",
    }
    time.sleep(random.randint(1, 5))
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    return response.json()


def parseData(response, writer):
    minutes = response['video']['duration'] // 1000 // 60
    seconds = response['video']['duration'] // 1000 % 60
    video_dict = {
        '用户名': response['author']['nickname'].strip(),
        '粉丝数量': response['author']['follower_count'],
        '视频描述': response['desc'],
        '视频id': response['aweme_id'],
        '发表时间': get_time(response['create_time']),
        '视频时长': "{:02d}:{:02d}".format(minutes, seconds),
        '点赞数量': response['statistics']['digg_count'],
        '收藏数量': response['statistics']['collect_count'],
        '评论数量': response['statistics']['comment_count'],
        '分享数量': response['statistics']['share_count'],
        '下载数量': response['statistics']['download_count'],
    }

    print(video_dict)
    writer.writerow(video_dict)

def search(keyword):
    offset = 20
    count = 16
    while True:
        response = get_json(keyword, offset, count)

        feeds = response['data']
        for feed in feeds:
            parseData(feed['aweme_info'], writer)

        if not response.get('has_more', 0):
            break

        offset = offset + count
        count = 10


if __name__ == '__main__':
    # keyword = input('')
    header = ['用户名', '粉丝数量', '视频描述', '视频id', '发表时间', '视频时长','点赞数量', '收藏数量', '评论数量', '分享数量', '下载数量']

    f = open('data.csv', 'a', encoding='utf-8', newline='')
    writer = csv.DictWriter(f, header)
    writer.writeheader()

    keyword = '哪吒2'
    search(keyword)