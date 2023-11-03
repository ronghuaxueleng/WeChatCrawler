import hashlib
import io
import os
import re
import sys

import requests

from db import Article, Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
url_file = "url1.csv"
name = ['title', 'link', 'create_time']


def save_image_urls():
    pattern = r"data-src=\"(?P<url>https:\/\/mmbiz\.qpic\.cn\S+)\""
    regex = re.compile(pattern)
    articles = Article.select().where(Article.grabState != 1).execute()
    if len(articles) > 0:
        for article in articles:
            url = article.url
            print(url)
            res = requests.get(url)
            text = res.text
            image_urls = regex.findall(text)
            md = hashlib.md5()
            md.update(url.encode('utf-8'))
            postId = md.hexdigest()
            if len(image_urls) > 0:
                for image_url in image_urls:
                    try:
                        image_data = {}
                        image_data['postId'] = postId
                        image_data['image_url'] = image_url
                        Image.insert(image_data).execute()
                    except Exception as e:
                        print(e)
            Article.update(grabState=1).where(Article.postId == postId).execute()


def request_get(url, ret_type="text", timeout=5, encoding="GBK"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers, timeout=timeout)
    res.encoding = encoding
    if ret_type == "text":
        return res.text
    elif ret_type == "image":
        return res.content


def save_image(image_src):
    md = hashlib.md5()  # 获取一个md5加密算法对象
    md.update(image_src.encode('utf-8'))  # 制定需要加密的字符串
    file_local_path = f"./img/{md.hexdigest()}.jpg"
    if not os.path.exists(file_local_path):
        content = request_get(image_src, "image")
        with open(file_local_path, "wb") as f:
            f.write(content)
            print("图片保存成功")


if __name__ == '__main__':
    save_image_urls()
    # with open('data.json', 'r', encoding='UTF-8') as f:
    #     os.makedirs('img', exist_ok=True)
    #     data_list = json.load(f)
    #     for image_src in data_list:
    #         save_image(image_src)
