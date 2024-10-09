import threading
import time
import random
import unittest
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    def test_concurrent_readers(self):
        """Test multiple threads reading simultaneously"""
        # Setup initial structure
        file_system_manager = FileSystemManagerImpl("root")
        file_system_manager.add_file_or_folder("root", "test_file.txt", False)

        def reader_task():
            for _ in range(10):
                contents = file_system_manager.list_contents("root")
                self.assertIn("test_file.txt", contents)
                time.sleep(0.01)  # Small delay to increase chance of thread overlap

        # Create and start multiple reader threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=reader_task)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def test_concurrent_writers(self):
        """Test multiple threads writing to different locations"""
        results = []
        file_system_manager = FileSystemManagerImpl("root")

        def writer_task(folder_name):
            file_system_manager.add_file_or_folder("root", folder_name, True)
            file_system_manager.add_file_or_folder(folder_name, "file.txt", False)
            results.append(folder_name)

        # Create and start multiple writer threads
        threads = []
        for i in range(10):
            folder_name = f"folder_{i}"
            thread = threading.Thread(target=writer_task, args=(folder_name,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify results
        contents = file_system_manager.list_contents("root")
        for folder_name in results:
            self.assertIn(folder_name, contents)
            folder_contents = file_system_manager.list_contents(folder_name)
            self.assertIn("file.txt", folder_contents)

    def test_readers_writers_conflict(self):
        """Test concurrent readers and writers"""
        stop_flag = threading.Event()
        file_system_manager = FileSystemManagerImpl("root")

        def reader_task():
            while not stop_flag.is_set():
                contents = file_system_manager.list_contents("root")
                time.sleep(0.01)

        def writer_task():
            for i in range(5):
                file_name = f"file_{i}.txt"
                file_system_manager.add_file_or_folder("root", file_name, False)
                time.sleep(0.02)

        # Start multiple reader threads
        reader_threads = []
        for _ in range(5):
            thread = threading.Thread(target=reader_task)
            thread.daemon = True  # Make thread daemon so it exits when main thread exits
            reader_threads.append(thread)
            thread.start()

        # Start multiple writer threads
        writer_threads = []
        for _ in range(3):
            thread = threading.Thread(target=writer_task)
            writer_threads.append(thread)
            thread.start()

        # Wait for writers to complete
        for thread in writer_threads:
            thread.join()

        # Signal readers to stop and wait for them
        stop_flag.set()
        for thread in reader_threads:
            thread.join(timeout=1.0)

        # Verify final state
        contents = file_system_manager.list_contents("root")
        for i in range(5):
            self.assertIn(f"file_{i}.txt", contents)

    def test_concurrent_moves(self):
        """Test concurrent move operations"""
        file_system_manager = FileSystemManagerImpl("root")
        # Setup initial structure
        for i in range(5):
            file_system_manager.add_file_or_folder("root", f"source_folder_{i}", True)
            file_system_manager.add_file_or_folder("root", f"dest_folder_{i}", True)
            file_system_manager.add_file_or_folder(f"source_folder_{i}", f"file_{i}.txt", False)

        def move_task(index):
            source = f"file_{index}.txt"
            dest = f"dest_folder_{index}"
            file_system_manager.move_file_or_folder(source, dest)

        # Create and start multiple move threads
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(move_task, i) for i in range(5)]
            # Wait for all moves to complete
            for future in as_completed(futures):
                future.result()

        # Verify final state
        for i in range(5):
            source_contents = file_system_manager.list_contents(f"source_folder_{i}")
            dest_contents = file_system_manager.list_contents(f"dest_folder_{i}")
            self.assertNotIn(f"file_{i}.txt", source_contents)
            self.assertIn(f"file_{i}.txt", dest_contents)

    def test_stress_test(self):
        """Stress test with multiple concurrent operations"""
        file_system_manager = FileSystemManagerImpl("root")
        def random_operation():
            op = random.randint(0, 2)
            if op == 0:  # Read operation
                file_system_manager.list_contents("root")
            elif op == 1:  # Write operation
                file_name = f"file_{random.randint(0, 1000)}.txt"
                file_system_manager.add_file_or_folder("root", file_name, False)
            else:  # Move operation
                contents = file_system_manager.list_contents("root")
                if contents:
                    file_to_move = random.choice(contents)
                    file_system_manager.move_file_or_folder(file_to_move, "root")

        # Create and start multiple threads performing random operations
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(random_operation) for _ in range(100)]
            # Wait for all operations to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.fail(f"Stress test failed with error: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting unit tests")
    unittest.main(testRunner=LoggingTestRunner())
