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
        "username": "17187306796",
        "password": "gf754963"
    },
    {
        "username": "17096445090",
        "password": "ms332508"
    },
    {
        "username": "17187306702",
        "password": "ms329164"
    },
    {
        "username": "17096444714",
        "password": "ms326291"
    },
    {
        "username": "17000569876",
        "password": "ms323034"
    },
    {
        "username": "17075306916",
        "password": "ms321361"
    },
    {
        "username": "15174975680",
        "password": "ms320424"
    },
    {
         "username": "17187306774",
         "password": "ms315900"
    },
    {
        "username": "17133143407",
        "password": "ms315217"
    },
    # {
    #     "username": "15648572606",
    #     "password": "ms332043"
    # },
    {
        "username": "17000569301",
        "password": "ms1234567"
    },
]

