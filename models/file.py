from models.file_system_item import FileSystemItem

class File(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)

    def is_folder(self) -> bool:
        return False
