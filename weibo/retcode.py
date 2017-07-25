import requests
import base64


def get_retcode(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    f.close()
    encrypted_data = base64.b64encode(data)
    appkey = '51388e6214aed10d'
    base_url = 'http://api.jisuapi.com/captcha/recognize'
    url = base_url + '?appkey=' + appkey
    param = {
        'pic': encrypted_data,
        'type': 'en',
    }
    response = requests.post(url, data=param)
    json = response.json()
    print json
    code = json['result']['code']
    print code
    return code


# if __name__ == '__main__':
#     get_retcode("../cha.jpg")