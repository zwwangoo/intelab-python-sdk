import os
import time

from . import run_shell


def capture(stream_url, output_jpg, timeout=10, type='jpg'):
    """
    :param stream_url:
    :param output_jpg:
    :param timeout: 连接超时时间，单位s
    :param type: 图片类型，jpg、png
    :return : 截图成功与否
    """

    if type == 'jpg':
        _f = '-f mjpeg'
    else:
        _f = '-f image2'
    shell_cmd = (
        'ffmpeg '
        '-y -rw_timeout {} '  # 设置超时时间10s
        '-i "{}" '
        '-ss 0 '
        '{} '
        '-vframes 1 '
        '{}'
    ).format(timeout * 1000 * 1000, stream_url, _f, output_jpg)

    result = False

    # 尝试三次获取截图
    for _ in range(3):
        error_log = run_shell(shell_cmd, name='ffmpeg_capture')
        if not error_log:
            result = True
            break

        if os.path.isfile(output_jpg):
            os.remove(output_jpg)

        time.sleep(1)

    return result
