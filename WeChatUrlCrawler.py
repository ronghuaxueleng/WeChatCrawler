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
cookie = "RK=OXF5VYXQSL; ptcz=d6aef6ae7d898679277fd206899c3f75b7c80941f26c87542276429261ff663f; pgv_pvid=9003241064; pac_uid=0_a7bab435a742a; fqm_pvqid=e87916b8-69c6-41e0-825a-3b8a0a745881; tvfe_boss_uuid=2e57caf825c92ff5; ua_id=nfHarAHBLwHm3paLAAAAAFkwASuGykNHC4Kh0eFjuTc=; wxuin=89142924142371; mm_lang=zh_CN; iip=0; _qimei_uuid42=17b0710381e1008a71172fc3b167065760f1c16a35; _qimei_fingerprint=533bd04cd49b52e5249a3f4895339de3; _qimei_q36=; _qimei_h38=21de8c7171172fc3b167065702000001e17b07; suid=ek168846137208123029; uuid=1ab7faa580f44235d657b58f1dd4c13b; _clck=3276594181|1|fnl|0; rand_info=CAESIAfusXEBAzXF/5fIQWQhcbrUGlOMqoYCdhE6ORECwFWx; slave_bizuin=3904718188; data_bizuin=3904718188; bizuin=3904718188; data_ticket=MVyW7vB05VHNKYQea0C3ZDiCmXuLBMs5FvJeqo4jjaycJhhdndK03HP//xpYai+o; slave_sid=VzVMb282MEtTS01BSFYxcF9FSFBKMnBodkxDM0UyQXBSejVXbEV2WVBJa2JmamJpWFN2NUxnMzJNamNjMWJRR2xxUDk5YTNuTDd5UW9JYndCNDlGODgxTWQxY1ZiYkE2bGFRVldhQURiU3JIWFNGeXJ6dkc3UGw5SkVaSFNrMzBjb3BRNVZNR2dmb3dnaFFG; slave_user=gh_59f4fe89993d; xid=4d32a67ffee1716ef049770b04973db6; _clsk=ap3v9j|1721354774631|2|1|mp.weixin.qq.com/weheat-agent/payload/record"

# 使用Cookie，跳过登陆操作

data = {
    "token": "1763065399",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "need_author_name": "1",
    "fakeid": "MzU1ODc3ODkwNA%3D%3D",
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
