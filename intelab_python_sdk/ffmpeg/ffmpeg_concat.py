import os
import shutil

from . import log, run_shell


def concat(file_list, output, removed=False):
    """
    :param file_list: 合并的文件列表
    :param output: 输出文件
    :param removed: 合并成功之后是否删除原有的视频文件
    :return :
    """
    if len(file_list) < 2:
        shutil.copy(file_list[0], output)
    else:
        file_name_list = _get_file_name_list(file_list, output)
        concat_shell = (
            'ffmpeg '
            '-y -v info '
            '-f concat -safe 0 -i {} '
            '-c copy '
            '-bsf:a aac_adtstoasc -movflags +faststart '
            '{}'
        ).format(file_name_list, output)

        error_log = run_shell(concat_shell)
        if error_log:
            error_files = []
            for file_name in file_list:
                if file_name in error_log:
                    os.remove(file_name)
                    error_files.append(file_name)

            # TODO 合并的视频文件音频问题
            if error_files:
                sub_file_list = [file_name for file_name in file_list if file_name not in error_log]
                return concat(sub_file_list, output, removed=True)

        if os.path.isfile(file_name_list):
            os.remove(file_name_list)

    if os.path.isfile(output) and removed:
        for file in file_list:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    return output


def _get_file_name_list(file_list, output):
    file_name_list = '{}.list.tmp'.format(output)
    with open(file_name_list, 'w+') as f:
        for file_name in file_list:
            if not os.path.isfile(file_name):
                log.warning('No such file or directory: %s', file_name)
                continue
            f.write('file {}\n'.format(file_name))
            log.debug('add file %s to %s', file_name, file_name_list)
    return file_name_list
