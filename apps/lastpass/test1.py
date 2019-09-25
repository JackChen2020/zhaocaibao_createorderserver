

from requests import request
import json
from urllib.parse import urlencode
from collections import OrderedDict
import hashlib
from libs.utils.mytime import UtilTime
import time,random
import demjson
import os

import base64
# from Cryptodome.PublicKey import RSA
# from Cryptodome.Hash import SHA1
# from Cryptodome.Signature import pkcs1_15
from Crypto.Cipher import AES
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA

from binascii import b2a_hex, a2b_hex

class LastPassBase(object):

    def __init__(self,**kwargs):
        self.secret = kwargs.get('secret')
        self.data = kwargs.get('data',{})

    def _sign(self):
        pass

class LastPass_BAOYANGHUI(LastPassBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.appId = "rogerxpp"
        self.appSecret = 'rogerxpp'
        self.token = None
        self.goods = None

        self.server = "http://www.baoyanghui.com/Car_2_0"

    def run_api(self,func):
        try:
            res = func()
            return (False, res['msg']) if str(res['code'])!='0' else (True,res['resultData']['accessToken'])
        except Exception as e:
            return (False,str(e))

    def get_token(self):

        try:
            api_server = "/api/open/token"
            result = request(method='GET', url=self.server+api_server,params={
                "appId" : self.appId,
                "appSecret" : self.appSecret
            })
            res = json.loads(result.content.decode('utf-8'))
            return (False, res['msg']) if str(res['code']) != '0' else (True, res['resultData']['accessToken'])
        except Exception as e:
            return (False, str(e))


    def get_goodsList(self):

        try:
            api_server = "/api/open/merchantPlace/list"
            result = request(method='GET', url=self.server+api_server,params={
                "accessToken": self.token
            })
            res = json.loads(result.content.decode('utf-8'))
            print(res)
            return (False, res['msg']) if str(res['code']) != '0' else (True, res['resultData'])
        except Exception as e:
            return (False, str(e))

    def run(self):


        res = self.get_token()
        if not res[0]:
            return res
        else:
            self.token = res[1]

        res = self.get_goodsList()
        if not res[0]:
            return res
        else:
            self.goods = res[1]

        print(self.goods)



if __name__=='__main__':

    res = LastPass_BAOYANGHUI().run()
    print(res)