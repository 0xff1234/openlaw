#coding=utf-8
import sys
import re
import codecs
import os
from bs4 import BeautifulSoup
import spiderUrl
import config


def download(browser):
    browser.switch_to.window(browser.window_handles[0])
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
    ids = config.get_ids()
    f = open(sys.path[0] + '/ids.txt', 'w')
    f.close()
    if len(ids) == 0:
        spiderUrl.get_download_ids(browser)
        return
    for id in ids:
        browser.get(document_url(id[0]))
        #print driver.page_source
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        content = get_content(soup)
        save_content(content, id[0])
        print config.echo_time() + " download " + id[0] + " success \n"


def document_url(name):
    return 'http://openlaw.cn/judgement/' + name


def record_count():
    f = open(sys.path[0] + '/count.txt', 'r')
    count = int(f.read()) + 1
    f.close()
    f = open(sys.path[0] + '/count.txt', 'w')
    f.write(str(count))
    f.close()


def get_content(soup):
    content = soup.select('#entry-cont')
    if len(content) == 0:
        return
    content = content[0].get_text()
    p = re.compile(r'((?<=())[\w\W]*?(?=(允许所有人查看该批注允许所有人编辑该批注)))')
    result = p.findall(content.encode('utf-8'))
    if len(result) == 0:
        return
    if len(result[0]) == 0:
        return
    content = unicode(result[0][0], "utf-8")
    title = soup.select('h2[class=="entry-title"]')[0].get_text()
    header = soup.select('article > header')[0].get_text()
    return {
        'content': content,
        'title': title,
        'header': header
    }


def save_content(content_map, id):
    if content_map is None:
        return
    file_path = sys.path[0] + '/judgements/' + id + '.txt'
    if os.path.exists(file_path):
        return
    f = codecs.open(file_path, 'w', 'utf-8')
    f.write(content_map.get('header'))
    f.write(content_map.get('content'))
    f.close()
    # 记录条数
    record_count()


def start(browser):
    while True:
        download(browser)
