from abc import ABC, abstractmethod
from utils.read_writer_lock import ReaderWriterLock

class FileSystemItem(ABC):
    def __init__(self, name):
        self.__name = name
        self.rw_lock = ReaderWriterLock()

    @property
    def get_name(self):
        return self.__name

