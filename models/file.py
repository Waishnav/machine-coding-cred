from models.file_system_item import FileSystemItem

class File(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)
        self.content = ""

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content
