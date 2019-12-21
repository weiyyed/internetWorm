# 今日头条图片抓取
import json
import re
import urllib.parse
from _md5 import md5
from json import JSONDecodeError
from hashlib import md5
import os
# from multiprocessing.pool import Pool

import pymongo
import requests
# 获取搜素页的json数据
import urllib3
from requests import RequestException
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from config.toutiao_conf import *

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def generate_session():
#     创建一个session
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Connection': 'keep-alive',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    cookies_dic = {
        "tt_webid": "1",
        "s_v_web_id": "1",
        "WEATHER_CITY": "%E5%8C%97%E4%BA%AC",
        "tt_webid": "1",
        "csrftoken": "1",
        "tasessionId": "1",
    }
    sess= requests.session()
    sess.headers.update(headers)
    for k,v in cookies_dic.items():
        sess.cookies.set(k,v)
    return sess
def get_main_page(offset,keyword,session):
    url="https://www.toutiao.com/api/search/content/?"
    params={
        "aid":"24",
        "app_name":"web_search",
        "offset":offset,
        "format":"json",
        "keyword":keyword,
        "autoload":"true",
        "count":"20",
        "en_qc":"1",
        "cur_tab":"1",
        "from": "search_tab",
        "pd": "synthesis",
        "timestamp": "1575469639909"
    }
    url=url+urllib.parse.urlencode(params)
    try:
        if isinstance(session,requests.sessions.Session):
            urllib3.disable_warnings(InsecureRequestWarning)
            response=session.get(url,verify=False)
            if response.status_code==200:
                return response.text
            return None
    except RequestException:
        raise Exception("请求失败了")
def parse_main_page(html):
    html=json.loads(html)
    if html and "data" in html.keys():
        for data in html["data"]:
            if "article_url" in data.keys():
                yield  data["article_url"]
    else:
        raise Exception("json 数据没有data")
def get_detail_page(url,session):
    if isinstance(session, requests.sessions.Session):
        response=session.get(url)
        return response.text
def parse_detain_page(html,url):
    bf=BeautifulSoup(html,"lxml")
    title=bf.select("title")[0].get_text() if bf.select("title") else None
    # 组图时使用此正则
    pattern=re.compile(r'gallery: JSON.parse\("({.*?})"\),',re.S)
    result=re.search(pattern,html)
    images=[]
    if result:
        # url中含有unicode字符，需要转换普通文本
        data=result.group(1).encode("utf-8").decode("unicode_escape")
        data=json.loads(data)
        # print("data:",data)
        if data and "sub_images" in data.keys():
            sub_images=data.get("sub_images")
        images.extend([s["url"] for s in sub_images])
    else:
        pattern = re.compile(r'&quot;http(.*?)\\&quot;', re.S)
        images = re.findall(pattern, html)
        print(images)
        for n in range(len(images)):
            images[n]="http"+images[n]
            images[n] = images[n].encode("utf-8").decode("unicode_escape")
    for i in images:download_image(i)
    yield  {
        "title":title,
        "url":url,
        "images_url":images
    }
def download_image(url):
    print("正在下载图片",url)
    # if isinstance(session, requests.sessions.Session):
    #     response=session.get(url)
    response=requests.get(url)
    if response.status_code==200:
        save_to_file(response.content)
        # return response.content
def save_to_file(conment):
    filepath="{0}//images/{1}.jpg".format(os.getcwd(),md5(conment).hexdigest())
    if not os.path.exists(filepath):
        with open(filepath,"wb") as f:
            f.write(conment)
def save_to_mongo(result):
    if db[MONGO_DB].insert(result):
        print("存储到mogon成功")
        return True
    return False
def main(offset):
    session=generate_session()
    html=get_main_page(offset, KEYWORD,session)
    for url in parse_main_page(html):
        detail_html=get_detail_page(url,session)
        # 存储到mogon
        # for detain in parse_detain_page(detail_html,url):
        #     save_to_mongo(detain)

if __name__ == '__main__':
    # main(0)
    # groups=[x*20  for x in range(GROUP_END+1)]
    # pool=Pool()
    # pool.map(main,groups)
    for x in range(GROUP_END+1):
        main(x)