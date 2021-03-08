from fei.ppds import Mutex, Semaphore
from time import sleep
from random import randint


class Shared:

    def __init__(self):

        self.mutex = Mutex()
        self.items_count = 0
        self.producing_done = Semaphore(0)
        self.consuming_done = Semaphore(10)
        self.finished = False


def produce(prod_time):

    sleep(prod_time)  # cas produkcie
    item = randint(1, 100)  # vyprodukuje polozku
    return item


def consume(shared, consume_time):

    sleep(consume_time)  # cas produkcie
    item = 5
    return item


def producer(shared, th_id, prod_time):

    while True:

        item = produce(prod_time)
        shared.consuming_done.wait()

        shared.mutex.lock()
        shared.items_count += 1
        shared.mutex.unlock()

        shared.producing_done.signal()

        if shared.finished:  # ak experiment skoncil
            break


def consumer(shared, th_id, consume_time):

    while True:

        shared.producing_done.wait()
        shared.mutex.lock()
        item = consume(shared, consume_time)
        shared.mutex.unlock()
        shared.consuming_done.signal()

        if shared.finished:
            break
