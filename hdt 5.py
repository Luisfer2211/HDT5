import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 42py -3.11 -m pip install simpy
random.seed(RANDOM_SEED)

# Parámetros de la simulación
RAM_CAPACITY = 100
CPU_SPEED = 3

class Process:
    def __init__(self, env, name, ram, cpu):
        self.env = env
        self.name = name
        self.ram_required = random.randint(1, 10)
        self.instructions = random.randint(1, 10)
        self.cpu = cpu
        self.ram = ram
        self.start_time = env.now
        self.action = env.process(self.run())

    def run(self):
        yield self.env.process(self.new())
        yield self.env.process(self.ready())
        yield self.env.process(self.running())
        yield self.env.process(self.terminated())

    def new(self):
        yield self.ram.get(self.ram_required)

    def ready(self):
        pass

    def running(self):
        for _ in range(self.instructions // CPU_SPEED):
            yield self.env.timeout(1)
            self.instructions -= CPU_SPEED
        if self.instructions > 0:
            if random.randint(1, 2) == 1:
                yield self.env.process(self.waiting())
            else:
                yield self.env.process(self.ready())
        else:
            yield self.env.timeout(0)

    def waiting(self):
        yield self.env.timeout(random.expovariate(1.0 / INTERVAL))

    def terminated(self):
        self.ram.put(self.ram_required)
        process_times.append(self.env.now - self.start_time)

def process_generator(env, ram, cpu, num_processes, interval):
    for i in range(num_processes):
        yield env.timeout(random.expovariate(1.0 / interval))
        env.process(Process(env, f'Proceso {i}', ram, cpu))

process_counts = [25, 50, 100, 150, 200]
intervals = [10, 5, 1]
average_times = []

for interval in intervals:
    for count in process_counts:
        process_times = []
        env = simpy.Environment()
        ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
        cpu = simpy.Resource(env, capacity=1)
        env.process(process_generator(env, ram, cpu, count, interval))
        env.run()
        average_times.append(np.mean(process_times))

    plt.plot(process_counts, average_times)
    plt.xlabel('Número de procesos')
    plt.ylabel('Tiempo promedio')
    plt.title(f'Tiempo promedio por número de procesos con intervalo {interval}')
    plt.show()
