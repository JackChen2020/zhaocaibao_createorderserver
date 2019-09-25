from utils.exceptions import PubErrorCustom
from apps.pay.models import PayType,PayPass
from apps.order.models import Order
from apps.public.models import QrCodeLinkPayType,TbDFPool
from libs.utils.mytime import timestamp_toDatetime,datetime_toTimestamp
from apps.utils import url_join
from apps.pay.models import PayType,PayPassLinkType
from apps.lastpass.utils import LastPass_JLF,LastPass_TY,LastPass_DD,\
    LastPass_YZL,LastPass_OSB,LastPass_BAOZHUANKA,LastPass_LIMAFU,LastPass_JUXING,LastPass_MK,\
        LastPass_TONGYU,LastPass_JIAE,LastPass_DONGFANG,LastPass_XIONGMAO,LastPass_KUAILAI,LastPass_SHANGHU,\
            LastPass_HAOYUN,LastPass_FENGNIAO,LastPass_LIANJINHAI,LastPass_JIUFU,LastPass_XINGYUANFU,LastPass_XINGYUN,LastPass_CHUANGYUAN,\
                LastPass_JLFZFB,LastPass_WXHFYS,LastPass_ZFBHFYS,LastPass_SDGY,LastPass_JIABAO,LastPass_QIANWANG,LastPass_CHUANGYUAN_YUANSHENG,\
                    LastPass_MIFENG,LastPass_TIGER,LastPass_GUAISHOU,LastPass_DINGSHENG,LastPass_CZKJ,LastPass_SBGM,LastPass_XINGHE,LastPass_YUANLAI,\
                        LastPass_JINGSHA,LastPass_ANJIE,LastPass_hahapay,LastPass_SHUIJING,LastPass_KUAIJIE,LastPass_ALLWIN

class CreateOrder(object):

    def __init__(self,**kwargs):

        self.user = kwargs.get('user')
        self.request_param = kwargs.get("request_param")
        self.lock = kwargs.get("lock","0")

        self.paypasslinktype = None
        self.qrcodelinkpaytype = None

        self.order = None

    def get_paypasslinktype(self):
        paypass = PayPassLinkType.objects.raw(
            """
            SELECT t1.*,t2.typename ,t2.name as paytypename,t3.name as paypassname FROM paypasslinktype as t1 
            INNER JOIN paytype as t2 on t1.paytypeid = t2.paytypeid
            INNER JOIN paypass as t3 on t1.passid = t3.paypassid
            WHERE t1.to_id=%s and t1.type='1' 
            """, [self.user.userid]
        )
        paypass = list(paypass)
        return paypass

    def check_request_param(self):

        if not self.request_param.get("down_ordercode"):
            raise PubErrorCustom("订单号不存在!")

        try:
            amount = float(self.request_param.get('amount'))
            if amount <= 0.0:
                raise PubErrorCustom("订单金额不能为0")
        except:
            raise PubErrorCustom("订单金额格式不正确!")

        # try:
        #     timestamp_toDatetime(self.request_param.get('createtime'))
        # except:
        self.request_param['createtime'] = datetime_toTimestamp()

        if not self.request_param.get('client_ip'):
            raise PubErrorCustom("客户端IP不能为空!")

        if not self.request_param.get("notifyurl"):
            raise PubErrorCustom("回调地址不能为空!")

        if not self.request_param.get("ismobile"):
            raise PubErrorCustom("是否手机标志不能为空!")

        if Order.objects.filter(userid=self.user.userid, down_ordercode=self.request_param.get('down_ordercode')).exists():
            raise PubErrorCustom("该订单已生成,请勿重复生成订单!")

        paypass = self.get_paypasslinktype()

        if not self.request_param.get('paytypeid'):
            if not len(paypass):
                raise PubErrorCustom("通道暂未开放!")
            if len(paypass) > 1:
                raise PubErrorCustom("通道暂未开放!")
            self.request_param['paytypeid'] = paypass[0].paytypeid
            self.paypasslinktype = paypass[0]
        else:
            for item in paypass:
                if str(item.paytypeid) == str(self.request_param.get('paytypeid')):
                    self.paypasslinktype = item
            if not self.paypasslinktype:
                raise PubErrorCustom("通道传入有误!")

    def create_order_handler(self):

        self.order  = Order.objects.create(**{
            "userid": self.user.userid,
            "down_ordercode": self.request_param.get("down_ordercode"),
            "paypass": self.paypasslinktype.passid,
            "paypassname": self.paypasslinktype.paypassname,
            "paytype": self.paypasslinktype.paytypeid,
            "paytypename": self.paypasslinktype.typename + self.paypasslinktype.paytypename,
            "amount": self.request_param.get("amount"),
            "status": "1",
            "ismobile": self.request_param.get("ismobile"),
            "client_ip": self.request_param.get("client_ip"),
            "notifyurl": self.request_param.get("notifyurl"),
            "createtime": self.request_param.get("createtime"),
            'qr_type': self.qrcodelinkpaytype.type if self.qrcodelinkpaytype and len(self.qrcodelinkpaytype.type) else "",
            "keep_info": self.request_param,
            "lock":self.lock
        })

    def select_pass(self):
        # 招财宝
        if self.paypasslinktype.passid in (0, 1):

            tbdfpool = TbDFPool.objects.select_for_update().filter(amount=self.order.amount,status='0')

            if not tbdfpool.exists():
                raise PubErrorCustom("暂时无码!")

            data={}

            data['amount'] = self.order.amount
            data['ordercode'] = tbdfpool[0].ordercode
            data['qrcode'] = url_join(tbdfpool[0].qrcode)

            tbdfpool[0].status='4'
            tbdfpool[0].save()

            self.order.tbdforder = tbdfpool[0].ordercode
            self.order.save()

            return {"res": data, "userid": self.order.userid, "ordercode": self.order.ordercode, "htmlfile": "pay10.html"}

    def run(self):
        self.check_request_param()
        self.create_order_handler()
        return self.select_pass()


# def get_type(request):
#
#
#     paypass = PayPassLinkType.objects.raw(
#         """
#         SELECT t1.*,t2.typename ,t2.name as paytypename FROM paypasslinktype as t1
#         INNER JOIN paytype as t2 on t1.paytypeid = t2.paytypeid
#         WHERE t1.to_id=%s and t1.type='1'
#         """, [request.user.userid]
#     )
#     paypass = list(paypass)
#     if not len(paypass):
#         raise PubErrorCustom("请联系客服设置支付方式!")
#     if len(paypass)>1:
#         raise PubErrorCustom("多种方式请通过支付方式接口获取,根据需要选择!")
#     paypass=paypass[0]
#     return paypass.paytypeid
#
# def check_type(request,data):
#     paypass = PayPassLinkType.objects.raw(
#         """
#         SELECT t1.*,t2.typename ,t2.name as paytypename FROM paypasslinktype as t1
#         INNER JOIN paytype as t2 on t1.paytypeid = t2.paytypeid
#         WHERE t1.to_id=%s and t1.type='1'
#         """, [request.user.userid]
#     )
#     for item in paypass:
#         if str(item.paytypeid) == str(data.get('paytypeid')):
# #             return True
# #
# #     return False
#
# def check_data(request):
#
#     data = request.data_format
#
#     if not data.get('paytypeid'):
#         data['paytypeid'] = get_type(request)
#     else:
#         if not check_type(request,data):
#             raise PubErrorCustom("支付方式不正确!")
#
#     try:
#         paytype = PayType.objects.get(paytypeid=data['paytypeid'])
#     except PayType.DoesNotExist:
#         raise PubErrorCustom("支付方式不存在,请通过接口获取!")
#
#     qrcodelinkpaytype=""
#     if request.user.paypassid in (0, 1):
#         try:
#             qrcodelinkpaytype = QrCodeLinkPayType.objects.get(paytypeid=data['paytypeid'])
#         except QrCodeLinkPayType.DoesNotExist:
#             raise PubErrorCustom("支付方式与二维码类型未关联!")
#
#     if not data.get("down_ordercode"):
#         raise PubErrorCustom("订单号不存在!")
#
#     if Order.objects.filter(userid=request.user.userid, down_ordercode=data.get('down_ordercode')).exists():
#         raise PubErrorCustom("该订单已生成,请勿重复生成订单!")
#
#     try:
#         amount = float(data.get('amount'))
#         if amount <= 0.0:
#             raise PubErrorCustom("订单金额不能为0")
#     except:
#         raise PubErrorCustom("订单金额格式不正确!")
#
#     try:
#         timestamp_toDatetime(data.get('createtime'))
#     except:
#         data['createtime'] = datetime_toTimestamp()
#         # raise PubErrorCustom("创建订单时间不正确!")
#
#     if not data.get('client_ip'):
#         raise PubErrorCustom("客户端IP不能为空!")
#
#     if not data.get("notifyurl"):
#         raise PubErrorCustom("回调地址不能为空!")
#
#     if not data.get("ismobile"):
#         raise PubErrorCustom("是否手机标志不能为空!")
#
#     return paytype,qrcodelinkpaytype
#
#
# def check_passtype(request):
#     try:
#         paypass = PayPass.objects.get( paypassid= request.user.paypassid)
#     except PayPass.DoesNotExist:
#         raise PubErrorCustom("支付渠道不存在!")
#
#     return paypass
#
# def create_order_handler(data,request,paytype,paypass,qrcodelinkpaytype):
#
#     order = Order.objects.create(**{
#         "userid": request.user.userid,
#         "down_ordercode": data.get("down_ordercode"),
#         "paypass" : paypass.paypassid,
#         "paypassname" : paypass.name,
#         "paytype": paytype.paytypeid,
#         "paytypename": paytype.typename + paytype.name,
#         "amount": data.get("amount"),
#         "status": "1",
#         "ismobile": data.get("ismobile"),
#         "client_ip": data.get("client_ip"),
#         "notifyurl": data.get("notifyurl"),
#         "createtime": data.get("createtime"),
#         'qr_type' : qrcodelinkpaytype.type if qrcodelinkpaytype and len(qrcodelinkpaytype) else "",
#         "keep_info": data
#     })
#
#     #傲银渠道
#     if request.user.paypassid in (0,1):
#         if not data.get('allwin_test'):
#             if float(data.get("amount")) < 300 or float(data.get("amount")) > 5000:
#                 raise PubErrorCustom("限额300至5000")
#         return QrTypePage(qrcodelinkpaytype.type,order).run()
#     #吉米支付宝原生渠道
#     elif str(request.user.paypassid) == '2':
#         raise PubErrorCustom("通道量满单，尽快配量")
#     elif str(request.user.paypassid) == '4':
#         request_data = {
#             "uid": str(order.userid),
#             "amount": order.amount,
#             "outTradeNo": str(order.ordercode),
#             "ip": order.client_ip,
#             "notifyUrl": url_join('/api/lastpass/juli_callback')
#         }
#         res = LastPass_JLF(data=request_data).run()
#         if not res[0]:
#             raise PubErrorCustom(res[1])
#         return {"path": res[1]}
#     elif str(request.user.paypassid) == '5':
#         request_data = {
#             "pay_orderid": str(order.ordercode),
#             "pay_amount": order.amount,
#             "pay_notifyurl": url_join('/api/lastpass/tianyi_callback')
#         }
#         res = LastPass_TY(data=request_data).run()
#         print(res)
#         if not res[0]:
#             raise PubErrorCustom("生成订单失败,请稍后再试!")
#
#         with open('/var/html/tianyi/{}.html'.format(order.ordercode), 'w') as f1:
#             f1.write(res[1])
#         return {"path": url_join('/tianyi/{}.html').format(order.ordercode) }


class QrTypePage(object):

    def __init__(self,type=None,order=None):
        self.type = type
        self.order = order

        self.custom_select = [
            {
                "userid":11,
                "type":'QR005',
                "paytype" : 'alipay'
            },
            {
                "userid": 4,
                "type": 'QR005',
                "paytype": 'wechat'
            }
        ]

    def run(self):

        for item in self.custom_select:
            if item['userid'] == self.order.userid and item['type'] == self.type :
                return {"path": url_join("/pay/#/{}/{}".format(item['paytype'],self.order.ordercode))}

        if self.type == 'QR001':
            return {"path": url_join("/pay/#/wechat/{}".format(self.order.ordercode))}
        elif self.type == 'QR005':
            return {"path": url_join("/pay/#/wechat/{}".format(self.order.ordercode))}
        elif self.type == 'QR010':
            return {"path": url_join("/pay/#/wechat/{}".format(self.order.ordercode))}
        elif self.type == 'QR015':
            return {"path": url_join("/pay/#/wechat/{}".format(self.order.ordercode))}
        elif self.type == 'QR020':
            return {"path": url_join("/pay/#/wechat/{}".format(self.order.ordercode))}
        else:
            return {"path": url_join("/pay/#/wechat/{}".format(self.order.ordercode))}

