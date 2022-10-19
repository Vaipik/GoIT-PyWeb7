import concurrent.futures
import logging
from multiprocessing import Process, Queue, JoinableQueue, Manager, Pool
from random import randint
from time import time, sleep
from typing import List
import sys

from logger import logged


NUMBERS = [randint(1, 1000000) for _ in range(400)]


@logged(message='[max number]')
def factorize_max(number):
    return [num for num in range(1, number + 1) if number % num == 0]


@logged(message='[sync]')
def factorize_sync(*number) -> List[List[int]]:
    return [[i for i in range(1, arg + 1) if arg % i == 0] for arg in number]


manager_dict = Manager().dict()


@logged(message='[multipocessing manager outside factorize]')
def factorize_man_out(*number):

    def slave(num: int, mng_dict):

        mng_dict[num] = [i for i in range(1, num + 1) if num % i == 0]
        sys.exit(0)

    workers = [Process(target=slave, args=(num, manager_dict)) for num in number]
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]

    return dict(manager_dict).values()  # !!!!!! dict(manager_dict) !!!!!!


@logged(message='[multipocessing manager inside factorize]')
def factorize_man_in(*number):

    mng_dict = Manager().dict()

    def slave(num: int):

        mng_dict[num] = [i for i in range(1, num + 1) if num % i == 0]
        sys.exit(0)

    workers = [Process(target=slave, args=(num,)) for num in number]
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]

    return dict(mng_dict).values()  # !!!!!! dict(manager_dict) !!!!!!


@logged(message='[multiprocessing queue]')
def factorize_q(*number):

    queue = Queue()

    def slave(q: Queue):
        num = q.get()
        manager_dict[num] = [i for i in range(1, num + 1) if num % i == 0]
        sys.exit(0)

    workers = [Process(target=slave, args=(queue, )) for _ in number]
    [worker.start() for worker in workers]
    [queue.put(num) for num in number]
    [worker.join() for worker in workers]

    return dict(manager_dict).values()


@logged(message='[multiprocessing joinable queue]')
def factorize_jq(*number):

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


def factorize(number) -> List[int]:
    return [i for i in range(1, number + 1) if number % i == 0]


if __name__ == '__main__':

    factorize_max(max(NUMBERS))
    sleep(1)

    factorize_sync(*NUMBERS)
    sleep(1)

    factorize_man_out(*NUMBERS)
    sleep(1)

    factorize_man_in(*NUMBERS)
    sleep(1)

    factorize_q(*NUMBERS)
    sleep(1)

    factorize_jq(*NUMBERS)
    sleep(1)

    start_time = time()
    pool = Pool(processes=4)

    pool.map(factorize, NUMBERS)
    logging.log(level=logging.DEBUG, msg=f"[multiprocessing pool] done in {time() - start_time}")
    sleep(1)

    start_time = time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(factorize, NUMBERS)
    logging.log(level=logging.DEBUG, msg=f"[multiprocessing PoolExecutor] done in {time() - start_time}")
