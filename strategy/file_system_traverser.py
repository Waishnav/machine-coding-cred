from collections.abc import Callable
from typing import Generic, Optional, TypeVar
from collections import deque

from models.file_system_item import FileSystemItem
from models.folder import Folder

T = TypeVar('T')

class FileSystemTraverser(Generic[T]):
    def traverse(self, start_folder: Folder, callback: Callable[[FileSystemItem], Optional[T]]) -> Optional[T]:
        folders = deque([start_folder])
        while folders:
            folder = folders.popleft()
            for item in folder.get_items:
                result = callback(item)
                if result is not None:
                    return result
                if isinstance(item, Folder):
                    folders.append(item)
        return None
