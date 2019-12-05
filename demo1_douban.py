# 豆瓣读书首页信息提取
import re,requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}
req=requests.get("https://book.douban.com",headers=headers)
text=req.text
pattern=re.compile('li.*?title="(.*?)".*?author">(.*?)<.*?year">(.*?)<.*?abstract">(.*?)<',re.S)
messages=re.findall(pattern,text)
for message in messages:
    title,author,publishyear,abstract=message
    author=re.sub("\s","",author)
    publishyear=re.sub("\s","",publishyear)
    abstract=re.sub("\s","",abstract)
    print(title,author,publishyear,abstract,end="\n")
