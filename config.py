#encoding:utf-8
import time
import os
import sys
# from pyvirtualdisplay import Display
from selenium import webdriver


def echo_time():
    return "[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "]"


def open_browser():
    # display = Display(visible=0, size=(800,600))
    # display.start()
    browser = webdriver.Firefox(executable_path=os.path.dirname(sys.path[0]) + "/etc/geckodriver")
    login = 'window.open("http://openlaw.cn/login.jsp");'
    search = 'window.open("http://openlaw.cn/search/judgement/advanced?showResults=true&' \
             'lawId=40eed8f94dca43a6b938331d255ccd6a&page=1");'
    browser.get('http://openlaw.cn/judgement/')
    browser.execute_script(login)
    browser.execute_script(search)
    # browser.window_handles[0] download
    # browser.window_handles[1] login
    # browser.window_handles[2] search
    return browser


def login(browser):
    browser.switch_to.window(browser.window_handles[1])
    browser.get("http://openlaw.cn/login.jsp")
    browser.find_element_by_id("j_username").send_keys(get_account())
    browser.find_element_by_id("j_password").send_keys("wakakakaka")
    browser.find_element_by_id("validateCode").send_keys("ha2ha")
    browser.find_element_by_id("submit").click()
    time.sleep(3)
    cookies = browser.get_cookies()
    f = open(sys.path[0] + '/cookie.txt', 'w')
    for cookie in cookies:
        f.write(cookie.get("name") + "," +cookie.get("value") + ",\n")
    f.close()


def get_cookies():
    result = []
    f = file(sys.path[0] + '/cookie.txt', 'r')
    for line in f.readlines():
        result.append(map(str, line.split(',')))
    f.close()
    return result


def get_ids():
    result = []
    f = file(sys.path[0] + '/ids.txt', 'r')
    for line in f.readlines():
        result.append(map(str, line.split(',')))
    f.close()
    return result


def change_account():
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    used_filename = sys.path[0] + '/account/' + today + '.txt'
    if os.path.exists(used_filename):
        used = open(used_filename, 'r+')
    else:
        used = open(used_filename, 'w+')
    used_account = used.readlines()

    f = open(sys.path[0] + '/account/account.txt', 'r')
    lines = f.readlines()
    use = open(sys.path[0] + '/account.txt', 'w+')
    for line in lines:
        if line + '\n' in used_account:
            continue
        else:
            use.write(line)
            used.write(line + '\n')
            return line
    use.close()
    f.close()
    used.close()
    return


def get_account():
    f = open(sys.path[0] + '/account.txt', 'r')
    lines = f.readlines()
    if len(lines) == 0:
        # 改变账户确定没有可执行账户
        change_account()
        lines = f.readlines()
        if len(lines) == 0:
            f.close()
            os._exit(0)
    else:
        f.close()
        return lines[0]
