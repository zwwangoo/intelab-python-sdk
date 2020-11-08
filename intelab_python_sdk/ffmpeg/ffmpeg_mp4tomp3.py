from . import run_shell


def ffmpeg_mp4tomp3(mp4_file, output_file):
    """
    mp4视频文件转mp3音频文件
    """
    shell_cmd = (
        'ffmpeg '
        '-y '
        '-i {} '
        '-vn '
        '-f mp3 '
        '{}'
    ).format(mp4_file, output_file)
    run_shell(shell_cmd, name='ffmpeg_mp4tomp3')
    return output_file
