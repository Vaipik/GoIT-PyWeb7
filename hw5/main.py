import concurrent.futures
from multiprocessing import Process, JoinableQueue, Manager, Pool
from time import sleep
from typing import List
import sys

from logger import logged


@logged(message='[max number]')
def factorize(number):
    return [num for num in range(1, number + 1) if number % num == 0]


a = factorize(10651060)
sleep(1)


@logged(message='[sync]')
def factorize(*number) -> List[List[int]]:
    return [[i for i in range(1, arg + 1) if arg % i == 0] for arg in number]


a, b, c, d = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [
    1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
    380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530,
    10651060
    ]

sleep(1)
manager_dict = Manager().dict()


@logged(message='[multipocessing manager outside factorize]')
def factorize(*number):

    def slave(num: int, mng_dict):

        mng_dict[num] = [i for i in range(1, num + 1) if num % i == 0]
        sys.exit(0)

    workers = [Process(target=slave, args=(num, manager_dict)) for num in number]
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]

    return dict(manager_dict).values()  # !!!!!! dict(manager_dict) !!!!!!


a, b, c, d = factorize(128, 255, 99999, 10651060)
sleep(1)


@logged(message='[multipocessing manager inside factorize]')
def factorize(*number):

    mng_dict = Manager().dict()

    def slave(num: int):

        mng_dict[num] = [i for i in range(1, num + 1) if num % i == 0]
        sys.exit(0)

    workers = [Process(target=slave, args=(num,)) for num in number]
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]

    return dict(mng_dict).values()  # !!!!!! dict(manager_dict) !!!!!!


a, b, c, d = factorize(128, 255, 99999, 10651060)
sleep(1)
assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [
    1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
    380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530,
    10651060
    ]


@logged(message='[multiprocessing joinable queue]')
def factorize(*number):

    queue = JoinableQueue()

    def slave(q: JoinableQueue):
        num = q.get()
        manager_dict[num] = [i for i in range(1, num + 1) if num % i == 0]
        q.task_done()
        sys.exit(0)

    [Process(target=slave, args=(queue, )).start() for _ in number]
    [queue.put(num) for num in number]
    queue.join()
    return dict(manager_dict).values()


factorize(128, 255, 99999, 10651060)
sleep(1)


@logged(message='[multiprocessing with pool]')
def factorize(number) -> List[int]:
    return [i for i in range(1, number + 1) if number % i == 0]


pool = Pool(processes=4)

a, b, c, d = pool.map(factorize, [128, 255, 99999, 10651060])
sleep(1)
assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [
    1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
    380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530,
    10651060
    ]

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    a, b, c, d = executor.map(factorize, [128, 255, 99999, 10651060])
