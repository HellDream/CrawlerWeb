# -*- coding: utf-8 -*-

from CrawlerWeb.celery import app
from weibo.weiboCrawler2 import WeiboCrawler


@app.task
def hello_world():
    print('Hello World')


@app.task
def do_crawler(keyword, username, password):
    crawler = WeiboCrawler(keyword=keyword, username=username, password=password)
    crawler.search()