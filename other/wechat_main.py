
from wxpy import *
from requests import request
import json
import os

cur_dir=os.path.split(os.path.realpath(__file__))[0]
filename = cur_dir.split('/')[-1]

url_api_base = "http://localhost:9601/api/paycall/wechat_callback"
url_api_base_login = "http://localhost:9601/api/paycall/wechat_login"
url_api_base_logout = "http://localhost:9601/api/paycall/wechat_logout"

def send_request(url, headers={}, method='get', params=None, data=None):
    try:
        print(data)
        result = request(method, url, headers=headers, params=params, json=data, verify=False)
        status_code = result.status_code
        result = result.json()
        print(result)
        if result.get('rescode') == '10000':
            return True, result.get('data')
        return "1", result.get('msg')
    except Exception as ex:
        return "2", '{0}'.format(ex)

def qr_handler(uuid,status,qrcode):
    with open('/var/nginx_upload/wechatlogin/{}.png'.format(filename),'wb') as f:
        f.write(qrcode)

def login_callback():

    res = send_request(
        url=url_api_base_login,
        method='POST',
        data={"data": {"msg":filename}})
    if res[0] == '1' or res[0] == '2':
        count = 3
        while count:
            res=send_request(
                url=url_api_base_login,
                method='POST',
                data={"data": {"msg": filename}})
            print("next:",res)
            if res[0] == True:
                break
            count -=1

def logout_callback():
    res = send_request(
        url=url_api_base_logout,
        method='POST',
        data={"data": {"msg":filename}})
    if res[0] == '1' or res[0] == '2':
        count = 3
        while count:
            res=send_request(
                url=url_api_base_logout,
                method='POST',
                data={"data": {"msg": filename}})
            print("next:",res)
            if res[0] == True:
                break
            count -=1


bot = Bot(cache_path='{}/wxpy.pkl'.format(cur_dir),console_qr=2,qr_callback=qr_handler, \
		login_callback=login_callback,logout_callback=logout_callback)

mp = ensure_one(bot.search('微信收款助手'))

@bot.register(msg_types=TEXT,run_async=True)
def just_print(msg):
    print(msg)

@bot.register(chats=mp,msg_types=SHARING,run_async=True)
def just_print(msg):

    print(msg)
    res = send_request(
        url=url_api_base,
        method='POST',
        data={"data": {"msg":msg.raw['Content']}})
    if res[0] == '1' or res[0] == '2':
        count = 3
        while count:
            res=send_request(
                url=url_api_base,
                method='POST',
                data={"data": {"msg":msg.raw['Content']}})
            print("next:",res)
            if res[0] == True:
                break
            count -=1

# 开始运行
bot.join()
