#encoding:utf-8
import config
import download
import thread
import spiderUrl
import time

browser1 = config.open_browser()
browser2 = config.open_browser()
time.sleep(3)
thread.start_new_thread(spiderUrl.start, (browser1,))
time.sleep(3)
thread.start_new_thread(download.start, (browser2,))
while True:
    pass
