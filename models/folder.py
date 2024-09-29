from models.file_system_item import FileSystemItem
from typing import Optional, List

class Folder(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)
        self.__items = []

    @property
    def get_items(self) -> List[FileSystemItem]:
        return self.__items

    def add_item(self, item: FileSystemItem) -> None:
        if self.get_item(item.get_name) is not None:
            return
        self.__items.append(item)

    def remove_item(self, item: FileSystemItem) -> None:
        self.__items.remove(item)

    def get_item(self, name: str) -> Optional[FileSystemItem]:
        for item in self.__items:
            if item.get_name == name:
                return item
        return None
