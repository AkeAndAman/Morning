from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

os.environ = {'START_DATE': '2022-08-01', 
              'CITY': '清远', 
              'BIRTHDAY': '12-16',
              'APP_ID': 'wx720fa7cc3a736f19',
              'APP_SECRET': 'd7cbd803af03d7175d541ae607a1915f',
              'USER_ID': 'obngy6QJerMZ2HUiJmHWSF59cPNM',
              'USER_ID2': 'obngy6Wqtl9El6R-PefCwogTVVzc',
              'TEMPLATE_ID': 'hB24-tFtybmhtmPuKSdo2yi7qlCS-sU7YnA9NRXtmlM'}

# 未明世事 'USER_ID':'obngy6QJerMZ2HUiJmHWSF59cPNM'
# 懒喵桑   'USER_ID2':obngy6Wqtl9El6R-PefCwogTVVzc'
today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]

def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], weather['wind'], \
           math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days

def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days

def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']

def get_proverb():
    with open(r"E:\PyCharm Community Edition 2019.3.1\pyexample\ex1\python_exicise\tuisong/proverb.txt", encoding="UTF-8") as f:
        content = f.read().splitlines()
        rand_int = random.randint(0, 319)*3
    return content[rand_int], content[rand_int+1]

def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

def get_date():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    time_tuple = datetime.now().timetuple()
    return str(time_tuple[0]) + '年' + str(time_tuple[1]) + '月' + str(time_tuple[2]) + '日', week_list[time_tuple[6]]

if __name__ == '__main__':
    client = WeChatClient(app_id, app_secret)

    wm = WeChatMessage(client)
    wea, wind, temp, low, high = get_weather()
    now_date, now_weekday = get_date()
    proverb_En, proverb_Ch = get_proverb()

    data = {"date": {"value": now_date, "color": get_random_color()},
            "weekday": {"value": now_weekday, "color": get_random_color()},
            "weather": {"value": wea, "color": get_random_color()},
            "wind": {"value": wind, "color": get_random_color()},
            "temperature": {"value": temp, "color": get_random_color()},
            "low": {"value": low, "color": get_random_color()},
            "high": {"value": high, "color": get_random_color()},
            "love_days": {"value": get_count(), "color": get_random_color()},
            "birthday_left": {"value": get_birthday(), "color": get_random_color()},
            "words": {"value": get_words(), "color": get_random_color()},
            "proverb_En": {"value": proverb_En, "color": get_random_color()},
            "proverb_Ch": {"value": proverb_Ch, "color": get_random_color()}}

    wm.send_template(user_id, template_id, data)
    wm.send_template(user_id2, template_id, data)
