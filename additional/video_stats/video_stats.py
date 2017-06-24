import artistic_video.Video as vid
import time
import os


def opt_flow():

    os.chdir('../../')

    pics = [
        './additional/images/redhead_320_240.jpg',
        './additional/images/redhead_640_480.jpg',
        './additional/images/redhead_720_480.jpg',
        './additional/images/redhead_800_600.jpg',
        './additional/images/redhead_1024_768.jpg',
        './additional/images/redhead_1280_720.jpg',
        './additional/images/redhead_1366_768.jpg'
    ]

    elapsed_time = []

    for frame in pics:
        start_time = time.time()
        vid.make_opt_flow(frame, frame, './additional/video_stats/output')
        end_time = time.time()
        elapsed_time.append(end_time - start_time)

    with open('./additional/video_stats/results.txt', 'w') as file:
        for t in elapsed_time:
            file.write(str(t) + " ")


if __name__ == '__main__':
    opt_flow()