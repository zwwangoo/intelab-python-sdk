import cv2
import time
import numpy as np
import subprocess


def read_to_frames(video_file, hight, width, start_time='00:00:00'):
    process = subprocess.Popen([
        'ffmpeg', '-v', 'error',
        '-ss', start_time,
        '-i', video_file,
        '-an',
        '-f', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-r', '1',  # 跳秒
        '-vframes', '1',  # 取10帧
        '-'
    ], stdout=subprocess.PIPE, stdin=None)

    t = time.time()
    return_code = process.poll()
    frames = []
    # TODO 这里有优化
    while not return_code:
        raw_image = process.stdout.read(width*hight*3)
        if not raw_image:
            break

        process.stdout.flush()
        frame_array = np.fromstring(raw_image, dtype='uint8')

        img = frame_array.reshape((hight, width, 3))
        frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        frames.append(frame)

        return_code = process.poll()

    print(time.time() - t)
    return frames


if __name__ == '__main__':
    a = read_to_frames('/tmp/videos/D86639983/D86639983_2021-08-12_13-45-42.mp4', 720, 1280)
    # cv2.imshow('a', a[0])
    # cv2.waitKey()
