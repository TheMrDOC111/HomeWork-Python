import multiprocessing
import os
import sys
import psutil
import threading
import time
from multiprocessing import Queue

class ProcessPool:
    def __init__(self, min_workers=2, max_workers=10, mem_usage=1024):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage

    def get_proc_info(self):
        global vertex_memory
        while self.status:
            for worker in self.workers:
                py = psutil.Process(worker.pid)  # proc info by id
                memory_use = py.memory_info()
                if float(memory_use.rss / 10 ** 6) > vertex_memory:
                    vertex_memory = float(memory_use.rss / 10 ** 6)
                print('memory use:', float(memory_use.rss) / 10 ** 6, " id:", worker.pid)
            print("-------------------------")
            time.sleep(1)

    def map(self, function, big_data):
        queue = Queue()
        global vertex_memory
        self.workers = []
        self.status = True
        self.workers_usage = 0
        vertex_memory = 0
        self.test_computation(function, big_data, queue)
        """for i in range(self.workers_usage):
            self.workers.append(self.worker_init(function, big_data))"""
        return [queue.get() for i in range(queue.qsize())]

    def worker_func(self, function, big_data, queue):
        while len(big_data) > 0:
            queue.put(function(big_data.pop(0)))

    def worker_init(self, function, big_data, queue):
        worker = multiprocessing.Process(target=self.worker_func, args=(function, big_data, queue))
        self.workers.append(worker)
        worker.start()
        return worker

    def value_workers(self, n_proc):
        if n_proc in range(self.min_workers, self.max_workers):
            return n_proc
        elif n_proc < self.min_workers:
            return self.min_workers
        else:
            return self.max_workers

    def test_computation(self, function, data_chunk, queue):
        worker_first = self.worker_init(function, data_chunk, queue)
        thread_info = threading.Thread(target=self.get_proc_info, args=())
        thread_info.start()
        worker_first.join()
        self.status = False
        self.workers_usage = self.value_workers(int(self.mem_usage / vertex_memory))

        """for i in range(n_proc):  # вот тут пока осторожно(возможно -cpu)
            proc = multiprocessing.Process(target=self.benchmark, args=())
            self.process_list.append(proc)
            proc.start()

        thread_info = threading.Thread(target=self.get_proc_info, args=())
        thread_info.start()"""

        for worker in self.workers:
            worker.join()
        print("DONE!", "vertex_memory:", vertex_memory, "workers_usage:", self.workers_usage)
