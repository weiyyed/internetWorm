# 禅道脚本生成
import re
import time
import requests
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chandao_url="8"
while chandao_url=="":
    chandao_url = input("input chandao url or project id:")
try:
    int(chandao_url)
    chandao_url="http://chandao.ushayden.com/zentao/bug-browse-{}-0-unresolved.html".format(chandao_url)
except:
    pass
option = Options()
option.add_argument("--headless")
option.add_argument("--disable-gpu")
driver = webdriver.Chrome(chrome_options=option)
driver.get(chandao_url)
driver.find_element_by_id("account").send_keys("weiyongyou")
driver.find_element_by_name("password").send_keys("a123456")
driver.find_element_by_id('submit').click()
time.sleep(1)
cookies = driver.get_cookies()

sess = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}
sess.headers.update(headers)
for cookie in cookies:
    sess.cookies.set(cookie["name"], cookie["value"])
driver.quit()

pattern="(http.*?-\d+)"
chandao_url=re.search(pattern,chandao_url).group(1)+"-0-unresolved-0--1048-1000-1.html"
text=sess.get(chandao_url).text

bf=BeautifulSoup(text,"lxml")
ids=bf.select('tr td.c-id.cell-id a')
titles=bf.select('tr td.c-title.text-left a')
deal_person=bf.select('td.c-assignedTo.has-btn.text-left span')
# ids=bf.select("tr td.c-id.cell-id")
deal_dic={}
total=0
for x in range(len(ids)):
    if deal_person[x].text in deal_dic:
        deal_dic[deal_person[x].text].append((ids[x].text,titles[x].text))
        total+=1
        continue
    deal_dic[deal_person[x].text]=[(ids[x].text,titles[x].text)]
    total+=1
with open("./unresolved.txt","w+",encoding="utf-8") as f:
    f.write("目前待处理问题{}个，请当前处理人尽快处理解决。\n".format(total))
    for p,vs in deal_dic.items():
        f.write("@{}\n".format(p))
        for n in range(len(vs)):
            f.write("{}:{}".format(vs[n][0],vs[n][1]))
            f.write("\n")
        f.write("\n")
