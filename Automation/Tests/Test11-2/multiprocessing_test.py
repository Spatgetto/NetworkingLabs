from multiprocessing import Process
import os

def process_info():
    print(f"Process ID: {os.getpid()}")

def worker(number):
    print(f"Worker number: {number}")
    process_info()

if __name__ == "__main__":
    processes = []
    for i in range(5):
        p = Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

        