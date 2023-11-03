# -*- coding: UTF-8 -*-
import hashlib

import requests
import time
import math
import random

from db import Info, Article

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
    "need_author_name": "1",
    "fakeid": "MzAwNTc0Mzc2Ng==",
    "type": "9",
}
headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",

}
nickname = '鱼羊史记'
md = hashlib.md5()
md.update(nickname.encode('utf-8'))
wx_name = md.hexdigest()  # 公众号名称
page_size = 4
content_json = requests.get(url, headers=headers, params=data).json()
count = int(content_json["app_msg_cnt"])
print(f"公众号文章总条数：{count}")
page = int(math.ceil(count / page_size))
print(f"公众号文章总页数：{page}")
content_list = []
if count > 0:
    info_exists = Info.select().where(Info.name == wx_name).exists()
    if not info_exists:
        info_data = {}
        info_data['name'] = md.hexdigest()
        info_data['count'] = count
        info_data['pages'] = page
        Info.insert(info_data).execute()


def get_one_page_urls(begin):
    data["begin"] = begin
    user_agent = random.choice(user_agent_list)
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,

    }
    try:
        # 使用get方法进行提交
        content_json = requests.get(url, headers=headers, params=data).json()
        # 返回了一个json，里面是每一页的数据
        for item in content_json["app_msg_list"]:
            try:
                # 提取每页文章的标题及对应的url
                postId = hashlib.md5()
                postId.update(item["link"].encode('utf-8'))
                article_data = {}
                article_data['postId'] = postId.hexdigest()
                article_data['nickname'] = nickname
                article_data['title'] = item["title"]
                article_data['url'] = item["link"]
                Article.insert(article_data).execute()
            except Exception as e:
                print(e)

        print(f"第{i}页爬取完成")
        if (i > 0) and (i % 10 == 0):
            sleep_seconds = random.randint(60, 90)
            print(f"等待{sleep_seconds}秒")
            time.sleep(sleep_seconds)
        else:
            sleep_seconds = random.randint(25, 35)
            print(f"等待{sleep_seconds}秒")
            time.sleep(sleep_seconds)
    except Exception as e:
        print(e)
        print(f"重试，begin={begin}")


for i in range(page):
    begin = i * page_size
    get_one_page_urls(begin)
    Info.update(grabCount=begin + page_size, count=count).where(Info.name == wx_name).execute()
