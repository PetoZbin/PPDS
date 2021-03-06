from fei.ppds import Thread, Mutex


class Shared:

    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * self.end     # nulove pole velkosti end, cize velkost pola
        self.mutex = Mutex()


class Histogram:

    def __init__(self, elms):

        self.dict = {}      # python slovnik key:value

        for item in elms:

            if item in self.dict:
                self.dict[item] = self.dict[item] + 1
            else:
                self.dict[item] = 1


def fnc_counter(sh):

    while True:

        if sh.counter >= sh.end: 
            break

        sh.elms[sh.counter] += 1       # jedno vlakno preplanuje planovac, druhe mu zvysi counter
        sh.mutex.lock()
        sh.counter += 1                 
        sh.mutex.unlock()


for i in range(100):

    shared = Shared(100000)     # parameter - velkost pola

    t1 = Thread(fnc_counter, shared)     # adresa funkcie, argument
    t2 = Thread(fnc_counter, shared)

    t1.join()
    t2.join()

    print(Histogram(shared.elms).dict)
