import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

seconds_opt_flow = [3.700949, 71.693549, 75.388477, 186.4160516,
           371.140060, 466.996901, 481.256280]
seconds_frame = [23.126104, 82.640347, 93.487573, 127.973041, 203.892024, 245.769916, 279.945757]
x = [0, 1, 2, 3, 4, 5, 6]
resolutions = ['320*240', '640*480', '720*480', '800*600', '1024*768', '1280*720', '1366*768']


def draw_opt_flow_time_chart():
    fig = plt.figure()
    sub_plot = fig.add_subplot(111)
    plt.title("Deepmatching - deepflow time")
    plt.plot(seconds_opt_flow, marker='o', color='b')
    plt.xticks(x, resolutions, rotation='vertical')
    sub_plot.legend(loc='upper right', shadow=True)
    plt.grid(True)
    plt.ylabel("Time(sec.)")
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.xlabel("Resolution(pixels)")
    plt.show()
    fig.savefig('deepmatching_deeplfow')


def one_min_video_opt_flow():
    fps = 24
    video_lenght = 60 #1 minute video
    frame_count = fps * video_lenght
    one_minute_video = []
    for sec_opt, sec_fr in zip(seconds_opt_flow, seconds_frame):
        one_minute_video.append((frame_count - 1) * (sec_opt + sec_fr) / video_lenght)

    print(one_minute_video)
    fig = plt.figure()
    sub_plot = fig.add_subplot(111)
    plt.title("Stylizing 1 minute video")
    plt.plot(one_minute_video, marker='o', color='b')
    plt.xticks(x, resolutions, rotation='vertical')
    sub_plot.legend(loc='upper right', shadow=True)
    plt.grid(True)
    plt.ylabel("Time(minutes)")
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.xlabel("Resolution(pixels)")
    plt.show()
    fig.savefig('one_min_video_opt_flow')


def one_min_video():
    fps = 24
    video_lenght = 60 # 1 minute video
    frame_count = fps * video_lenght
    one_minute_video = []
    for sec_fr in seconds_frame:
        one_minute_video.append((frame_count * sec_fr) / video_lenght)

    print(one_minute_video)
    fig = plt.figure()
    sub_plot = fig.add_subplot(111)
    plt.title("Stylizing 1 minute video")
    plt.plot(one_minute_video, marker='o', color='b')
    plt.xticks(x, resolutions, rotation='vertical')
    sub_plot.legend(loc='upper right', shadow=True)
    plt.grid(True)
    plt.ylabel("Time(minutes)")
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.xlabel("Resolution(pixels)")
    plt.show()
    fig.savefig('one_min_video')


if __name__ == '__main__':
    # draw_opt_flow_time_chart()
    one_min_video_opt_flow()
    one_min_video()