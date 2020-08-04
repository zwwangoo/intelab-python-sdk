# encoding=utf-8
import time
import urllib
import base64
import hashlib
import hmac

try:
    quote_plus = urllib.parse.quote_plus
except AttributeError:
    quote_plus = urllib.quote_plus

from intelab_python_sdk.logger import log
from intelab_python_sdk.utils import do_request


class DingTalkMessage(object):
    """钉钉机器人消息推送
    """

    headers = {"Content-Type": "application/json;charset=utf-8"}

    def __init__(self, webhook, secret=None, pc_slide=True):

        self.webhook = webhook
        self.pc_slide = pc_slide
        self.secret = secret
        self.pc_slide = pc_slide
        self.start_time = time.time()
        if self.secret is not None and self.secret.startswith('SEC'):
            self._update_webhook()

    def send_text(self, content, mobiles=None, at_all=False):
        """发送文本消息

        :param content: 文本内容
        :param mobiles: 群中at的用户，可以为空
        :param at_all: bool. at群中所有人，默认值为False
        """
        if mobiles is None:
            mobiles = []
        msg_dict = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": mobiles,
                "isAtAll": at_all
            }
        }
        return self._send(msg_dict)

    def send_link(self, title, text, message_url, pic_url=''):
        """ link类型

        :param title: 消息标题
        :param text: 消息内容（如果太长自动省略显示）
        :param message_url: 点击消息触发的URL
        :param pic_url: 图片URL（可选）
        :return: 返回消息发送结果
        """
        msg_dict = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": pic_url,
                "messageUrl": self._msg_open_type(message_url)
            }
        }
        log.debug('link类型：%s' % msg_dict)
        return self._send(msg_dict)

    def send_markdown(self, title, text, mobiles=None, at_all=False):
        """ markdown

        :param title: 消息标题
        :param text: 消息内容。支持简单的md语法。
        :param: mobiles:
        :param at_all:
        :return:
        """
        if mobiles is None:
            mobiles = []

        msg_dict = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text,
            },
            "at": {
                "atMobiles": mobiles,
                "isAtAll": at_all
            }
        }
        return self._send(msg_dict)



    def _update_webhook(self):
        """
        钉钉群自定义机器人安全设置加签时，签名中的时间戳与请求时不能超过一个小时，
        所以每个1小时需要更新签名
        """
        timestamp = round(self.start_time * 1000)
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(self.secret.encode(), string_to_sign.encode(),
                             digestmod=hashlib.sha256).digest()

        sign = quote_plus(base64.b64encode(hmac_code))
        self.webhook = '{}&timestamp={}&sign={}'.format(
            self.webhook, str(timestamp), sign)

    def _msg_open_type(self, url):
        """
        消息链接的打开方式
        1、默认或不设置时，为浏览器打开：pc_slide=False
        2、在PC端侧边栏打开：pc_slide=True
        """
        return 'dingtalk://dingtalkclient/page/link?url={}&pc_slide={}'.format(
            quote_plus(url), 'true' if self.pc_slide else 'false')

    def _send(self, data):
        now = time.time()

        if now - self.start_time >= 3600 \
                and self.secret is not None \
                and self.secret.startswith('SEC'):
            self.start_time = now
            self._update_webhook()
        try:
            res = do_request('POST', url=self.webhook, data=data,
                             headers=self.headers)
            if 'errcode' in res and res['errcode'] == 0:
                log.info('dingtalk message sent is successful.')
                return True
            else:
                raise ValueError(res)
        except Exception as e:
            log.error("dingtalk message sent is unsuccessful!!!\n %s", e)
        return False
