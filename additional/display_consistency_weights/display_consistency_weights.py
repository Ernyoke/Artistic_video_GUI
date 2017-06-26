import numpy as np
import scipy.misc


def read_consistency_file(path):
    with open(path) as f:
        lines = f.readlines()
        width, height = [int(i) for i in lines[0].split(' ')]
        values = np.zeros((height, width), dtype=np.float32)
        for i in range(0, len(lines) - 1):
            line = lines[i + 1].rstrip().split(' ')
            consistency_values = np.array([np.float32(j) for j in line])

            def convert(value):
                return value

            values[i] = list(map(convert, consistency_values))

        # expand to 3 channels
        weights = np.dstack([values.astype(np.float32)] * 3)

    return weights


def save_flow(flow, output_path):
    scipy.misc.imsave(output_path, flow)


if __name__ == '__main__':
    forward = read_consistency_file('input_frame00001_input_frame00002_forward_reliable.txt')
    backward = read_consistency_file('input_frame00001_input_frame00002_backward_reliable.txt')
    save_flow(forward, 'forward.jpg')
    save_flow(backward, 'backward.jpg')
