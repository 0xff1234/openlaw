# openlaw.cn网站爬虫

第一次写py，边学边写了这个从openlaw爬取文书内容保存为txt文件的小内容。

因为openlaw做了防护，所以使用selenium模拟浏览器访问。

#### TXT文档说明

- **account.txt** 记录当前使用哪个账户登录openlaw
- **account/account.txt** 记录所有的openlaw Account，因为openlaw的每个账户每天访问次数限制，所以需要多个账户
- **account/Y-m-d.txt** 记录某一天哪些账户已经不可以再次访问
- **cookie.txt** 记录登陆之后的coojie
- **count.txt** 记录已经下载的文书数量
- **page.txt** 记录爬到了哪一页
- **ids.txt** 记录每一页爬取下来的文书id

#### spiderUrl.py

spiderUrl.py分页爬取文书的id，openlaw每一篇文书都有一个唯一的浏览id

- spiderUrl.get_url()可配置具体的搜索条件，参考openlaw的搜索url设置。
- spiderUrl.get_download_ids()每三秒执行一次，执行前判断ids是否为空空文件则爬取下一页的文书id，否则pass

#### download.py

根据文书的唯一浏览id，下载文书内容到txt文件，所有下载的文件位于judgements文件夹下

- download.save_content(content_map, id) 可以配置文件保存位置

- 每次从ids.txt文件中读取完ids会将ids.txt置空，让spiderUrl爬取下一页的ids

- download.download()函数将页面的内容处理为一个BeautifulSoup穿个get_content()函数处理页面内容。

- download.get_content(soup) 讲页面内容进行处理返回


  ```
 {
  'content': content,# 文书内容
  'title': title, # 文书标题
  'header': header # 文书的时间等一些说明
 }
  ```


- download.save_content(content_map, id) 将get_content()返回的内容写进文档

#### config.py

爬虫的共享txt文件的读，和打开浏览器，登录，更换账号函数写在这个文件内。

登录的密码为同一的密码

#### start.py

开启两个线程，一个让spiderUrl爬取文书ids，一个让download下载文书，两个互不干扰，提高效率。

#### 问题

判断登录失效以及读写共享文件时没有做线程保护