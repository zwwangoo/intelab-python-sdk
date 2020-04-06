# encoding=utf-8
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

from intelab_python_sdk.logger import log

SMTP_SERVER = {
    '163.com': ('smtp.163.com', 465),
    'qq.com': ('smtp.qq.com', 465),
    'ilabservice.com': ('smtp.qiye.aliyun.com', 465)
}


class EMailMessage(object):
    """Email封装

    :param sender: 发件人邮箱，以``@163.com``或``@qq.com``或``@ilabservice.com``结尾
    :param name: 发件人名称
    :param password: 密码
    """

    def __init__(self, sender, name, password):
        self.sender = sender
        self.name = name
        self.password = password
        self.smtp_host, self.smtp_port = SMTP_SERVER.get(
            self.sender.split('@')[-1])

    def create(self, receivers, content, subject,
               content_type='plain',
               annex_path=None, annex_name=''):
        """ 创建邮件

        :param receivers: list. 收件人邮箱，可以包含多个
        :param content: str. 要发送的内容，拼接好的string。如果是html格式， :param content_type: 为 ``html``
        :param subject: str. 邮件主题
        :param content_type: (optional)
        :param annex_path: 附件文件路径
        :param annex_name: 附件文件名
        """

        msg = MIMEMultipart()
        msg.attach(MIMEText(content, content_type, 'utf-8'))
        msg['From'] = formataddr([self.name, self.sender])
        msg['To'] = ','.join(receivers) if isinstance(receivers, list) \
            else receivers
        msg['Subject'] = subject

        if annex_path:  # 添加附件
            xlsxpart = MIMEApplication(open(annex_path, 'rb').read())
            xlsxpart.add_header('Content-Disposition',
                                'attachment', filename=annex_name)
            msg.attach(xlsxpart)
        return msg

    def send(self, receivers, msg):
        """发送邮件
        """

        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        try:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, receivers, msg.as_string())
            server.quit()
            log.info('Email sent successfully.')
        except Exception as e:
            log.error("An error occurred while sending the message!!! %s", e)
