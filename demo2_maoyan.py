# 爬取猫眼电影中排名前100名电影信息
import json
import re
import requests
from requests.exceptions import RequestException
from  multiprocessing import Pool
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Connection': 'keep-alive',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    # try:
    response=requests.get(url,headers=headers,verify=False)
    if response.status_code==200:
        return response.text
    return None
    # except RequestException:
    #     return None
def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(.*?)</i.*?title="(.*?)".*?data-src="(.*?)".*?score.*?integer">(.*?)</i.*?fraction">(.*?)</i',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            "index":item[0],
            "name":item[1],
            "image":item[2],
            "score":item[3]+item[4]
        }
def save_to_file(content):
    with open("films.txt","a",encoding="utf-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+"\n")
def main(offset):
    url="https://maoyan.com/board/4?offset="+str(offset)
    html=get_one_page(url)
    for itme in parse_one_page(html):
        save_to_file(itme)
if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])