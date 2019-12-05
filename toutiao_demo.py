# 今日头条图片抓取
import json
import urllib.parse
import requests
# 获取搜素页的json数据
from requests import RequestException

def get_main_page(offset,keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Connection': 'keep-alive',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
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
    cookies_dic={
        "tt_webid" : "1",
        "s_v_web_id" : "1",
        "WEATHER_CITY" : "%E5%8C%97%E4%BA%AC",
        "tt_webid" : "1",
        "csrftoken" : "1",
        "tasessionId" : "1",
    }
    sess=requests.session()
    for k,v in cookies_dic.items():
        sess.cookies.set(k,v)
    try:
        response=sess.get(url,headers=headers,verify=False)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        raise Exception("请求失败了")
def parse_main_page(html):
    html=json.loads(html)
    print(html)
    if html and "data" in html.keys():
        for data in html["data"]:
            if "article_url" in data.keys():
                yield  data["article_url"]
    else:
        raise Exception("json 数据没有data")

def main():
    html=get_main_page(0, "街拍")
    for url in parse_main_page(html):
        print(url)

if __name__ == '__main__':
    main()