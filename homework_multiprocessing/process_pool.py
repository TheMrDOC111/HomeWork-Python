import multiprocessing
import os
import psutil
import threading
import time
from multiprocessing import Queue


class ProcessPool:
    def __init__(self, min_workers=2, max_workers=10, mem_usage=512):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.output_queue = Queue()
        self.input_queue = Queue()
        self.workers = []
        self.status = True
        self.workers_usage = 0
        self.vertex_memory = 0

    def get_proc_info(self):
        while self.status:
            for worker in self.workers:
                try:
                    py = psutil.Process(worker.pid)
                    memory_use = py.memory_info()
                    if float(memory_use.rss / 2 ** 20) > self.vertex_memory:
                        self.vertex_memory = float(memory_use.rss / 2 ** 20)
                    print('memory use:', float(memory_use.rss) / 2 ** 20, " id:", worker.pid)
                except Exception:
                    pass
            print("-------------------------")
            time.sleep(1)

    def map(self, function, big_data):

        for i in big_data:
            self.input_queue.put(i)

        self.test_computation(function, self.input_queue, self.output_queue)

        for i in range(self.workers_usage):
            self.worker_init(function, self.input_queue, self.output_queue)

        for worker in self.workers:
            worker.join()

        self.status = False

        return [self.output_queue.get() for i in range(self.output_queue.qsize())]

    def worker_init(self, function, input_queue: Queue, output_queue: Queue):
        worker = multiprocessing.Process(target=worker_func, args=(function, input_queue, output_queue))
        self.workers.append(worker)
        worker.start()
        return worker

    def value_workers(self, n_proc: int):
        if n_proc in range(self.min_workers, self.max_workers):
            return n_proc
        elif n_proc < self.min_workers:
            return self.min_workers
        else:
            return self.max_workers

    def test_computation(self, function, input_queue: Queue, output_queue: Queue):
        worker_first = multiprocessing.Process(target=test_worker_func, args=(function, input_queue, output_queue))
        self.workers.append(worker_first)
        thread_info = threading.Thread(target=self.get_proc_info, args=())
        worker_first.start()
        thread_info.start()
        worker_first.join()
        self.workers.clear()
        # self.status = False
        self.workers_usage = self.value_workers(int(self.mem_usage / self.vertex_memory))
        print("DONE!", "vertex_memory:", self.vertex_memory, "workers_usage:", self.workers_usage)


def test_worker_func(function, input_queue: Queue, output_queue: Queue):
    value = input_queue.get()
    output_queue.put(function(value) + " by worker id: " + str(os.getpid()))


def worker_func(function, input_queue: Queue, output_queue: Queue):
    while input_queue.qsize() > 0:
        value = input_queue.get()
        output_queue.put(function(value) + " by worker id: " + str(os.getpid()))
