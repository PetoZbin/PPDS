from fei.ppds import Mutex, Semaphore, Thread
from time import sleep
from random import randint
from matplotlib import pyplot as plt


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

        shared.mutex.lock()             # ide zapisovat, zamkne lock
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

        if shared.finished:  # ak experiment skoncil
            break


def experiment():       # zdrojom je seminar, z neho inspiracia riesenia

    reps = 10
    results = []
    cons_time = 0.0005
    n_consumers = 50
    sleep_time = 0.005       # vnutorny cyklus caka sleep_time a zastavi vlakna

    for prod_time in range(1, 5):
        # menim cas produkcie jednej polozky
        prod_time = prod_time / 100

        for prod in range(1, 30):
            iters_per_second_sum = 0

            for i in range(reps):
                # 10 krat urobim to iste, spriemerujem hodnoty a ulozim

                shared = Shared()
                producers = create_threads(prod, shared, prod_time, producer)
                consumers =
                create_threads(n_consumers, shared, cons_time, consumer)

                sleep(sleep_time)
                shared.finished = True

                shared.producing_done.signal(100)
                shared.consuming_done.signal(100)

                for thread in producers:
                    thread.join()

                for thread in consumers:
                    thread.join()

                items_per_second = shared.items_count / sleep_time
                iters_per_second_sum += items_per_second

            average_ips = iters_per_second_sum / reps
            results.append((prod_time, prod, average_ips))
    plot_graph(results)


def create_threads(num_producers, shared, prod_time, fnc):

    threads = list()

    for i in range(num_producers):
        threads.append(Thread(fnc, shared, i, prod_time))

    return threads


def plot_graph(graph_data):     # funkcia na zaklade seminaru

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    x = [item[0] for item in graph_data]
    y = [item[1] for item in graph_data]
    z = [item[2] for item in graph_data]

    ax.set_xlabel("čas produkcie")
    ax.set_ylabel("počet producentov")
    ax.set_zlabel("počet produktov / sekunda")

    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

    plt.show()


if __name__ == '__main__':
    experiment()
