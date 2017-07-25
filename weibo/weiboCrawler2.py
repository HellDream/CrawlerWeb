# -*- coding: utf-8 -*-
import random
import time
from urllib import quote
from bs4 import BeautifulSoup
import requests
from WeiboLogin import WeiboLogin
from crawlersettings import headers, ACCOUNTS, URL_QUEUE
import sys
import threading
import Queue
from .models import Key, Weibo
reload(sys)
sys.setdefaultencoding("utf-8")

headers = headers
session = requests.session()
# DATA = []
URL_PAGE = Queue.Queue()
key_object = None


class CrawlerThread(threading.Thread):
    def __init__(self):
        super(CrawlerThread, self).__init__()

    def run(self):
        # global DATA
        global URL_PAGE
        global key_object
        if URL_QUEUE.qsize() == 0:
            self.is_alive = False
        search_url = URL_QUEUE.get()
        print "Downloading:{0}".format(search_url)
        html = URL_PAGE.get()
        soup = BeautifulSoup(html, 'lxml')
        print search_url
        item_list = soup.find_all("div", class_="card item_weibo")
        for item in item_list:
            try:
                username_ = item.find("p", class_="tit_m").get_text()
                timestamp = item.find("p", class_="time").find("span").get_text()
                contents = item.find_all("div", class_="blk5")
                content = contents[1].find_next().get_text()
                try:
                    location = item.find("span", class_="lbs").get_text()
                except:
                    location = None
                weibo_item = Weibo.objects.create(key=key_object,
                                                  username=username_,
                                                  content=content,
                                                  location=location,
                                                  timestamp=timestamp)
                weibo_item.save()
                # DATA.append(data_item)
            except:
                continue
        # print len(DATA)



class WeiboCrawler:

    def __init__(self, keyword, username=None, password=None):
        global headers
        global session
        global key_object
        account = random.choice(ACCOUNTS)
        if username is None or password is None:
            self.username = account["username"]
            self.password = account["password"]
        else:
            self.username = username
            self.password = password
        self.base_url = 'http://s.weibo.com/'
        self.keyword = keyword
        self.session = session
        weibo_login = WeiboLogin(self.username, self.password, self.session)
        weibo_login.login()
        key = Key.objects.create(keyword=keyword)
        key.save()
        key_object = key

    def get_url(self, page_number):
        keyword_ = quote(str(self.keyword))
        url = "{0}weibo/{1}&nodup=1&page={2}".format(self.base_url, keyword_, page_number)
        return url

    def download_url(self):
        global headers
        global URL_PAGE
        next_page = True
        page_num = 1
        search_url = self.base_url + "weibo/" + quote(str(self.keyword)) + "&nodup=1"
        html = self.session.get(search_url, headers=headers).text
        while next_page:
            print "_______________________________________________________________________"
            soup = BeautifulSoup(html, 'lxml')
            print search_url
            item_list = soup.find_all("div", class_="card item_weibo")
            if not item_list:
                print item_list
                next_page = False
                break
            URL_QUEUE.put(search_url)
            URL_PAGE.put(html)
            page_num += 1
            # time.sleep(1)
            search_url = self.get_url(page_num)
            html = self.session.get(search_url, headers=headers).text

    def search(self):
        global session
        session = self.session
        threadpoor = []
        self.download_url()
        while URL_PAGE.qsize() > 0:
            while len(threadpoor) < 5:
                thread = CrawlerThread()
                threadpoor.append(thread)
                thread.start()
                if URL_PAGE.qsize() < 5 - len(threadpoor):
                    break
            # 线程结束时将其从线程池中删除
            for thread in threadpoor:
                if not thread.is_alive:
                    threadpoor.remove(thread)
    # def search(self):
    #     global headers
    #     next_page = True
    #     page_num = 1
    #     data = []
    #     search_url = self.base_url + "weibo/" + quote(self.keyword) + "&nodup=1"
    #     html = self.session.get(search_url, headers=headers).text
    #     # print htmlms332508
    #     while next_page:
    #         print "_______________________________________________________________________"
    #         soup = BeautifulSoup(html, 'lxml')
    #         print search_url
    #         item_list = soup.find_all("div", class_="card item_weibo")
    #         print item_list
    #         if not item_list:
    #             next_page = False
    #             break
    #         filename = self.keyword + str(page_num) + ".html"
    #         with open(filename, 'w') as f:
    #             f.write(html)
    #         f.close()
    #         for item in item_list:
    #             try:
    #                 username_ = item.find("p", class_="tit_m").get_text()
    #                 timestamp = item.find("p", class_="time").find("span").get_text()
    #                 contents = item.find_all("div", class_="blk5")
    #                 content = contents[1].find_next().get_text()
    #                 try:
    #                     location = item.find("span", class_="lbs").get_text()
    #                 except:
    #                     location = None
    #
    #                 data_item = {
    #                     'username': username_,
    #                     'timestamp': timestamp,
    #                     'content': content,
    #                     'location': location,
    #                 }
    #                 print data_item
    #                 data.append(data_item)
    #             except:
    #                 continue
    #         page_num += 1
    #         time.sleep(1)
    #         search_url = self.get_url(page_num)
    #         html = self.session.get(search_url, headers=headers).text
    #     print len(data)


# if __name__ =="__main__":
#     keyword = "广州"
#     w = WeiboCrawler(keyword=keyword)
#     w.search()
