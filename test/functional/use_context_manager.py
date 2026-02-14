"""
Check that is a file is opened without using a context manager, a refactor message is triggered.
Same thing for threading locks.
"""
import threading

with open('afile.txt') as af:  #@
    pass

f = open('afile.txt')  #@

lock = threading.RLock()  #@
with lock:  #@
    do_something()
lock.acquire()  #@
lock.release()  #@

lock = threading.Lock()  #@
lock.acquire()  #@

lock = threading.Semaphore()  #@
lock.acquire()  #@
