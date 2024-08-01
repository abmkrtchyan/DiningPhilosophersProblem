import logging
import os
import random
import threading
import time

main_file_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(main_file_directory, "philosophers.log")
logging.basicConfig(level=logging.INFO, format='%(message)s', filename=log_file_path)
logger = logging.getLogger(__name__)

NUM_PHILOSOPHERS = 5
FORKS = {i: threading.Lock() for i in range(NUM_PHILOSOPHERS)}


class Philosopher(threading.Thread):
    def __init__(self, philosopher_id, left, right):
        super(Philosopher, self).__init__()
        self.id = philosopher_id
        self.left_fork = left
        self.right_fork = right

    def run(self):
        while True:
            self.think()
            self.get_forks()
            self.eat()
            self.put_forks()

    def think(self):
        logger.info(f"Philosopher {self.id} is thinking")
        time.sleep(random.random())

    def get_forks(self):
        lowest_fork_id, highest_fork_id = sorted([self.left_fork, self.right_fork])

        FORKS[lowest_fork_id].acquire()
        logger.info(f"Philosopher {self.id} picks up lowest fork {lowest_fork_id}")
        FORKS[highest_fork_id].acquire()
        logger.info(f"Philosopher {self.id} picks up highest fork {highest_fork_id}")

    def eat(self):
        logger.info(f"Philosopher {self.id} is eating")
        time.sleep(random.random())

    def put_forks(self):
        lowest_fork_id, highest_fork_id = sorted([self.left_fork, self.right_fork])

        FORKS[lowest_fork_id].release()
        logger.info(f"Philosopher {self.id} puts down lowest fork {lowest_fork_id}")
        FORKS[highest_fork_id].release()
        logger.info(f"Philosopher {self.id} puts down highest fork {highest_fork_id}")


philosophers = []
for i in range(NUM_PHILOSOPHERS):
    left_fork = i
    right_fork = (i + 1) % NUM_PHILOSOPHERS
    philosopher = Philosopher(i, left_fork, right_fork)
    philosophers.append(philosopher)
    philosopher.start()

for philosopher in philosophers:
    philosopher.join()
