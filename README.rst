intelab-python-sdk
==================

安装
----

.. code-block:: bash

    $ pip install intelab-python-sdk

logging 模块(V0.3.0)
--------------------

Usage::

    >>> from intelab_python_sdk.logger import log_init
    >>> # 初始化配置
    >>> log = log_init('test', debug=True, log_path='./logs')
    >>> log.info('info')
    2019-12-16T17:46:41.930061-+08:00 wen-work-pc 25689 test
    INFO root:<ipython-input-5-6a92ee17c096>:1
    Message: info

    >>> log.debug('debug')
    2019-12-16T17:47:31.113047-+08:00 wen-work-pc 25689 test
    DEBUG root:<ipython-input-6-03b5a4252de9>:1
    Message: debug

    >>> log.error('error')
    2019-12-16T17:48:02.338739-+08:00 wen-work-pc 25689 test
    ERROR root:<ipython-input-7-5bfd94e0c8ba>:1
    Message: error

    >>> import logging  # 其他文件中
    >>> log1 = logging.getLogger()
    >>> log1.info('info')
    2019-12-16T17:46:41.930061-+08:00 wen-work-pc 25689 test
    INFO root:<ipython-input-6-d225ecf23612>:1
    Message: info

*说明：*

1. info日志输出到指定路径下的``log.info.{日期}``
#. error日志输出到指定路径下的``error.info.{日期}``
#. 日志文件每天零点切分
#. 修复多进程下零点时切分出多个日志文件的Bug