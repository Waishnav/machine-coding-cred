from abc import ABC, abstractmethod
from typing import Optional

class FileSystemManager(ABC):

    @abstractmethod
    def add_file_or_folder(self, parent_folder_name: str, name: str, is_folder: bool) -> bool:
        """
        Adds a file or folder to the system.

        :param parent_folder_name: the name of the parent folder
        :param name: the name of the file or folder to add
        :param is_folder: whether the new item is a folder
        :return: True if added successfully, otherwise False
        """
        pass

    @abstractmethod
    def move_file_or_folder(self, source_name: str, destination_folder: str) -> bool:
        """
        Moves a file or folder to a new location.

        :param source_name: the name of the file or folder to move
        :param destination_folder: the name of the destination folder
        :return: True if moved successfully, otherwise False
        """
        pass

    @abstractmethod
    def list_contents(self, folder_name: str) -> list:
        """
        Lists the contents of a specific folder.

        :param folder_name: the name of the folder
        :return: a list of names of files and folders within the specified folder
        """
        pass

    @abstractmethod
    def list_directory_structure(self) -> list:
        """
        Returns the directory structure of each file and folder in the file system.

        :return: a list representing the directory structure
        """
        pass

    @abstractmethod
    def search_file_exact_match(self, folder_name: str, file_name: str) -> Optional[str]:
        """
        Searches for an exact file match within a specific folder.

        :param folder_name: the name of the folder to search within
        :param file_name: the exact name of the file to search for
        :return: the name of the file if found, None otherwise
        """
        pass

    @abstractmethod
    def search_file_like_match(self, folder_name: str, pattern: str) -> list:
        """
        Searches for files by pattern within a specific folder.

        :param folder_name: the name of the folder to search within
        :param pattern: the pattern that must be part of the file name.
        :return: a list of file names that match the pattern
        """
        pass
