# -*- coding: UTF-8 -*-
import requests
import time
import pandas as pd
import math
import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",
]

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
cookie = "appmsglist_action_3276594181=card; RK=OXF5VYXQSL; ptcz=d6aef6ae7d898679277fd206899c3f75b7c80941f26c87542276429261ff663f; pgv_pvid=9003241064; pac_uid=0_a7bab435a742a; fqm_pvqid=e87916b8-69c6-41e0-825a-3b8a0a745881; tvfe_boss_uuid=2e57caf825c92ff5; logTrackKey=6f9ec61f270a4d0b9e98bc527a7b3978; ua_id=nfHarAHBLwHm3paLAAAAAFkwASuGykNHC4Kh0eFjuTc=; wxuin=89142924142371; mm_lang=zh_CN; ptui_loginuin=353752092; iip=0; rand_info=CAESIEhGI512xtOZVQwNSJccgU82X/cKJdveS1+sZMPL9Bl7; slave_bizuin=3276594181; data_bizuin=3276594181; bizuin=3276594181; data_ticket=fc9mDx01ccGuc2+bW9J29B3qBMc4IlDcN7m5DUqfHbrKaI98wihDKDCY7/tg21FM; slave_sid=eTZBa0xFRDR5dm9fRTNoX3l3dENpVXM0ek53ZzJiY0N0NzM2ekdDeGlyWWVFSnVUZVNqcFZ3SnlJaGQ1Q05saEdTc3lOUTZQWm9PZTZRUmNEc2lfZWNXOXM4bDhFVlloeWN0enFXTmVudDVyRmxzdENOaHduN0RPdGFrTUdjS0hFejBlRHBHNGJmTXhBV3dW; slave_user=gh_d8d2bdeb345c; xid=edcd0084f040a677b762dcaac80625a2; _clck=3276594181|1|fge|0; _clsk=1rb9cq3|1698978151904|5|1|mp.weixin.qq.com/weheat-agent/payload/record"

# 使用Cookie，跳过登陆操作

data = {
    "token": "814717580",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "MzAwNTc0Mzc2Ng==",
    "type": "9",
}
headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",

    }
content_json = requests.get(url, headers=headers, params=data).json()
count = int(content_json["app_msg_cnt"])
print(count)
page = int(math.ceil(count / 5))
print(page)
content_list = []
# 功能：爬取IP存入ip_list列表

for i in range(page):
    data["begin"] = i * 5
    user_agent = random.choice(user_agent_list)
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,

    }
    ip_headers = {
        'User-Agent': user_agent
    }
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        items = []
        items.append(item["title"])
        items.append(item["link"])
        t = time.localtime(item["create_time"])
        items.append(time.strftime("%Y-%m-%d %H:%M:%S", t))
        content_list.append(items)
    print(i)
    if (i > 0) and (i % 10 == 0):
        name = ['title', 'link', 'create_time']
        test = pd.DataFrame(columns=name, data=content_list)
        test.to_csv("url.csv", mode='a', encoding='utf-8')
        print("第" + str(i) + "次保存成功")
        content_list = []
        time.sleep(random.randint(60,90))
    else:
        time.sleep(random.randint(15,25))

name = ['title', 'link', 'create_time']
test = pd.DataFrame(columns=name, data=content_list)
test.to_csv("url.csv", mode='a', encoding='utf-8')
print("最后一次保存成功")