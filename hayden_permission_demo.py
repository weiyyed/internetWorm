# 一键生成菜单功能按钮
import datetime,json,re,time,requests,os
from json import JSONDecodeError
from selenium import webdriver
from urllib.parse import urlencode
from config import hayden_conf
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def get_html_source(url,session):
    if isinstance(session,requests.sessions.Session):
        req=session.get(url)
        if req.status_code==200:
            return req.text
        else:
            raise Exception("请求失败{}".format(req.status_code))
def parse_html(data):
    data_change=None
    try:
        data_change=json.loads(data)
    except JSONDecodeError:
        print("数据不是json",data)
    if data_change and "data" in data_change.keys():
        items=data_change.get("data")
        merge={}
        for item in items:
            merge[item["codepath"]] = [item["name"]]
    else:
        raise Exception("解析data数据失败")
    order_dic = sorted(merge.items(), key=lambda x: x[0])
    return order_dic
def generate_session(url,name,password,module="sy"):
    option=Options()
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    driver=webdriver.Chrome(chrome_options=option)
    driver.get(url)
    if int(hayden_conf.LOGIN_TYPE)==1:
        driver.find_element_by_id("name").send_keys(name)
        driver.find_element_by_id("pwd1").send_keys(password)
        driver.find_element_by_xpath(r'//a[@onclick="login()"]').click()
    elif int(hayden_conf.LOGIN_TYPE)==2:
        driver.find_element_by_id("username").send_keys(name)
        driver.find_element_by_id("pwd1").send_keys(password)
        driver.find_element_by_css_selector(r'input[value="立即登录"]').click()
    time.sleep(1)
    wait=WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/script")))

    if module=="sy":
        driver.get(url+"#eyJtYyI6InN5IiwiZmMiOiJTWV9QRVJNSVNTT05fUEMiLCJ1YyI6IjAxNzAwMDQ1MDAxMCJ9")
    time.sleep(1)
    html_source=driver.page_source
    csrf=re.search("window.csrf = '(.*?)'",html_source).group(1)
    cookies=driver.get_cookies()
    driver.close()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    sess=requests.session()
    sess.headers.update(headers)
    for cookie in cookies:
        sess.cookies.set(cookie["name"],cookie["value"])
    sess.headers.update({"csrf":csrf})
    return sess
def save_to_file(parse_data_dic,menu="pc"):
    if not os.path.exists("./file"):
        os.mkdir("./file")
    with open("file/{0}_{1}_{2}_{3}.txt".format(menu,hayden_conf.DOMAIN[7:].split("/")[0].split(":")[0],hayden_conf.USERNAME,datetime.date.today()),"w",encoding="utf-8") as f:
        for d in parse_data_dic:
            k,v=d
            k1=str(k).split("#",1)[-1]
            if len(str(k).split("#",1))==1:
                f.write("\n")
            f.write(k1 + ":" + str(v) + "\n")
def main():
    params={
        "clientType": 0,
        "contentType": "json",
        "ajax": "true",
    }
    url=hayden_conf.DOMAIN+"/sy/SY_PERMISSON_PC/getPermissionTree?"+urlencode(params)
    user=hayden_conf.USERNAME
    pwd=hayden_conf.PASSWORD
    req_session=generate_session(hayden_conf.DOMAIN,user,pwd)
    # PC端
    source=get_html_source(url,req_session)
    save_to_file(parse_html(source),menu="pc")
    # 移动端
    url_mobile = hayden_conf.DOMAIN + "/sy/SY_PERMISSION_M/getPermissionTree?"+ urlencode(params)
    source_mobile = get_html_source(url_mobile, req_session)
    save_to_file(parse_html(source_mobile),menu="m")
if __name__ == '__main__':
    main()