from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium  import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
driver = webdriver.Chrome()
driver.maximize_window() #最大化窗口
try:
    driver.get("https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable")
    driver.execute_script("window.open()") #调用js新增选项卡
    handles=driver.window_handles  #获取窗口句柄
    driver.switch_to.window(handles[1])
    driver.get("http://www.baidu.com")
    driver.switch_to.window(handles[0]) #切换窗口
finally:
    # 注意：close方法只会关闭一个选项卡，浏览器不会被关闭。如果是quit则会把2个选项卡都关闭
    driver.close()
    driver.quit()