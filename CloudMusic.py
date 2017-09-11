import time,logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)
    return driver

def login_qq(driver, login_page, username, password):
    driver.get(login_page)
    iframe = driver.find_element_by_xpath("//iframe[@id]")
    driver.switch_to.frame(iframe)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "switcher_plogin"))
        )
    except Exception as e:
        logging.exception(e)
        pass
    driver.find_element_by_id("switcher_plogin").click()  # 切换到qq登录输入框
    # 用户名
    username_input = driver.find_element_by_id("u")
    username_input.clear()
    username_input.send_keys(username)
    # 密码
    password_input = driver.find_element_by_id("p")
    password_input.clear()
    password_input.send_keys(password)
    before_url = driver.current_url  # 记录地址栏url
    # 点击登录
    driver.find_element_by_id("login_button").click()
    time.sleep(2)
    if driver.current_url == before_url:  # 如果url没有改变,则判定登录失败
        # 登录不成功
        print("登录失败,正在重试")
        login_qq(driver, login_page,username,password)
    return "seccess"

def like_music(driver,music_page):
    driver.get(music_page)
    driver.switch_to.frame('g_iframe')
    time.sleep(2)
    while True:
        comments = driver.find_element_by_id('comment-box').find_elements_by_css_selector('.itm') #获取所有评论item元素
        for item in comments:
            try:
                target = driver.find_element_by_xpath('//a[@data-type="like"]') #筛选出未点赞的元素
                driver.execute_script("arguments[0].scrollIntoView();", target)  #拖动到可见的元素处
                target.click() #点赞
                time.sleep(0.4)
            except Exception as e:
                logging.exception(e)
                pass
        next_btn=driver.find_element_by_link_text("下一页") # 评论翻页
        if "disable" in next_btn.get_attribute("class"): #判断class属性中是否包含disabled字段
            print("点赞完毕")
            break
        next_btn.click()
        time.sleep(1)
    return "over"

login_page="https://graph.qq.com/oauth/show?which=Login&display=pc&client_id=100495085&response_type=code&redirect_uri=https://music.163.com/back/qq&forcelogin=true&state=ZwKHpxUoam"
driver = get_driver()
try:
    login_qq(driver, login_page, "qq_username", "qq_password") #登录
except Exception as e:
    logging.exception(e)
    pass
driver.refresh()
music_page="http://music.163.com/#/song?id=32358440"
like_music(driver,music_page) #点赞
