

from apps.utils import GenericViewSetCustom
from rest_framework.decorators import list_route
from core.decorator.response import Core_connector
from utils.exceptions import PubErrorCustom,InnerErrorCustom
from utils.log import logger
from apps.lastpass.utils import LastPass_JLF,LastPass_TY,LastPass_DD,LastPass_YZL,\
    LastPass_OSB,LastPass_BAOZHUANKA,LastPass_LIMAFU,LastPass_JUXING,LastPass_MK,\
        LastPass_TONGYU,LastPass_JIAE,LastPass_XIONGMAO,LastPass_KUAILAI,LastPass_SHANGHU,LastPass_FENGNIAO,LastPass_LIANJINHAI,LastPass_JIUFU, \
            LastPass_XINGYUANFU,LastPass_XINGYUN,LastPass_CHUANGYUAN,LastPass_WXHFYS,LastPass_SDGY,LastPass_JIABAO,LastPass_QIANWANG,\
                LastPass_CHUANGYUAN_YUANSHENG,LastPass_MIFENG,LastPass_TIGER,LastPass_GUAISHOU,LastPass_DINGSHENG,LastPass_CZKJ,LastPass_SBGM,\
                    LastPass_XINGHE,LastPass_YUANLAI,LastPass_ANJIE,LastPass_KUAIJIE

from rest_framework.response import Response
from django.db import transaction
from functools import wraps
import json
from django.shortcuts import HttpResponse

class Jl_HttpResponse(Response):

    def __init__(self,data=None):
        super().__init__(data=data)


class Gs_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("success")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("error")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("error")
        return wrapper


class Error_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("OK")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                a=1/0
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                a=1/0
        return wrapper

class Jl_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("success")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("fail")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("fail")
        return wrapper

class Ty_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("OK")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("fail")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("fail")
        return wrapper



class Yzl_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("success")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("fail")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("fail")
        return wrapper


class OSB_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("success")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("fail")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("fail")
        return wrapper

class BAOZHUANKA_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("ok")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("fail")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("fail")
        return wrapper

class JUXING_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("success")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("fail")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("fail")
        return wrapper

class Lmf_Core_connector:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("SUCCESS")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("fail")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("fail")
        return wrapper

class Lmf_Core_connector1:
    def __init__(self,**kwargs):
        pass
    def __run(self,func,outside_self,request,*args, **kwargs):
        with transaction.atomic():
            res = func(outside_self, request, *args, **kwargs)

    def __call__(self,func):
        @wraps(func)
        def wrapper(outside_self,request,*args, **kwargs):
            try:
                self.__run(func,outside_self,request,*args, **kwargs)
                return HttpResponse("SUCCESS")
            except PubErrorCustom as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),e.msg))
                return HttpResponse("SUCCESS")
            except Exception as e:
                logger.error('[%s : %s  ] : [%s]'%(outside_self.__class__.__name__, getattr(func, '__name__'),str(e)))
                return HttpResponse("SUCCESS")
        return wrapper

class LastPassAPIView(GenericViewSetCustom):

    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def juli_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_JLF(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @JUXING_Core_connector()
    def tianyi_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_TY(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Ty_Core_connector()
    def mk_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_MK(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Ty_Core_connector()
    def jiabao_callback(self, request, *args, **kwargs):
        data={}
        # for item in request.data:
        #     data[item] = request.data[item]
        data['memberid'] = request.data['memberid']
        data['orderid'] = request.data['orderid']
        data['amount'] = request.data['amount']
        data['transaction_id'] = request.data['transaction_id']
        data['datetime'] = request.data['datetime']
        data['returncode'] = request.data['returncode']
        data['sign'] = request.data['sign']

        LastPass_JIABAO(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Lmf_Core_connector()
    def tongyu_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        data1={}
        for item in data:
            data1=json.loads(item)
        data={}
        for item in data1:
            data[item] = data1[item]
        LastPass_TONGYU(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Ty_Core_connector()
    def dada_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_DD(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Yzl_Core_connector()
    def yzl_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_YZL(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @OSB_Core_connector()
    def osb_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_OSB(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @BAOZHUANKA_Core_connector()
    def baozhanka_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_BAOZHUANKA(data=data).call_run()
        return None

    @list_route(methods=['GET'])
    @Lmf_Core_connector()
    def limafu_callback(self, request, *args, **kwargs):
        data={}
        for item in request.query_params:
            data[item] = request.query_params[item]
        LastPass_LIMAFU(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @JUXING_Core_connector()
    def juxing_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_JUXING(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @JUXING_Core_connector()
    def jiae_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        print(data)
        LastPass_JIAE(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @JUXING_Core_connector()
    def xiongmao_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        print(type(request.data['return_type']))
        tmp = json.loads(request.data['return_type'])
        for item in tmp:
            data[item] = tmp[item]

        LastPass_XIONGMAO(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @JUXING_Core_connector()
    def kuailai_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        print(data)

        LastPass_KUAILAI(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Lmf_Core_connector()
    def shanghu_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        print(data)

        LastPass_SHANGHU(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @JUXING_Core_connector()
    def fengniao_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        print(data)

        LastPass_FENGNIAO(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @JUXING_Core_connector()
    def lianjinhai_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        print(data)

        LastPass_LIANJINHAI(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Ty_Core_connector()
    def jiufu_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_JIUFU(data=data).call_run()
        return None


    @list_route(methods=['GET'])
    @BAOZHUANKA_Core_connector()
    def xingyuanfu_callback(self, request, *args, **kwargs):
        data={}
        for item in request.query_params:
            data[item] = request.query_params[item]
        LastPass_XINGYUANFU(data=data).call_run()
        return None

    @list_route(methods=['GET'])
    @Lmf_Core_connector()
    def xingfu_callback(self, request, *args, **kwargs):
        data={}
        for item in request.query_params:
            data[item] = request.query_params[item]
        print(data)
        LastPass_XINGYUN(data=data).call_run()
        return None



    @list_route(methods=['POST'])
    @BAOZHUANKA_Core_connector()
    def chuangyuan_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        data1={}
        for item in data:
            data1=json.loads(item)
        data={}
        for item in data1:
            data[item] = data1[item]
        LastPass_CHUANGYUAN(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Lmf_Core_connector1()
    def wxhf_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]

        print(data)
        LastPass_WXHFYS(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Ty_Core_connector()
    def sdgy_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_SDGY(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Error_Core_connector()
    def qianwang_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]
        LastPass_QIANWANG(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def chuangyuan_yuansheng_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_CHUANGYUAN_YUANSHENG(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def mifeng_callback(self, request, *args, **kwargs):
        print(request.data)
        data={}
        for item in request.data.get('return_type'):
            data[item] = request.data.get('return_type')[item]
        print(data)
        LastPass_MIFENG(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Ty_Core_connector()
    def tiger_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_TIGER(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Gs_Core_connector()
    def guaishou_callback(self, request, *args, **kwargs):
        print(request.data)
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_GUAISHOU(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Ty_Core_connector()
    def dingsheng_callback(self, request, *args, **kwargs):
        data={}
        for item in request.data:
            data[item] = request.data[item]
        LastPass_DINGSHENG(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def czkj_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]
        LastPass_CZKJ(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def sbgm_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]
        LastPass_SBGM(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def anjie_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]
        LastPass_ANJIE(data=data).call_run()
        return None

    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def xinghe_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]
        LastPass_XINGHE(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Jl_Core_connector()
    def yuanlai_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]
        LastPass_YUANLAI(data=data).call_run()
        return None


    @list_route(methods=['POST'])
    @Gs_Core_connector()
    def kuaijie_callback(self, request, *args, **kwargs):
        data={}
        print(request.data)
        for item in request.data:
            data[item] = request.data[item]
        LastPass_KUAIJIE(data=data).call_run()
        return None