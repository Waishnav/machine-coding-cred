from typing import List
from models.file import File
from models.file_system_item import FileSystemItem
from models.folder import Folder
from strategy.file_system_traverser import FileSystemTraverser
from strategy.search_strategy import SearchStrategy


class ExactMatchSearchStrategy(SearchStrategy):
    def search(self, folder: Folder, criteria: str) -> List[str]:
        traverser = FileSystemTraverser[List[str]]()
        result = []
        def collect_exact_matches(item: FileSystemItem) -> None:
            if isinstance(item, File) and item.get_name == criteria:
                result.append(item.get_name)
        traverser.traverse(folder, collect_exact_matches)
        return result

