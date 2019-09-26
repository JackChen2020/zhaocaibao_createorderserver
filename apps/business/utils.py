from utils.exceptions import PubErrorCustom,InnerErrorCustom
from apps.order.models import Order
from apps.public.models import TbDFPool
from libs.utils.mytime import datetime_toTimestamp
from apps.utils import url_join
from apps.pay.models import PayPassLinkType
from libs.utils.mytime import UtilTime
from libs.utils.log import logger
import random
from django.db.models import Q

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

            tbdfbase = TbdfBase(self.order.amount)

            tbdfpoolObj = tbdfbase.get_qrcode()

            data={}

            data['amount'] = self.order.amount
            data['ordercode'] = tbdfpoolObj.ordercode
            data['qrcode'] = url_join(tbdfpoolObj.qrcode)
            data['pay_url'] = tbdfpoolObj.url
            data['start_time'] = self.order.createtime

            self.order.tbdforder = tbdfpoolObj.ordercode
            self.order.qr_id = tbdfpoolObj.id
            self.order.save()

            return {"res": data, "userid": self.order.userid, "ordercode": self.order.ordercode, "htmlfile": "pay10.html"}

    def run(self):
        self.check_request_param()
        self.create_order_handler()
        return self.select_pass()


class TbdfBase(object) :

    def __init__(self,amount):
        self.ut = UtilTime()

        self.amount = amount

        #当前时间
        self.today = self.ut.today

        #有效时间 300秒
        self.order_failure_time = 300

        #订单失效时间 4填
        self.order_max_failure_time = 3 * 24 * 60 * 60

    # def get_qrcode_obj(self,id):
    #     try:
    #         qrcode_obj = Qrcode.objects.get(id=id,status='0')
    #     except Qrcode.DoesNotExist:
    #         raise PubErrorCustom("无此二维码!")
    #     return qrcode_obj


    def get_expire_time(self,updtime=None,timetype=None):
        """
        获取过期时间(时间戳)
        :param timetype: 为None时默认为时间戳,为True代表时间
        :return:
        """

        return  self.ut.timestamp_to_arrow(updtime).replace(seconds=self.order_failure_time ).timestamp if not timetype else \
                     self.ut.timestamp_to_arrow(updtime).replace(seconds=self.order_failure_time )

    def get_valid_max_time(self,timetype=None):
        """
        获取对应码的有效时间(时间戳)
        :param timetype: 为None时默认为时间戳,为True代表时间
        :return:
        """

        return self.today.replace(seconds=self.order_max_failure_time * -1).timestamp if not timetype else \
                     self.today.replace(seconds=self.order_max_failure_time * -1)

    def get_valid_time(self,timetype=None):
        """
        获取对应码的有效时间(时间戳)
        :param timetype: 为None时默认为时间戳,为True代表时间
        :return:
        """

        return self.today.replace(seconds=self.order_failure_time * -1).timestamp if not timetype else \
                     self.today.replace(seconds=self.order_failure_time * -1)

    def qrcode_valid(self,updtime=None):
        """
        判断二维码是否有效
        :param updtime:  创建时间时间戳
        :return:  True : 有效 , False : 失效
        """

        return True if self.get_valid_time() < updtime else False

    def get_qrcode(self):
        """
        #获取有效二维码
        :param
        :return:
        """
        print(self.get_valid_max_time())
        qrcodes = TbDFPool.objects.filter(status='0',amount=self.amount,createtime__gte=self.get_valid_max_time()).order_by('id')

        if not qrcodes.exists():
            raise InnerErrorCustom("10010", "码池正在加紧上码,请稍等刷新!")
        qrids = [ item.id for item in qrcodes ]

        print(self.get_valid_time())
        qrids_exists = [ item.qr_id for item in Order.objects.select_for_update().filter(Q(qr_id__in=qrids,status=0) | Q(qr_id__in=qrids,status=1 ,createtime__gte=self.get_valid_time())) ]

        logger.info("\n 二维码列表：{} \n 已在订单表里存在的二维码列表：{}".format(qrids,qrids_exists))

        valid_ids = [ item for item in qrids if item not in qrids_exists ]

        if not valid_ids:
            raise InnerErrorCustom("10010", "码池正在加紧上码,请稍等刷新!")

        #筛选出有效二维码
        valid_id = random.sample(valid_ids,1)[0]

        valid_obj = None

        for item in qrcodes:
            print(item.id,valid_id)
            if item.id == valid_id:
                valid_obj = item

        if not valid_obj:
            raise InnerErrorCustom("10010", "码池正在加紧上码,请稍等刷新!")

        valid_obj.updtime = self.ut.timestamp
        print(valid_obj.updtime)
        valid_obj.save()

        return valid_obj

