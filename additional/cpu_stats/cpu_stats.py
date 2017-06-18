import matplotlib.pyplot as plt


def cpu_vs_gpu_chart():
    cpu_seconds = [862.980290, 6 * 581.321981, 6 * 907.808317, 6 * 1489.300687]
    gpu_seconds = [23.126104, 82.640347, 127.973041, 203.892024]
    x = [0, 1, 2, 3]
    resolutions = ['320*240', '640*480', '800*600', '1024*768']

    fig = plt.figure()
    sub_plot = fig.add_subplot(111)

    plt.title("Rendering time on CPU vs GPU")
    plt.plot(gpu_seconds, marker='o', color='b', label='GPU')
    plt.plot(cpu_seconds, marker='o', color='r', label='CPU')
    plt.xticks(x, resolutions, rotation='vertical')
    sub_plot.legend(loc='upper left', shadow=True)
    plt.grid(True)
    plt.ylabel("Time(sec.)")
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.xlabel("Resolution(pixels)")
    plt.show()
    fig.savefig('cpu_vs_gpu')


def draw_speedup():
    speedup = [862.980290 / 23.126104, 6 * 581.321981 / 82.640347,
                6 * 907.808317 / 127.973041, 6 * 1489.300687 / 203.892024]
    x = [0, 1, 2, 3]
    resolutions = ['320*240', '640*480', '800*600', '1024*768']

    fig = plt.figure()
    sub_plot = fig.add_subplot(111)

    plt.title("Speedup")
    plt.plot(speedup, marker='o', color='b')
    plt.xticks(x, resolutions, rotation='vertical')
    sub_plot.legend(loc='upper left', shadow=True)
    plt.ylim([30, 50])
    plt.grid(True)
    plt.ylabel("CPU time / GPU time")
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.xlabel("Resolution(pixels)")
    plt.show()
    fig.savefig('speedup')


if __name__ == '__main__':
    # cpu_vs_gpu_chart()
    draw_speedup()