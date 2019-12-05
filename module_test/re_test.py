import re
# 正则字符串编译成对象，便于重复使用
content = """extra hello 1234567 this is a demo,hello 12347 world_this is  demo"""
pattern="he.*?(\d+).*?demo"
result=re.findall(pattern,content)
