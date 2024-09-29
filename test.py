import unittest
import logging
import threading

from service.file_system_manager_imp import FileSystemManagerImpl

logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to see all log messages
logger = logging.getLogger(__name__)

# Custom TestResult class to log test start and end
class LoggingTestResult(unittest.TextTestResult):
    def startTest(self, test):
        logger.info(f"Starting test: {test}")
        super().startTest(test)

    def stopTest(self, test):
        logger.info(f"Finished test: {test}")
        super().stopTest(test)

# Custom TestRunner to use LoggingTestResult
class LoggingTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return LoggingTestResult(self.stream, self.descriptions, self.verbosity)








class FileSystemManagerTest(unittest.TestCase):

    # Adding a file to an existing folder
    def test_adding_file_to_existing_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        contents = file_system_manager.list_contents("folder1")
        self.assertIsNotNone(contents)
        self.assertIn("file1.txt", contents)

    # Adding a folder to an existing folder
    def test_adding_folder_to_existing_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "subfolder1", True)
        contents = file_system_manager.list_contents("folder1")
        self.assertIsNotNone(contents)
        self.assertIn("subfolder1", contents)

    # Adding a file or folder to a non-existent parent folder
    def test_adding_to_non_existent_parent_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("nonExistentFolder", "file1.txt", False)
        contents = file_system_manager.list_contents("root")
        self.assertIsNotNone(contents)
        self.assertNotIn("file1.txt", contents)

    # Moving a file or folder to a non-existent destination folder
    def test_moving_to_non_existent_destination_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "file1.txt", False)
        file_system_manager.move_file_or_folder("file1.txt", "nonExistentFolder")
        contents = file_system_manager.list_contents("root")
        self.assertIsNotNone(contents)
        self.assertIn("file1.txt", contents)

    # Moving a non-existent file or folder
    def test_moving_non_existent_file_or_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.move_file_or_folder("nonExistentFile", "folder1")
        contents = file_system_manager.list_contents("folder1")
        self.assertIsNotNone(contents)
        self.assertNotIn("nonExistentFile", contents)

    # Listing contents of a folder
    def test_listing_contents_of_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        contents = file_system_manager.list_contents("folder1")
        self.assertIsNotNone(contents)
        self.assertIn("file1.txt", contents)

    # Moving a folder from one folder to another
    def test_move_folder_to_another_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "folder2", True)
        file_system_manager.move_file_or_folder("folder2", "root")
        root_contents = file_system_manager.list_contents("root")
        folder1_contents = file_system_manager.list_contents("folder1")
        self.assertIsNotNone(root_contents)
        self.assertIn("folder2", root_contents)
        self.assertIsNotNone(folder1_contents)
        self.assertNotIn("folder2", folder1_contents)

    # Moving a file from one folder to another
    def test_moving_file_to_another_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("root", "folder2", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        file_system_manager.move_file_or_folder("file1.txt", "folder2")
        contents_folder1 = file_system_manager.list_contents("folder1")
        contents_folder2 = file_system_manager.list_contents("folder2")
        self.assertIsNotNone(contents_folder1)
        self.assertNotIn("file1.txt", contents_folder1)

        self.assertIsNotNone(contents_folder2)
        self.assertIn("file1.txt", contents_folder2)

    # Listing the entire directory structure
    def test_listing_entire_directory_structure(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        structure = file_system_manager.list_directory_structure()

        self.assertIsNotNone(structure)
        self.assertIn("+ root", structure)
        self.assertIn("  + folder1", structure)
        self.assertIn("    - file1.txt", structure)

    # Searching for a file with an exact match
    def test_search_file_exact_match(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        result = file_system_manager.search_file_exact_match("folder1", "file1.txt")
        self.assertIsNotNone(result)
        self.assertEqual("file1.txt", result)

    # Searching for files with a pattern match
    def test_search_file_like_match(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        file_system_manager.add_file_or_folder("folder1", "file2.jpg", False)
        file_system_manager.add_file_or_folder("folder1", "subfolder", True)
        file_system_manager.add_file_or_folder("subfolder", "file3.txt", False)
        search_results = file_system_manager.search_file_like_match("root", ".txt")

        self.assertIsNotNone(search_results)
        self.assertEqual(2, len(search_results))
        self.assertIn("file1.txt", search_results)
        self.assertIn("file3.txt", search_results)

    # Listing contents of a non-existent folder
    def test_listing_contents_of_non_existent_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        contents = file_system_manager.list_contents("non_existent_folder")

        self.assertIsNotNone(contents)
        self.assertEqual(0, len(contents))

    # Searching for a file with a pattern that matches no files
    def test_search_file_with_no_matching_pattern(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        results = file_system_manager.search_file_like_match("folder1", "pattern")

        self.assertIsNotNone(results)
        self.assertEqual(0, len(results))

    # Searching for a file in a non-existent folder
    def test_searching_for_file_in_non_existent_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        result = file_system_manager.search_file_exact_match("non_existent_folder", "file.txt")
        self.assertIsNone(result)

    # Handling of duplicate file or folder names within the same parent folder
    def test_handling_duplicate_names_within_parent_folder(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        file_system_manager.add_file_or_folder("folder1", "file1.txt", False)
        contents = file_system_manager.list_contents("folder1")

        self.assertIsNotNone(contents)
        self.assertEqual(1, contents.count("file1.txt"))

    # Handling of special characters in file and folder names
    def test_handling_special_characters_in_names(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder$#@!", True)
        file_system_manager.add_file_or_folder("folder$#@!", "file%^&.txt", False)
        contents = file_system_manager.list_contents("folder$#@!")

        self.assertIsNotNone(contents)
        self.assertIn("file%^&.txt", contents)

    # Performance with a large number of files and folders
    def test_performance_large_number_of_files_and_folders(self):
        # Prepare a large number of files and folders
        file_system_manager = FileSystemManagerImpl("root")

        #  Add a large number of files and folders
        for i in range(1000):
            file_system_manager.add_file_or_folder("root", "folder{}".format(i), True)
            file_system_manager.add_file_or_folder("folder{}".format(i), "file{}.txt".format(i), False)

        # List contents of a specific folder with a large number of items.
        contents = file_system_manager.list_contents("folder500")

        # Assert that the contents contain a specific file
        self.assertIsNotNone(contents)
        self.assertIn("file500.txt", contents)

    # Case sensitivity in file and folder names during search operations
    def test_case_sensitivity_search_operations(self):
        # Create FileSystemManagerImpl instance
        file_system_manager = FileSystemManagerImpl("Root")

        # Add files and folders with different case variations
        file_system_manager.add_file_or_folder("Root", "Folder1", True)
        file_system_manager.add_file_or_folder("Folder1", "file1.txt", False)
        file_system_manager.add_file_or_folder("Folder1", "File2.TXT", False)
        file_system_manager.add_file_or_folder("Folder1", "FOLDER2", True)

        # Search for files with different case variations
        exact_match = file_system_manager.search_file_exact_match("Folder1", "file1.txt")
        like_match_results = file_system_manager.search_file_like_match("Folder1", "file")

        # Assertions for case sensitivity
        self.assertIsNotNone(exact_match)
        self.assertEqual("file1.txt", exact_match)

        self.assertIsNotNone(like_match_results)
        self.assertIn("file1.txt", like_match_results)
        self.assertIn("File2.TXT", like_match_results)
        self.assertNotIn("FOLDER2", like_match_results)


    def test_concurrent_folder_access(self):
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "folder1", True)
        
        def list_contents():
            file_system_manager.list_contents("folder1")
        
        threads = []
        for _ in range(50):
            thread = threading.Thread(target=list_contents)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        self.assertTrue(True)

    def test_concurrent_add_operations(self):
        file_system_manager = FileSystemManagerImpl("root")
        
        def add_file(index):
            file_system_manager.add_file_or_folder("root", f"file{index}.txt", False)
        
        threads = []
        for i in range(100):
            thread = threading.Thread(target=add_file, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        contents = file_system_manager.list_contents("root")
        self.assertEqual(len(contents), 100)

if __name__ == "__main__":
    logger.info("Starting unit tests")
    unittest.main(testRunner=LoggingTestRunner())
