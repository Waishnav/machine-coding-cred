from abc import ABC, abstractmethod
from typing import List

from models.folder import Folder

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, folder: Folder, criteria: str) -> List[str]:
        pass
