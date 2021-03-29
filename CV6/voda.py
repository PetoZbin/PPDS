from fei.ppds import Semaphore, Thread, Mutex, print
from time import sleep


class Shared:

    def __init__(self):

        self.molecules_formed = 0
        self.actual_molecule_bonds = 0  # naratava do 3 vazieb pre molekulu

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


def oxygen(shared):     # kod hydrogen a oxygen na zaklade prednasky

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
    bond(shared)

    shared.barrier.wait()
    shared.mutex.unlock()


def hydrogen(shared):

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
    bond(shared)

    shared.barrier.wait()


def bond(shared):

    pass


if __name__ == '__main__':

    shared = Shared()
