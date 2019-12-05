from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup = BeautifulSoup(html_doc,"lxml")
# 查找所有p标签
ps=soup.find_all('p')
# 查询标签的属性
for p in ps:
    # 获取属性
    print(p["class"])
    #嵌套，提取下级标签
    print(p.b)
# prettify方法：格式行html，缺少的tag会自动补全
print(soup.prettify())
