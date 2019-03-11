import multiprocessing
import os
import psutil
import threading
import time


def benchmark():
    a = 1000000000 ** 1000000


def get_proc_info():
    while status:
        for i_proc in process_list:
            py = psutil.Process(i_proc.pid)  # proc info by id
            memory_use = py.memory_info()
            print('memory use:', float(memory_use.rss) / 10 ** 6, " id:", i_proc.pid)
        print("-------------------------")
        time.sleep(1)


if __name__ == '__main__':
    process_list = []
    status = True

    for i in range(2):
        proc = multiprocessing.Process(target=benchmark, args=())
        process_list.append(proc)
        proc.start()

    thread_info = threading.Thread(target=get_proc_info, args=())
    thread_info.start()

    for proc in process_list:
        proc.join()

    status = False
    print("Done!")
