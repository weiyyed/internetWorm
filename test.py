import collections

import requests,selenium,redis,socket
# from selenium import webdriver
from bs4 import BeautifulSoup
# from pyquery import PyQuery as pq
import  socket,urllib.request,urllib.error

def fun():
    for i in range(5):
        yield{
            x:i,
            y:i+1
        }
if __name__=="__main__":
    d1 = collections.OrderedDict()
    d1['a'] = 'A'
    d1['c'] = 'C'
    d1['b'] = 'B'
    d1['1'] = '1'
    d1['2'] = '2'
    for k, v in d1.items():
        print(k, v)