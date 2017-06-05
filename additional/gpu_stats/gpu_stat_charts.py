import matplotlib.pyplot as plt


def draw_gpu_usage_chart():
    usage = [0, 0, 3, 1, 1, 5, 92, 100, 96, 100, 99, 99, 99, 99, 99, 100, 100, 99, 99, 99, 99, 100, 99, 99, 99, 100, 100,
             99, 99, 99, 99, 99, 100, 100, 100, 100, 99, 99, 100, 100, 100, 100, 99, 99, 100, 100, 99, 99, 100, 100, 100,
             100, 99, 99, 100, 100, 100, 100, 100, 99, 100, 99, 100, 100, 99, 100, 100, 100, 100, 99, 99, 99, 100, 100,
             99, 100, 99, 99, 100, 100, 100, 99, 99, 99, 100, 100, 53, 0, 1, 0, 0, 0, 1, 0, 0]

    fig = plt.figure()
    sub_plot = fig.add_subplot(111)

    plt.title("GPU usage")
    plt.plot(usage, color='b')
    sub_plot.legend(loc='upper right', shadow=True)
    plt.grid(True)
    plt.ylabel("Usage(%)")
    plt.xlabel("Time(sec.)")
    plt.show()
    fig.savefig('gpu_usage')


def draw_gpu_memory_usage_chart():
    usage = [494, 494, 494, 490, 490, 7779, 7829, 7861, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860,
             7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860,
             7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860,
             7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860,
             7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860, 7860,
             7860, 7860, 7864, 7860, 7860, 7860, 7860, 7860, 7860, 480, 475, 475, 475, 475, 475]

    fig = plt.figure()
    sub_plot = fig.add_subplot(111)

    plt.title("GPU memory usage")
    plt.plot(usage, color='b')
    sub_plot.legend(loc='upper right', shadow=True)
    plt.grid(True)
    plt.ylabel("Memory(MB)")
    plt.xlabel("Time(sec.)")
    plt.show()
    fig.savefig('gpu_memory_usage')


def draw_time_chart():
    seconds = [23.126104, 82.640347, 93.487573, 127.973041, 203.892024, 245.769916, 279.945757]
    x = [0, 1, 2, 3, 4, 5, 6]
    resolutions = ['320*240', '640*480', '720*480', '800*600', '1024*764', '1280*720', '1366*768']

    fig = plt.figure()
    sub_plot = fig.add_subplot(111)

    plt.title("Rendering time")
    plt.plot(seconds, marker='o', color='b')
    plt.xticks(x, resolutions, rotation='vertical')
    sub_plot.legend(loc='upper right', shadow=True)
    plt.grid(True)
    plt.ylabel("Time(sec.)")
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.xlabel("Resolution(pixels)")
    plt.show()
    fig.savefig('time_per_res')


if __name__ == '__main__':
    # draw_time_chart()
    # draw_gpu_usage_chart()
    draw_gpu_memory_usage_chart()