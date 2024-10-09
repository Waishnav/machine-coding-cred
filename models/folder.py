from models.file_system_item import FileSystemItem
from typing import Optional, List

class Folder(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)
        self.__items = []

    @property
    def get_items(self) -> List[FileSystemItem]:
        try:
            self.rw_lock.acquire_read()
            return self.__items.copy()           # Return a copy to prevent external modifications
        finally:
            self.rw_lock.release_read()


    def add_item(self, item: FileSystemItem) -> None:
        try:
            self.rw_lock.acquire_write()
            if self._get_item_no_lock(item.get_name) is not None:
                return
            self.__items.append(item)
        finally:
            self.rw_lock.release_write()

    def remove_item(self, item: FileSystemItem) -> None:
        try:
            self.rw_lock.acquire_write()
            self.__items.remove(item)
        finally:
            self.rw_lock.release_write()

    def get_item(self, name: str) -> Optional[FileSystemItem]:
        try:
            self.rw_lock.acquire_read()
            return self._get_item_no_lock(name)
        finally:
            self.rw_lock.release_read()

    # internal method
    def _get_item_no_lock(self, name: str) -> Optional[FileSystemItem]:
        for item in self.__items:
            if item.get_name == name:
                return item
        return None
