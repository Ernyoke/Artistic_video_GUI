#!/usr/bin/python3

import gpustat
import time

def log_stats():
    usage = []
    memory = []
    print("GPU usage monitor running. Press Ctrl + C for stopping")
    while True:
        try:
            all_gpu_stats = gpustat.GPUStatCollection.new_query()
            for g in all_gpu_stats:
                usage.append(g.utilization)
                memory.append(g.memory_used)
            time.sleep(1)  # sleep for 1 second
        except KeyboardInterrupt:
            with open('gpu_stats.txt', 'w') as file:
                for u in usage:
                    file.write(str(u) + " ")
                file.write('\n')
                for m in memory:
                    file.write(str(m) + " ")
            return


if __name__ == '__main__':
    log_stats()