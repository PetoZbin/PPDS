from fei.ppds import Semaphore, Event, Thread, print
from time import sleep
from random import randint


class Shared:

    def __init__(self, n, implementation):

        self.count = 0
        self.n = n
        self.implementation = implementation
        self.sequence = [0, 1] + [0]*n        
        self.syn_patterns = list()           # zoznam, kde indexu vlakna zodpoveda 1 semafor alebo udalost

        if self.implementation == "events":

            for i in range(n + 2):
                self.syn_patterns.append(Event())

            self.syn_patterns[0].signal()
            self.syn_patterns[1].signal()

        if self.implementation == "semaphores":

            for i in range(n + 2):
                self.syn_patterns.append(Semaphore(0))

            self.syn_patterns[0].signal(1)
            self.syn_patterns[1].signal(2)


def thread_routine(shared, i):

    sleep(randint(0, 10) / 10)

    print("Vlakno pred stretnutim: " + str(i))

    shared.syn_patterns[i+1].wait()
    shared.syn_patterns[i].wait()

    print("Vlakno po stretnuti: " + str(i))

    shared.sequence[i+2] = shared.sequence[i] + shared.sequence[i+1]    # vzorec
    print(shared.sequence)

    if shared.implementation == "semaphores":
        shared.syn_patterns[i+2].signal(2)   # z jedneho cisla  pocitam 2 cisla (prepustit 2 vlakna)

    if shared.implementation == "events":
        shared.syn_patterns[i+2].signal()


if __name__ == '__main__':

    n = 20                         # pocet vlaken
    # zakomentujte jeden z 2 nasledujucich riadkov
    # implementation = "semaphores"
    implementation = "events"

    sh = Shared(n, implementation)  # zdielany objekt
    threads = list()
    for i in range(n):              # zoznam vlaken

        threads.append(Thread(thread_routine, sh, i))

    for t in threads:
        t.join()
    print("Vysledna postupnost")
    print(sh.sequence)