from abc import ABC, abstractmethod
import threading

class ReaderWriterLock:
    def __init__(self):
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.reader_count = 0

    def acquire_read(self):
        with self.read_lock:
            self.reader_count += 1
            if self.reader_count == 1:
                self.write_lock.acquire() # first reader should acquire write lock so writer is blocked

    def release_read(self):
        with self.read_lock:
            self.reader_count -= 1
            if self.reader_count == 0: # last reader should release write lock so writer can acquire it
                self.write_lock.release()

    def acquire_write(self):
        self.write_lock.acquire()

    def release_write(self):
        self.write_lock.release()

