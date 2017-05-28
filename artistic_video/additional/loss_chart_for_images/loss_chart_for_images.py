import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def read_content(file_name):
    with open(file_name, 'r') as file:
        content = file.readline()
        content = content.split()
        return np.array(content)


def draw_chart():
    buf1 = read_content('losses_1.txt')
    buf10 = read_content('losses_10.txt')
    buf20 = read_content('losses_20.txt')

    fig = plt.figure()
    sub_plot = fig.add_subplot(111)
    sub_plot.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))

    plt.title("Total loss values")
    plt.plot(buf1, label='learning rate: 1.0')
    plt.plot(buf10, label='learning rate: 10.0')
    plt.plot(buf20, label='learning rate: 20.0')
    sub_plot.legend(loc='upper right', shadow=True)
    plt.grid(True)
    plt.ylabel("Error value")
    plt.xlabel("Iterations")
    plt.show()
    fig.savefig('total_loss_values')

if __name__ == '__main__':
    draw_chart()