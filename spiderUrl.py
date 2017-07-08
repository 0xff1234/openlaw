#coding=utf-8
import re
import sys
import config
import time


def get_url():
    page_number = record()
    return 'http://openlaw.cn/search/judgement/advanced?showResults=true&lawId=40eed8f94dca43a6b938331d255ccd6a&page='\
           + str(page_number)


def get_download_ids(browser):
    browser.switch_to.window(browser.window_handles[2])
    browser.delete_all_cookies()
    cookies = config.get_cookies()
    if len(cookies) < 4:
        config.login(browser)
        return
    for cookie in cookies:
        browser.add_cookie({
            'name': cookie[0],
            'value': cookie[1]
        })
    url = get_url()
    browser.get(url)
    content = browser.page_source
    if u'你今天的访问超出正常用户的最大访问限制！' in content:
        config.change_account()
        # 清理cookie，下次换账号登录
        f = open(sys.path[0] + '/cookie.txt', 'w')
        f.close()
    print config.echo_time() + " get download urls success: " + url + "\n"
    # print content
    p = re.compile(r'((?<=("/judgement/))[a-zA-Z0-9]+(?=(")))')
    result = p.findall(content)
    if len(result) == 0:
        config.login(browser)
        return
    f = open(sys.path[0] + '/ids.txt', 'w')
    for id in result:
        f.write(id[0] + ",\n")
    f.close()


def record():
    f = open(sys.path[0] + '/page.txt', 'r')
    page_number = int(f.read())
    f.close()
    f = open(sys.path[0] + '/page.txt', 'w')
    f.write(str(page_number + 1))
    f.close()
    return page_number


def start(browser):
    while True:
        time.sleep(3)
        if len(config.get_ids()) == 0:
            get_download_ids(browser)


