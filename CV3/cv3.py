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

        if shared.finished:
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


def experiment():

    reps = 10
    results = []
    cons_time = 0.0005
    n_consumers = 50
    sleep_time = 0.005

    for prod_time in range(1, 5):
        pass
        for prod in range(1, 30):
            pass
            for i in range(reps):
                pass


if __name__ == '__main__':
    experiment()
