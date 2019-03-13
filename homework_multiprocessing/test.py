from multiprocessing import Process, Queue
import time
import os


def worker_func(function, input_queue, output_queue):
    while input_queue.qsize() > 0:
        print(os.getpid())
        output_queue.put(function(input_queue.get()))


def benchmark(data_chunk):
    a = 1000000000 ** data_chunk
    return a


def map(function, big_data):
    output_queue = Queue()
    input_queue = Queue()
    for i in big_data:
        input_queue.put(i)
    workers_usage = 8
    workers = []

    for i in range(workers_usage):
        worker = Process(target=worker_func, args=(function, input_queue, output_queue))
        worker.start()
        workers.append(worker)
    print("!!!")

    for worker in workers:
        print(worker)
        worker.join()
    print("!!!")

    return [output_queue.get() for i in range(output_queue.qsize())]


if __name__ == '__main__':
    start_time = time.perf_counter()
    results = map(benchmark, [1230, 4560, 789000, 10, 1230, 123, 130, 30])
    print(time.process_time() - start_time)
    print(results)
