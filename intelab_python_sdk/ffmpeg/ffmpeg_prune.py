from . import log, run_shell


def prune(file_name, output, start_time=0, duration=None):
    """
    :param file_name: 剪切的文件
    :param output: 输出文件
    :param start_time: 剪切开始的时间
    :param duration: 持续时间
    :return :
    """

    if duration:
        _duration = '-t {} '.format(duration)
    else:
        _duration = ''

    shell = (
        'ffmpeg '
        '-y '
        '-ss {} {}'
        '-i {} '
        '-c:a copy '
        '-c:v copy '
        '{}'
    ).format(start_time, _duration, file_name, output)
    log.info(shell)
    run_shell(shell)

    return output
