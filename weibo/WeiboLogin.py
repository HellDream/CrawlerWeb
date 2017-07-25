# -*- coding: utf-8 -*-

import base64
import random
import urllib2

import binascii

import re
import rsa
import time
import requests
import sys

from crawlersettings import ACCOUNTS
from retcode import get_retcode
from CrawlerWeb.settings import BASE_DIR
# from PIL import Image
# import json
reload(sys)
sys.setdefaultencoding("utf-8")
session = requests.session()
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',

}


index_url = "http://weibo.com/login.php"
try:
    session.get(index_url, headers=headers, timeout=2)
except:
    session.get(index_url, headers=headers)


class WeiboLogin:
    def __init__(self, username, password, session):
        self.username = username
        self.password = password
        print username
        print password
        self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
        self.session = session

    def get_encrypted_name(self):
        username_quote = urllib2.quote(self.username)
        username_encrypted = base64.b64encode(username_quote.encode("utf-8"))
        return username_encrypted.decode('utf-8')

    def get_password(self, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password)  # 拼接明文js加密文件中得到
        message = message.encode("utf-8")
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    def get_pre_login_args(self, su):
        pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
        pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
        pre_url = pre_url + str(int(time.time() * 1000))
        pre_data_res = self.session.get(pre_url, headers=headers)

        sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))
        return sever_data

    def get_cha(self, pcid):
        cha_url = "http://login.sina.com.cn/cgi/pin.php?r="
        cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
        cha_url = cha_url + pcid
        cha_page = self.session.get(cha_url, headers=headers)
        path = BASE_DIR + "/cha.jpg"
        print path
        with open(path, 'wb') as f:
            f.write(cha_page.content)
        f.close()
        # try:
        #     im = Image.open("cha.jpg")
        #     im.show()
        #     im.close()
        # except:
        #     print(u"请到当前目录下，找到验证码后输入")

    def login(self):
        su = self.get_encrypted_name()
        sever_data = self.get_pre_login_args(su)
        servertime = sever_data["servertime"]
        nonce = sever_data['nonce']
        rsakv = sever_data["rsakv"]
        pubkey = sever_data["pubkey"]
        password_secret = self.get_password(servertime, nonce, pubkey)
        try:
            showpin = sever_data["showpin"]
        except:
            showpin = 0
        postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': password_secret,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        if showpin == 0:
            login_page = self.session.post(self.login_url, data=postdata, headers=headers)
        else:
            pcid = sever_data["pcid"]
            self.get_cha(pcid)
            time.sleep(1)
            path = BASE_DIR + "/cha.jpg"
            code = get_retcode(path)
            postdata['door'] = code
            login_page = self.session.post(self.login_url, data=postdata, headers=headers)
        login_loop = (login_page.content.decode("GBK"))
        pa = r'location\.replace\([\'"](.*?)[\'"]\)'
        loop_url = re.findall(pa, login_loop)[0]
        # print(loop_url)
        # 此出还可以加上一个是否登录成功的判断，下次改进的时候写上
        login_index = self.session.get(loop_url, headers=headers)
        uuid = login_index.text
        print uuid
        uuid_pa = r'"uniqueid":"(.*?)"'
        try:
            uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
            web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
            weibo_page = self.session.get(web_weibo_url, headers=headers)
            weibo_pa = r'<title>(.*?)</title>'
            # print(weibo_page.content.decode("utf-8"))
            userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
            print(u"欢迎你 %s" % userID)
        except:
            account = random.choice(ACCOUNTS)
            self.username = account['username']
            self.password = account['password']
            self.login()


# if __name__ == '__main__':
#     login_obj = WeiboLogin("17187306796", "gf754963", session)
#     login_obj.login()