import cProfile
import threading
import time
from multiprocessing import Process

# 模拟 I/O 绑定任务（如 CAN 通信）
def io_bound_task(task_id):
    print(f"Task {task_id} started")
    for _ in range(1000):
        # 模拟 I/O 等待（如 CAN 数据接收）
        time.sleep(0.001)
    print(f"Task {task_id} finished")

# 模拟 CPU 密集型任务
def cpu_bound_task(task_id):
    print(f"Task {task_id} started")
    for _ in range(1000000):
        a = 1 + 1  # 简单计算
    print(f"Task {task_id} finished")

# 启动多线程任务（I/O 绑定）
def run_io_tasks():
    threads = []
    for i in range(10):  # 创建 10 个线程
        thread = threading.Thread(target=io_bound_task, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

# 启动多线程任务（CPU 密集型）
def run_cpu_tasks_threading():
    threads = []
    for i in range(10):  # 创建 10 个线程
        thread = threading.Thread(target=cpu_bound_task, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

# 启动多进程任务（CPU 密集型）
def run_cpu_tasks_multiprocessing():
    processes = []
    for i in range(10):  # 创建 10 个进程
        process = Process(target=cpu_bound_task, args=(i,))
        processes.append(process)
        process.start()

    # 等待所有进程完成
    for process in processes:
        process.join()

# 使用 cProfile 进行性能分析
if __name__ == "__main__":
    print("=== Testing I/O Bound Tasks (Multi-threading) ===")
    cProfile.run('run_io_tasks()', sort='time')

    print("\n=== Testing CPU Bound Tasks (Multi-threading) ===")
    cProfile.run('run_cpu_tasks_threading()', sort='time')

    print("\n=== Testing CPU Bound Tasks (Multi-processing) ===")
    cProfile.run('run_cpu_tasks_multiprocessing()', sort='time')

