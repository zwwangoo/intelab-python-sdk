intelab-python-sdk
==================

安装
----

.. code-block:: bash

    $ pip install intelab-python-sdk

FFmpeg常用工具(V0.6.0)
------------------------

python运行ffmpeg命令执执行常用的视频处理命令，依赖系统安装的ffmpeg。

Linux::
    sudo apt install ffmpeg

功能：

- 视频流分片录制--`ffmpeg_record.py`
- 拼接多个视频文件--`ffmpeg_concat.py`
- 获取流地址的当前一帧--`ffmpeg_capture.py`
- mp4转mp3--`ffmpeg_mp4tomp3.py`
- 视频裁剪--`ffmpeg_prune.py`

CPU资源监控脚本(V0.5.0)
-----------------------

协助自己在服务器端监控进程的使用资源情况。每一秒打印一次。

Usag::
    $ intelab_python_sdk ffmpeg
    PID    CPU    MEM    MCPU
    2243   0.1    0.1    0.1    intelab_python_sdk ffmpeg


钉钉群机器人信息发送(V0.4.0)
----------------------------
钉钉机器人是钉钉群的一个高级扩展功能， 目前自定义机器人支持文本（text）、链接（link）

`官方文档参考 <https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq>`__

Usage::

    >>> from intelab_python_sdk.dingtalk import DingTalkMessage
    >>> dingtalk = DingTalkMessage(webhook, secret)
    >>> dingtalk.send_text('这是文本信息', mobiles=['15131601294'], at_all=False)  # mobiles是at群中的人(手机号),at_all为True是at全体
    >>> dingtalk.send_link('这是标题', '这是内容', 'https://www.baidu.com')
    >>> dingtalk.send_markdown('这是标题', '# 这是内容 \n> 这是引用\n [百度](https://baidu.com)')

邮箱模块(V0.3.5)
----------------

对简单的邮件发送进行封装

Usage::

    >>> from intelab_python_sdk.email import EMailMessage
    >>> email = EMailMessage('w_angzhiwen@163.com', '发送者', 'xxxxx')  # 'xxxx' 用户密码
    >>> msg = email.create(['zw.wang@ilabservice.com'], '你好，我是机器人', '无主题')  # 创建邮件内容
    >>> msg = email.send(['zw.wang@ilabservice.com'], msg)  # 发送

logging 模块(V0.3.4)
--------------------

日志格式::

    时间 | 主机名 | 进程号 | 名称 | 级别 | 文件和行号 | 信息

Usage::

    >>> from intelab_python_sdk.logger import log_init
    >>> # 初始化配置
    >>> log = log_init('test', debug=True, log_path='./logs')
    >>> log.info('info')
    2019-12-16T17:46:41.930061-+08:00 | wen-work-pc | 25689 | test | INFO    | root:<ipython-input-5-6a92ee17c096>:1 | info
    >>> log.debug('debug')
    2019-12-16T17:47:31.113047-+08:00 | wen-work-pc | 25689 | test | DEBUG   | root:<ipython-input-6-03b5a4252de9>:1 | debug
    >>> log.error('error')
    2019-12-16T17:48:02.338739-+08:00 | wen-work-pc | 25689 | test | ERROR   | root:<ipython-input-7-5bfd94e0c8ba>:1 | error

    >>> import logging  # 其他文件中
    >>> log1 = logging.getLogger()
    >>> log1.info('info')
    2019-12-16T17:46:41.930061-+08:00 | wen-work-pc | 25689 | test | INFO    | root:<ipython-input-6-d225ecf23612>:1 | info

*说明：*

1. info日志输出到指定路径下的 ``log.info.{日期}``
#. error日志输出到指定路径下的 ``error.info.{日期}``
#. 日志文件每天零点切分
#. 修复多进程下零点时切分出多个日志文件的Bug

*log_init参数说明*

TimedRotatingFileHandler的使用说明：

    If backupCount is > 0, when rollover is done, no more than backupCount
    files are kept - the oldest ones are deleted.


缓存(0.3.0)
-----------

Usage::

    >>> from intelab_python_sdk.cache import FileSystemCache
    >>> from datetime import datetime
    >>> cache = FileSystemCache('.cache')
    >>> cache.set('12', datetime.now())
    >>> cache.get('12')
    datetime.datetime(2019, 12, 19, 12, 16, 1, 511077)
    >>> list(cache.keys())
    ['12']
    >>> cache.delete('12')

*说明：*

1. 以key为文件名，存储python数据类型

更新历史
========

0.6.0
-----

*更新内容*

- 视频流分片录制
- 拼接多个视频文件
- 获取流地址的当前一帧
- mp4转mp3
- 视频裁剪

0.5.0
-----

*更新内容*

- 新增CPU资源监控脚本

0.4.0
-----

*更新内容*

- 新增对钉钉群机器人消息推送的接口封装，目前支持文本信息和链接

0.3.5
-----

*更新内容*

- 新增utils.get_host_ip()
- 新增email，对简单的发送邮件进行封装

0.3.4
-----

*更新内容*

- 日志log_init新增使用参数

0.3.1
-----

*更新内容*

- 日志打印在一行，使用 `|` 区分。
