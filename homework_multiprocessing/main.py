import multiprocessing
import os
import sys
import psutil
import threading
import time


def benchmark():
    a = 1000000000 ** 100000000000000


def get_proc_info():
    global peak_memory
    while status:
        for i_proc in process_list:
            py = psutil.Process(i_proc.pid)  # proc info by id
            memory_use = py.memory_info()
            if float(memory_use.rss / 10 ** 6) > peak_memory:
                peak_memory = float(memory_use.rss / 10 ** 6)
            print('memory use:', float(memory_use.rss) / 10 ** 6, " id:", i_proc.pid)
        print("-------------------------")
        time.sleep(1)


if __name__ == '__main__':
    process_list = []
    status = True
    your_memory = 8192
    can_use_memory = your_memory / 2
    peak_memory = 0

    proc_first = multiprocessing.Process(target=benchmark, args=())
    process_list.append(proc_first)
    proc_first.start()

    thread_info = threading.Thread(target=get_proc_info, args=())
    thread_info.start()

    proc_first.join()
    process_list.clear()

    n_proc = int(can_use_memory / peak_memory)

    for i in range(n_proc):  # вот тут пока осторожно(возможно -cpu)
        proc = multiprocessing.Process(target=benchmark, args=())
        process_list.append(proc)
        proc.start()

    thread_info = threading.Thread(target=get_proc_info, args=())
    thread_info.start()

    for proc in process_list:
        proc.join()
    print("DONE!", "peak_memory:", peak_memory, "n_proc:", n_proc)
    sys.exit(0)
