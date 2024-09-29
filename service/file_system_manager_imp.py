from typing import Optional
from models.file_system_item import FileSystemItem
from service.file_system_manager import FileSystemManager
from models.folder import Folder
from models.file import File

from strategy.exact_match_search_strategy import ExactMatchSearchStrategy
from strategy.file_system_traverser import FileSystemTraverser
from strategy.pattern_match_search_strategy import PatternMatchSearchStrategy

class FileSystemManagerImpl(FileSystemManager):
    def __init__(self, root_name):
        self.root = Folder(root_name)
        self.traverser = FileSystemTraverser()

    def _find_folder(self, folder_name: str) -> Optional[Folder]:
        if self.root.get_name == folder_name:
            return self.root
        return self.traverser.traverse(self.root, lambda item: item if isinstance(item, Folder) and item.get_name == folder_name else None)

    def add_file_or_folder(self, parent_folder_name: str, name: str, is_folder: bool) -> bool:
        """
        Adds a file or folder to the system.

        :param parent_folder_name: the name of the parent folder
        :param name:
        :param is_folder:
        """
        parent_folder = self._find_folder(parent_folder_name)
        if parent_folder:
            new_item = Folder(name) if is_folder else File(name)
            parent_folder.add_item(new_item)
            return True
        return False

    def move_file_or_folder(self, source_name: str, destination_folder: str) -> bool:
        """
        Moves a file or folder to a new location.

        :param source_name: the name of the file or folder to move
        :param destination_folder: the name of the destination folder
        """
        final_folder = self._find_folder(destination_folder)
        if not final_folder:
            return False

        def find_and_move(item: FileSystemItem) -> Optional[bool]:
            if item.get_name == source_name:
                parent = self.traverser.traverse(self.root, lambda i: i if isinstance(i, Folder) and item in i.get_items else None)
                if parent:
                    parent.remove_item(item)
                    final_folder.add_item(item)
                    return True
            return None

        return self.traverser.traverse(self.root, find_and_move) or False

    def list_contents(self, folder_name: str) -> list:
        """
        Lists the contents of a specific folder.

        :param folder_name: the name of the folder
        :return: a list of names of files and folders within the specified folder
        """
        folder = self._find_folder(folder_name)
        return [item.get_name for item in folder.get_items] if folder else []

    def list_directory_structure(self) -> list:
        """
        Returns the directory structure of each file and folder in the file system.

        :return: a list representing the directory structure
        """
        def list_directory(folder: Folder, level: int) -> list[str]:
            result = [f"{'  ' * level}+ {folder.get_name}"]
            for item in folder.get_items:
                if isinstance(item, Folder):
                    result.extend(list_directory(item, level + 1))
                else:
                    result.append(f"{'  ' * (level + 1)}- {item.get_name}")
            return result

        return list_directory(self.root, 0)

    def search_file_exact_match(self, folder_name: str, file_name: str) -> Optional[str]:
        """
        Searches for an exact file match within a specific folder.

        :param folder_name: the name of the folder to search within
        :param file_name: the exact name of the file to search for
        :return: the name of the file if found, null otherwise
        """
        folder = self._find_folder(folder_name)
        if not folder:
            return None

        strategy = ExactMatchSearchStrategy()
        result = strategy.search(folder, file_name) if folder else []

        return result[0] if result else None

    def search_file_like_match(self, folder_name: str, pattern: str) -> list:
        """
        Searches for files by pattern within a specific folder.

        :param folder_name: the name of the folder to search within
        :param pattern: the pattern must be part(Contains) of the file name.
        :return: a list of file names that match the pattern
        """
        folder = self._find_folder(folder_name)
        if not folder:
            return []

        strategy = PatternMatchSearchStrategy()
        return strategy.search(folder, pattern) if folder else []

