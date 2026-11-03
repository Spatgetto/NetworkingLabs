import threading

def threading_id():
    print(f"Thread ID: {threading.current_thread().ident}")

def worker(number):
    print(f"Worker number: {number}")
    threading_id()

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
