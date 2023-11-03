# -*- coding: UTF-8 -*-
import hashlib

import requests
import time
import math
import random

from db import Article

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
cookie = "pgv_pvid=2190759718; RK=vXFxAYXYQr; ptcz=829e7a36d4bf9a051959208a5f52ce887ea0239ef7ede4a9ae15855bef809123; user_device_id=bca653d65ade48cf959a52b7db240333; user_device_id_timestamp=1698489332321; ua_id=SljbCRQJgkLP2CngAAAAALqYIWrtJEwt4wO30eDxYZs=; wxuin=99014392727474; uuid=63a2d9bec38c2cdf536530950cf55ce3; _clck=1mo4cpf|1|fge|0; rand_info=CAESIIOI5EydDW6mDQJT49mlG8NuBWAG1mUsC3afMebb94dQ; slave_bizuin=3276594181; data_bizuin=3276594181; bizuin=3276594181; data_ticket=RwDbSefFNfoHFXyolVQJbLeAl640pWgeSX7l6Chh8tNCN/vExNwRaNSxAQxAkaqd; slave_sid=d0FuTzU1SjRsVF9wMTlaTkxSM2dwZlVSREJabEQ3MF91YVJXU1RtY2pQSk41cmN3d2pTcldpbnpHY1BEamtwUHdDaEt1UVdmM3duMHVjcUs4T1B6SnVvQUhReEFGNG84THZuaHljamVubXlNYkxJS2VKZ1Q0eDN0dVFmdEh0VFR4NGJUSHROemVjb2I0WEtB; slave_user=gh_d8d2bdeb345c; xid=a3ea56ea1d5f599dcf3d8fc9d04c4277; mm_lang=zh_CN;"

# 使用Cookie，跳过登陆操作

data = {
    "token": "1904460733",
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
articleCount = Article.select().where(Article.nickname == nickname).count()
print(f"已抓取的公众号文章总条数：{articleCount}")
has_pages = int(math.ceil(articleCount / page_size))
content_json = requests.get(url, headers=headers, params=data).json()
count = int(content_json["app_msg_cnt"])
print(f"公众号文章总条数：{count}")
actual_count = count - articleCount
print(f"要抓取的公众号文章总条数：{actual_count}")
page = int(math.ceil(actual_count / page_size))
print(f"要抓取的公众号文章总页数：{page}")


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


for i in range(has_pages, page):
    begin = i * page_size
    get_one_page_urls(begin)
