from fei.ppds import Semaphore, Thread, Mutex, print
from time import sleep


class Shared:

    def __init__(self):

        self.molecules_formed = 0
        self.actual_molecule_bonds = 0  # molekula ma mat 3 atomy

        self.oxygens_available = 0
        self.hydrogens_available = 0
        self.oxyQueue = Semaphore(0)  # semafory, kde cakaju kysliky / vodiky
        self.hydroQueue = Semaphore(0)
        self.mutex = Mutex()
        self.barrier = Semaphore(3)
        pass

    def consume_atoms(self):
        self.oxygens_available -= 1
        self.hydrogens_available -= 2


def oxygen(shared, thread_id):

    sleep(0.001)
    shared.mutex.lock()

    shared.oxygens_available += 1

    if shared.hydrogens_available < 2:
        shared.mutex.unlock()
    else:
        shared.consume_atoms()
        shared.oxyQueue.signal()
        shared.hydroQueue.signal(2)

    shared.oxyQueue.wait()
    bond(shared, "kyslik", thread_id)

    shared.barrier.wait()
    shared.mutex.unlock()


def hydrogen(shared, thread_id):

    sleep(0.001)
    shared.mutex.lock()
    shared.hydrogens_available += 1

    if (shared.oxygens_available < 1) or (shared.hydrogens_available < 2):
        shared.mutex.unlock()
    else:
        shared.consume_atoms()
        shared.oxyQueue.signal()
        shared.hydroQueue.signal(2)

    shared.hydroQueue.wait()
    bond(shared, "vodik", thread_id)

    shared.barrier.wait()


def bond(shared, forming_element, thread_id):

    print("Sucastou vazby je vlakno prvku: " +
          str(forming_element) + " id vlakna: " + str(thread_id))
    shared.actual_molecule_bonds += 1

    if shared.actual_molecule_bonds == 3:
        shared.molecules_formed += 1
        print("Molekula vody s poradovym cislom: " +
              str(shared.molecules_formed) + " vytvorena")
        shared.actual_molecule_bonds = 0
        print("\n")


def create_threads(num_threads, shared, fnc):  # vytvor n vlakien

    threads = list()

    for i in range(num_threads):

        threads.append(Thread(fnc, shared, i))

    return threads


if __name__ == '__main__':

    shared = Shared()

    oxygen_threads = create_threads(1000, shared, oxygen)
    hydrogen_threads = create_threads(2000, shared, hydrogen)

    for thread in oxygen_threads:
        thread.join()

    for thread in hydrogen_threads:
        thread.join()
