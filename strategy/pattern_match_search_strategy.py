from typing import List
from models.file import File
from models.file_system_item import FileSystemItem
from models.folder import Folder
from strategy.file_system_traverser import FileSystemTraverser
from strategy.search_strategy import SearchStrategy

class PatternMatchSearchStrategy(SearchStrategy):
    def search(self, folder: Folder, criteria: str) -> List[str]:
        traverser = FileSystemTraverser[List[str]]()
        result = []
        def collect_pattern_matches(item: FileSystemItem) -> None:
            if isinstance(item, File) and criteria.lower() in item.get_name.lower():
                result.append(item.get_name)
        traverser.traverse(folder, collect_pattern_matches)
        return result
