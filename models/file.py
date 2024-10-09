from models.file_system_item import FileSystemItem

class File(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)
        self.content = ""

    def get_content(self):
        try:
            self.rw_lock.acquire_read()          # Multiple readers can read simultaneously
            return self.content
        finally:
            self.rw_lock.release_read()

    def set_content(self, content):
        try:
            self.rw_lock.acquire_write()         # Only one writer at a time, no readers allowed
            self.content = content
        finally:
            self.rw_lock.release_write()
