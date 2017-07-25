import Queue

import requests

USER_AGENTS = {

}

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests':'1',
           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
           }

URL_QUEUE = Queue.Queue()

URL_NUMBER = 0


ACCOUNTS = [
    {
        "username": "**********",
        "password": "*******"
    },
]

