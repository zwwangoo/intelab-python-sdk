import os
import re
import threading
import subprocess

from datetime import datetime

from . import log


class FfmpegRecordThread(threading.Thread):

    def __init__(self, name, stream_url, out_file_path, video_duration=300, timeout=5000000, **kwargs):
        """
        :param name:
        :param stream_url: 流地址
        :param out_file_path:
        :param video_duration: 视频持续时间，默认持续 5 * 60 秒
        :param timeout: 超时断开连接，设定时间，默认5s,单位为微妙级
        :param kwargs:
        """
        sub_shell = ''
        if 'rtsp_transport' in kwargs:
            sub_shell = '-rtsp_transport {} '.format(kwargs.pop('rtsp_transport'))
        if 'stimeout' in kwargs:
            sub_shell += '-stimeout {} '.format(kwargs.pop('stimeout'))
        else:
            sub_shell += '-rw_timeout {} '.format(timeout)

        super(FfmpegRecordThread, self).__init__(**kwargs)

        self.create_time = datetime.now()
        self.name = name
        self.stream_url = stream_url
        self.out_file_path = out_file_path
        self.out_file_dir = os.path.split(out_file_path)[0]
        self.video_duration = video_duration
        self.file_name_out_list = os.path.join(self.out_file_dir, name + '.txt')

        self.shell_cmd_mp4 = (
            'ffmpeg '
            '-y '                                       # 覆盖输出文件
            '-v info '
            '-rtbufsize 1m '
            '{sub_shell}'                               # 超时断开连接，设定是5s
            '-i "{stream_url}" '                        # 输入视频文件或流等其他
            '-movflags faststart '                      # 使mp4支持渐进式下载
            '-c:v copy '                                # 原始编解码数据必须被拷贝
            '-c:a copy '                                # 设定声音编码，降低CPU使用
            '-f segment '                               # 输出流切片
            '-segment_format mp4 '                      # 流输出格式
            '-strftime 1 '                              # 设置切片名为生成切片的时间点
            '-segment_time {segment_time} '             # 流切分时长
            '-reset_timestamps 1 '                      # 每个切片都重新初始化时间戳
            '-segment_list "{file_name_out_list}" '     # 切片列表主文件名，输入是在文件写入完成之后
            '-segment_list_size 10 '                    # 列表文件长度
            '-segment_list_entry_prefix "{out_path}" '  # 写文件列表时写入每个切片路径的前置路径

            '"{out_file}" '                             # 输出文件名
        ).format(sub_shell=sub_shell,
                 stream_url=self.stream_url,
                 segment_time=video_duration,
                 file_name_out_list=self.file_name_out_list,
                 out_path=self.out_file_dir + '/',
                 out_file=self.out_file_path)

        os.makedirs(self.out_file_dir, exist_ok=True)
        self.ffmpeg_proc = None
        self.video_resolution = None

    def kill(self):
        try:
            self.ffmpeg_proc.communicate(input='q'.encode(), timeout=2)
        except Exception as e:
            log.debug(e)
            self.ffmpeg_proc.kill()

    def run(self):
        log.debug(self.shell_cmd_mp4)
        self.ffmpeg_proc = subprocess.Popen(
            self.shell_cmd_mp4, shell=True,
            close_fds=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

        # 实时打印ffmpeg日志
        log_buffer = ''
        return_code = self.ffmpeg_proc.poll()
        while return_code is None:
            # 这里会阻塞,所以不用获取所有的日志才返回，获取81个字节就可以返回了！
            line = self.ffmpeg_proc.stdout.readline(81)
            log_buffer += line.decode()
            # 换行打印日志
            if r'\n' in str(line) or r'\r' in str(line):
                if 'Packet mismatch' in log_buffer:
                    self.kill()
                    break

                # 处理日志中\r的超过81字符的日志长度
                log_buffer = log_buffer.split('\r')
                if len(log_buffer) > 1:
                    log_buffer, stdout = '\n'.join(log_buffer[:-1]), log_buffer[-1]
                else:
                    log_buffer = ''.join(log_buffer)
                    stdout = ''

                # 通过日志获取分辨率
                resolution = re.findall(r'(\d{3,4}x\d{3,4}),', log_buffer)
                if resolution:
                    self.video_resolution = resolution[0]

                log.debug('%s:%s', self.name, log_buffer.strip())
                log_buffer = stdout

            return_code = self.ffmpeg_proc.poll()
        log.debug('%s:%s', self.name, log_buffer.strip())

        self.ffmpeg_proc.kill()
        log.info('{}的ffmpeg exit.'.format(self.name))
