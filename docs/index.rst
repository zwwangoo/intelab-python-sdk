.. intelab-python-sdk documentation master file, created by
   sphinx-quickstart on Thu Dec 19 11:44:07 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

intelab-python-sdk
==============================================

安装
----

.. code-block:: bash

    $ pip install intelab-python-sdk

邮箱模块(V0.3.5)
----------------

对简单的邮件发送进行封装

.. warning::
    目前仅支持 @163.com、@qq.com、@ilabservice.com

Usage::

    >>> from intelab_python_sdk.email import EMailMessage
    >>> email = EMailMessage('w_angzhiwen@163.com', '发送者', 'xxxxx')  # 'xxxx' 用户密码
    >>> msg = email.create(['zw.wang@ilabservice.com'], '你好，我是机器人', '无主题')  # 创建邮件内容
    >>> msg = email.send(['zw.wang@ilabservice.com'], msg)  # 发送


logging 模块(V0.3.0)
--------------------

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

缓存(V0.3.0)
------------

Usage::

    >>> from intelab_python_sdk.cache import FileSystemCache
    >>> from datetime import datetime
    >>> cache = FileSystemCache('.cache')
    >>> cache.set('12', datetime.now())
    >>> cache.get('12')
    datetime.datetime(2019, 12, 19, 12, 16, 1, 511077)

*说明：*

1. 以key为文件名，存储python数据类型

更新历史
========

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

API
===

.. toctree::
    :maxdepth: 2

    logger
    cache
    email
