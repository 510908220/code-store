# 配置
可以查看官网[使用说明](http://qydev.weixin.qq.com/wiki/index.php?title=%E5%BE%AE%E4%BF%A1JS-SDK%E6%8E%A5%E5%8F%A3#.E6.AD.A5.E9.AA.A4.E4.B8.80.EF.BC.9A.E5.BC.95.E5.85.A5JS.E6.96.87.E4.BB.B6)

这里说一下再配置时出现的问题, 

```
wx.ready(function () {
    wx.hideOptionMenu();
});
```
放在一个js文件里的话, 里面的代码```wx.hideOptionMenu()```并没有执行.

当和```wx.config```放在一个文件里时就可以执行.


# JS-SDK配置信息

```
wx.config({
    debug: false,
    appId: '{{ sign.appId }}',
    timestamp: {{ sign.timestamp }},
    nonceStr: '{{ sign.nonceStr }}',
    signature: '{{ sign.signature }}',
    jsApiList: [

        'hideOptionMenu',

    ]
});
```

官网有提供接口，下面是整理的:
```
import time
import random
import string
import hashlib


class Sign(object):
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }
    
    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    
    def __create_timestamp(self):
        return int(time.time())
    
    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

```

获取签名各个参数, 签名使用```wechatpy```这个python库:
```
def get_sign_info(request):
    we = WeChatJSAPI(g_client)
    ticket = we.get_jsapi_ticket()
    sign = Sign(ticket, settings.WEIXIN_CONF['domain'] + request.get_full_path())
    sign_info = sign.sign()
    sign_info.update({"appId": settings.WEIXIN_CONF['corpid']})
    return sign_info
```
