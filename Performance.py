import time
from memory_profiler import memory_usage
import os
import psutil
import threading
from typing import Callable
import tracemalloc

global start_time
global end_time

def start_time() -> float:
    return time.time()

def end_time() -> float:
    return time.time()
     

def show_time_differrence() -> None:
    difference = end_time() - start_time()
    print(f"Runtime: {difference:10f} Seconds")

def monitor_memory_usage(method, arguments) -> list:
    process = psutil.Process(os.getpid())
    #memory_use = memory_usage((method, (arguments)))
    tracemalloc.start()
    start_mem = process.memory_info().rss / (1024 * 1024)  # MB

    # Run the function and monitor memory
    method(*arguments)

    # Check peak memory during execution
    current_mem = process.memory_info().rss / (1024 * 1024)
    peak = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()

    memory_usage_samples = [start_mem, max(start_mem, peak, current_mem), current_mem]

    print(f"Memory Usage: {memory_usage_samples} MB")
    # print(f"Memory Usage: {memory_use} \n")
    # print("Starting memory:", memory_use[0], "MB \n")
    # print("Maximum usage:", max(memory_use), "MB \n")
    # print("Final usage:", memory_use[-1], "MB \n")

    return memory_usage_samples


def measure_cpu_usage() -> list:
    pid = os.getpid()
    process = psutil.Process(pid)

    cpu_percentages = []

    for _ in range (20):
        cpu = process.cpu_percent(interval=0.02)
        cpu_percentages.append(cpu)
    
    return cpu_percentages

def show_cpu_usage(method: Callable, arguments: list) -> list:
    cpu_data = []
    monitor= threading.Thread(target=lambda: cpu_data.extend(measure_cpu_usage()))
    monitor.start()
    method(*arguments)
    monitor.join()
    print(f"CPU usage samples: {cpu_data}")
    print(f"Average CPU usage: {sum(cpu_data) / len(cpu_data):.2f}%")
    return cpu_data