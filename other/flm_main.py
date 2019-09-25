import hashlib
import json
import requests
import time
from requests import request
import redis
from concurrent.futures import ThreadPoolExecutor


# def send_request(url, headers={}, method='get', params=None, data=None):
#     try:
#         result = request(method, url, headers=headers, params=params, json=data, verify=False)
#         status_code = result.status_code
#         result = result.json()
#         if result.get('rescode') == '10000':
#             return True, result.get('data')
#         return "1", result.get('msg')
#     except Exception as ex:
#         return "2", '{0}'.format(ex)

# class FmlCallbackManys(object):
#
#
#     def __init__(self ,time_wait=3, callback=None):
#
#         """
#         付临门聚合码支付获取交易数据
#         :param mobiles: 登录账号集合
#         :param time_wait: 监控等待秒数
#         :param callback: 回调函数处理
#         """
#
#         redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=4, password="plokiqikj##mlad,..ad")
#         self.redis_pool = redis.StrictRedis(connection_pool=redis_pool)
#         self.redis_key = "flm_mobiles"
#
#         self.executor = ThreadPoolExecutor(max_workers=8)
#
#         self.mobiles = {}
#         # self.password = hashlib.md5((password + 'superpw1234_!QAZ').encode('utf-8')).hexdigest()
#
#         self.login_url = 'https://smzf.yjpal.com/payQRCode/loginCheck.htm'
#         self.tranlist_url = 'https://smzf.yjpal.com/payQRCode/newQrcodeTransjnlsList.htm'
#
#         self.time_wait = time_wait
#         self.callback = callback
#
#         self.token = None
#         self.tranlist_obj = None
#
#
#     def redis_dict_insert(self,value):
#         self.redis_pool.set(self.redis_key,json.dumps(value))
#
#     def redis_dict_get(self):
#         res = self.redis_pool.get(self.redis_key)
#         return json.loads(res) if res else res
#
#
#     def _login(self,mobile,password):
#         try:
#             response = requests.post(url=self.login_url, data={
#                 "mobileNo" : mobile,
#                 "password" : hashlib.md5((password + 'superpw1234_!QAZ').encode('utf-8')).hexdigest()
#             })
#             response = json.loads(response.content.decode('utf-8'))
#
#             self.mobiles[mobile]['token'] = response['token']
#
#             return response['code']
#         except Exception :
#             return None
#
#     def tranlist(self,mobile,time):
#         try:
#             headers = {
#                 "AccessToken" : self.mobiles[mobile]['token']
#             }
#             response = requests.post(url=self.tranlist_url, headers=headers , data={
#                 "mobileNo" : mobile,
#                 "pageNo" : 0,
#                 "time" : time
#             })
#             self.mobiles[mobile]['tranlist']=json.loads(response.content.decode('utf-8'))
#         except Exception :
#             return None
#
#     def handler_tranlist(self):
#         """
#         获取付临门交易明细
#         :return:
#         """
#
#         for item in self.mobiles:
#             self.mobiles[item]['tranlist'] = None
#             count = 3
#             while self.tranlist(item,201905) != '0000':
#                 self._login(item,self.mobiles[item]['password'])
#                 count -=1
#                 if not count:
#                     break
#
#     def request_data(self):
#         try:
#             res = requests.get(url='http://localhost:9601/api/paycall/flm_tranlist_get?data={"page":1,"page_size":9999999}')
#             return json.loads(res.content.decode('utf-8'))['data']
#         except Exception as e:
#             print(str(e))
#             return None
#
#     def run(self):
#
#         while True:
#             res = self.redis_dict_get()
#             while not res or not res.get('data',None) or not len(res.get('data',None)):
#                 res = self.redis_dict_get()
#
#             tmp_mobiles = res.get('data',None)
#             new_mobiles = {}
#             for item in tmp_mobiles:
#                 if item not in self.mobiles:
#                     new_mobiles[item] = tmp_mobiles[item]
#
#             error_mobile = []
#             for mobile in new_mobiles:
#                 count = 3
#                 while self._login(mobile,new_mobiles[mobile]['password']) != '0000':
#                     count -= 1
#                     if not count:
#                         error_mobile.append(mobile)
#                         break
#
#             if len(error_mobile):
#                 for item in new_mobiles:
#                     if item not in error_mobile:
#                         self.mobiles[item] = new_mobiles[item]
#
#             print(self.mobiles)
#             #获取付临门交易明细
#             self.handler_tranlist()
#
#             count = 2
#             res = self.request_data()
#             while not res:
#                 res = self.request_data()
#                 count -= 1
#                 if not count:
#                     break
#             if count:
#                 while item in self.mobiles:
#                     if not self.mobiles[item]['tranlist']:
#                         print("mobile:{},获取临门交易明细有误!".format(item))
#                         continue
#                     if not len(self.mobiles[item]['tranlist']):
#                         continue
#             else:
#                 print("请求对方服务器出错!")
#
# def flmInsert(tranlist):
#
#     data= {
#         "tranlist" : tranlist
#     }
#     res = send_request(
#         url='http://localhost:9601/api/paycall/flm_callback',
#         method='POST',
#         data={"data" : data})
#     print("请求后返回的POST数据:",res)
#     return None
#
# def callback(tranlist_obj):
#     if not len(tranlist_obj['transList']):
#         return None
#     print("付临门查询出的数据:",tranlist_obj)
#
#     res = flmQuery()
#     print("服务器查询的数据:",res)
#     ordercodes = [ item['ordercode'] for item in res ]
#
#     tranlist = [ item for item in tranlist_obj['transList'] if item['status']=='交易成功' and item['orderNo'] not in ordercodes and item['remark'] >= start_date ]
#
#     if len(tranlist):
#         print("请求的数据:",tranlist)
#         flmInsert(tranlist)

if __name__ == '__main__':
    redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=5, password="plokiqikj##mlad,..ad")
    redis_pool = redis.StrictRedis(connection_pool=redis_pool)

    value={
        "today_amount":10000.0,
        "tot_amount":999999.0,
        "today_order_tot_count":2,
        "today_order_ok_count":1,
        "tot_order_tot_count":10,
        "tot_order_ok_count":100
    }
    redis_pool.hset('ordercount',1,json.dumps(value))
