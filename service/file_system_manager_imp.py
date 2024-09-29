from typing import Deque
from service.file_system_manager import FileSystemManager
from models.folder import Folder
from models.file import File
from collections import deque

class FileSystemManagerImpl(FileSystemManager):

    def __init__(self, root_name):
        self.root = Folder(root_name)

    def _find_folder(self, folder_name: str) -> Folder:
        if self.root.get_name == folder_name:
            return self.root
        return self._find_folder_recursively(self.root, folder_name)

    def _find_folder_recursively(self, current_folder: Folder, folder_name: str) -> Folder:
        found_item = current_folder.get_item(folder_name)
        if found_item and found_item.is_folder():
            return found_item

        for item in current_folder.get_items:
            if item.is_folder():
                found_folder = self._find_folder_recursively(item, folder_name)
                if found_folder:
                    return found_folder
        return None

    def _find_match_file_recursively(self, current_folder: Folder, pattern: str) -> list:
        folders :Deque[Folder] = deque()
        folders.append(current_folder)
        matched_items = []
        while folders:
            folder = folders.popleft()
            for item in folder.get_items:
                if not item.is_folder() and pattern.lower() in item.get_name.lower():
                    matched_items.append(item.get_name)
                if item.is_folder():
                    folders.append(item)

        return matched_items

    def _find_exact_file_recursively(self, current_folder: Folder, searched_file: str) -> str:
        folders :Deque[Folder] = deque()
        folders.append(current_folder)
        while folders:
            folder = folders.popleft()
            for item in folder.get_items:
                if not item.is_folder() and searched_file == item.get_name:
                    return item
                if item.is_folder():
                    folders.append(item)
        return None

    def _find_parent_folder_recursively(self, current_folder, name):
        folders = deque()
        folders.append(current_folder)
        while folders:
            folder = folders.popleft()
            for item in folder.get_items:
                if item.get_name == name:
                    return (folder, item)
                if item.is_folder():
                    folders.append(item)
        return (None, None)

    def _list_directory(self, folder, level):
        result = []
        if level == 0:
            result.append("+ " + folder.get_name)
        else:
            indent = ' '*level
            result.append(indent + "+ " + folder.get_name)

        for item in folder.get_items:
            if item.is_folder():
                result.extend(self._list_directory(item, level + 2))
            else:
                file_indent = " "*(level +2)
                result.append(file_indent + "- " + item.get_name)
        return result

    def add_file_or_folder(self, parent_folder_name: str, name: str, is_folder: bool) -> bool:
        """
        Adds a file or folder to the system.

        :param parent_folder_name: the name of the parent folder
        :param name:
        :param is_folder:
        """
        parent_folder = self._find_folder(parent_folder_name)
        if parent_folder:
            if is_folder:
                new_folder = Folder(name)
                parent_folder.add_item(new_folder)
            else:
                new_file = File(name)
                parent_folder.add_item(new_file)
            return True
        else:
            return False

    def move_file_or_folder(self, source_name: str, destination_folder: str) -> bool:
        """
        Moves a file or folder to a new location.

        :param source_name: the name of the file or folder to move
        :param destination_folder: the name of the destination folder
        """
        final_folder = self._find_folder(destination_folder)
        if final_folder:
            parent_of_source, source_item = self._find_parent_folder_recursively(self.root, source_name)
            if parent_of_source:
                parent_of_source.remove_item(source_item)
                final_folder.add_item(source_item)
                return True
            else:
                return False
        else:
            return False

    def list_contents(self, folder_name: str) -> list:
        """
        Lists the contents of a specific folder.

        :param folder_name: the name of the folder
        :return: a list of names of files and folders within the specified folder
        """
        curr_folder = self._find_folder(folder_name)
        if curr_folder:
            return [item.get_name for item in curr_folder.get_items]
        return []

    def list_directory_structure(self) -> list:
        """
        Returns the directory structure of each file and folder in the file system.

        :return: a list representing the directory structure
        """
        return self._list_directory(self.root, 0) 

    def search_file_exact_match(self, folder_name: str, file_name: str) -> str :
        """
        Searches for an exact file match within a specific folder.

        :param folder_name: the name of the folder to search within
        :param file_name: the exact name of the file to search for
        :return: the name of the file if found, null otherwise
        """
        curr_folder = self._find_folder(folder_name)
        if curr_folder:
            item = self._find_exact_file_recursively(curr_folder, file_name)
            return item.get_name
        return None

    def search_file_like_match(self, folder_name: str, pattern: str) -> list:
        """
        Searches for files by pattern within a specific folder.

        :param folder_name: the name of the folder to search within
        :param pattern: the pattern must be part(Contains) of the file name.
        :return: a list of file names that match the pattern
        """
        curr_folder = self._find_folder(folder_name)
        if curr_folder:
            all_items = self._find_match_file_recursively(curr_folder, pattern)
            return all_items
        else:
            return []
