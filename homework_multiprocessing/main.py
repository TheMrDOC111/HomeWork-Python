import multiprocessing
import os
import sys
import psutil
import threading
import time
import process_pool
from multiprocessing.pool import ThreadPool



def benchmark(data_chunk):
    a = 1000000000 ** data_chunk
    return a


if __name__ == '__main__':
    pool = process_pool.ProcessPool()
    results = pool.map(benchmark, [1230000, 4560000, 78900000, 10, 123000, 123000, 102030, 102030])
    print(results)
