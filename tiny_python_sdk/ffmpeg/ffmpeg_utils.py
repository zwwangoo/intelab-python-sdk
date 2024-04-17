import re
import os
import subprocess


def time_to_seconds(duration):
    """
    时间字符串转换成秒
    :param duration: 时间格式串, 例如"01:46:00"
    :return seconds: int
    """
    hours, minutes, seconds = duration.split(':')
    seconds = int(seconds)
    if minutes > '00':
        seconds += int(minutes) * 60
    if hours > '00':
        seconds += int(hours) * 3600
    return seconds


def get_time_str(seconds):
    """
    秒转换成时间字符串
    :param seconds: 秒
    :return duration: str '01:46:00'
    """
    if seconds >= 3600:
        s = str('%02d' % (seconds // 3600))
        seconds = seconds % 3600
    else:
        s = '00'
    if seconds > 60:
        s += str(':%02d' % (seconds // 60))
        seconds = seconds % 60
    else:
        s += ':00'

    s += str(':%02d' % seconds)
    return s


def get_video_duration(file_name, start_time='00:00:00', key_word='block unavailable'):
    resolution,  duration, bitrate, media_type = ['0x0'], ['00:00:00'], ['0'], 'VideoHandler'
    size, error_log, fps = 0, '', ['0']

    log_buffer = subprocess.getoutput(
        'ffmpeg -y -ss {} -i {} -t 1 -vframes 1 /tmp/tmp.jpg'.format(start_time, file_name))

    if 'moov atom not found' in log_buffer:
        error_log += log_buffer
    if 'Impossible to open' in log_buffer:
        error_log = log_buffer
    if key_word in log_buffer:
        error_log = log_buffer
    if 'errors in I frame' in log_buffer:
        error_log += log_buffer

    duration = re.findall(r'Duration: (\d\d:\d\d:\d\d)\.\d\d', log_buffer) or duration
    bitrate = re.findall(r'bitrate: (\d+) kb/s', log_buffer) or bitrate
    resolution = re.findall(r'(\d{3,4}x\d{3,4})', log_buffer) or resolution
    fps = re.findall(r', (\d+) fps,', log_buffer) or fps

    if 'SoundHandler' in log_buffer:
        media_type += '+SoundHandler'
    if os.path.isfile(file_name):
        size = os.path.getsize(file_name) / 1024.0 / 1024.0

    video_info = {
        'duration': duration[0], 'bitrate': bitrate[0],
        'resolution': resolution[0], 'media_type': media_type,
        'file_name': file_name, 'size': round(size, 2),
        'fps': fps[0]
    }
    return video_info, error_log


def judge_video_error(file_name):
    """
    :param file_name: 文件路径
    :return duration, bitrate, error_log
    """
    # 通过ffmpeg打开文件两次判定文件是否花屏
    video_info, error_log = get_video_duration(file_name)
    *_, error_log = get_video_duration(file_name, video_info['duration'])\
        if not error_log else (video_info, error_log)
    return video_info, error_log
