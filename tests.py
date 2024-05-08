import inspect
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory
import shutil
from helpers import Helper
from constants import Constants


def seed(path: str) -> list[Path]:
    d1: Path = Path(path, "lvl1/", "lvl2/", "lvl3/")
    d2: Path = Path(path, ".thumb/")
    d1.mkdir(parents=True)
    d2.mkdir()
    with open(Path(d1, "file1.file"), "w") as file:
        file.truncate(100 * Constants.KILOBYTE)
    with open(Path(d1, "file2.file"), "w") as file:
        file.truncate(110 * Constants.KILOBYTE)
    with open(Path(d1.parent, "file3.file"), "w") as file:
        file.truncate(120 * Constants.KILOBYTE)
    with open(Path(d1, "bigger_than_1mb_file.file"), "w") as file:
        file.truncate(1 * Constants.MEGABYTE + 1)
    return list((d1, d2))


class Printer:
    @staticmethod
    def print_files_in_path_recursively(
        path: Path, pattern: str = "*", additional_text: str = ""
    ) -> None:
        print("\n\n" + additional_text)
        for item in path.rglob(pattern):
            print(item)

    @staticmethod
    def print_files_from_list(files: list[Path], additional_text: str = "") -> None:
        print("\n\n" + additional_text)
        for x in files:
            print(x)

    @staticmethod
    def print_paths_from_dict(
        files: dict[Path, int], additional_text: str = ""
    ) -> None:
        print("\n\n" + additional_text)
        for x in files:
            print(x)


class TestHumanReadableSize(unittest.TestCase):
    def test_human_size_zero_bytes(self):
        test_size: int = 0
        size: str = Helper.get_human_readable_size(test_size)
        self.assertEqual(size, "0.0 B")

    def test_human_size_bytes(self):
        test_size: int = 150
        size: str = Helper.get_human_readable_size(test_size)
        self.assertEqual(size, "150.0 B")

    def test_human_size_kilobytes(self):
        test_size: int = 1 * Constants.KILOBYTE
        size: str = Helper.get_human_readable_size(test_size)
        self.assertEqual(size, "1.0 KiB")

    def test_human_size_megabytes(self):
        test_size: int = 1 * Constants.MEGABYTE
        size: str = Helper.get_human_readable_size(test_size)
        self.assertEqual(size, "1.0 MiB")

    def test_human_size_gigabytes(self):
        test_size = 1 * Constants.GIGABYTE
        size: str = Helper.get_human_readable_size(test_size)
        self.assertEqual(size, "1.0 GiB")

    def test_human_size_terabytes(self):
        test_size: int = 1500 * Constants.GIGABYTE
        size: str = Helper.get_human_readable_size(test_size)
        self.assertEqual(size, "1500.0 GiB")


class TestHelperMethods(unittest.TestCase):
    def test_create_folders(self, verbose: bool = False):
        with TemporaryDirectory() as tmp_dir:
            self.assertFalse(any(Path(tmp_dir).iterdir()))
            dirs: list[Path] = list(Helper.create_folders(tmp_dir))
            if verbose:
                Printer.print_files_from_list(dirs)
                self.assertTrue(any(Path(tmp_dir).iterdir()))

    def test_create_files_in_folders(self, verbose: bool = False):
        with TemporaryDirectory() as tmp_dir:
            Helper.create_folders(tmp_dir)
            f1, f2, f3, f4 = Helper.create_files(tmp_dir)
            self.assertTrue(f1.is_file())
            self.assertEqual(f1.stat().st_size, 100 * 1024)
            self.assertTrue(f2.is_file())
            self.assertEqual(f2.stat().st_size, 110 * 1024)
            self.assertTrue(f3.is_file())
            self.assertEqual(f3.stat().st_size, 20 * 1024)
            self.assertTrue(f2.is_file())
            self.assertGreater(f4.stat().st_size, 1024 * 1024)


class TestDeleteDirTree(unittest.TestCase):
    def test_shutil_rmtree(self, verbose: bool = False) -> None:
        with TemporaryDirectory() as tmp_dir:
            self.d1, self.d2 = seed(tmp_dir)
            self.assertTrue(self.d1.is_dir())
            self.assertTrue(self.d2.is_dir())
            if verbose:
                Printer.print_files_in_path_recursively(
                    Path(tmp_dir), "*", f"printed by {inspect.stack()[0][3]}() "
                )

            shutil.rmtree(tmp_dir)
            if verbose:
                Printer.print_files_in_path_recursively(
                    Path(tmp_dir), "*", "Printed after shutil.rmtree()\n"
                )

            self.assertFalse(Path(tmp_dir).exists())


class TestFiltering(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass
        # TODO: Add decorator to functions for verbose mode

    def test_filter_of_files(self, verbose: bool = True) -> None:
        with TemporaryDirectory() as tmp_dir:
            self.d1: Path
            self.d2: Path
            self.d1, self.d2 = Helper.create_folders(tmp_dir)
            Helper.create_files(tmp_dir)
            self.assertTrue(self.d1.is_dir())
            self.assertTrue(self.d2.is_dir())
            # less than 1 MiB
            files_dict: dict[Path, int] = Helper.filter_by_size(
                Path(tmp_dir),
                Constants.EMPTY_DIR_GLOB,
                1 * Constants.MEGABYTE,
            )
            if verbose:
                Printer.print_paths_from_dict(
                    files_dict, additional_text="print after filtering"
                )
            expected_number_of_items: int = (
                0 if ".thumb" in Constants.FILTER_SUFFIXES else 1
            )
            self.assertEqual(len(files_dict), expected_number_of_items)
            # less than 2 MiB
            files_dict = Helper.filter_by_size(
                Path(tmp_dir), Constants.EMPTY_DIR_GLOB, 2 * Constants.MEGABYTE
            )
            expected_number_of_items = 1 if ".thumb" in Constants.FILTER_SUFFIXES else 2
            self.assertEqual(len(files_dict), expected_number_of_items)
            files_dict = Helper.filter_by_size(Path(tmp_dir), Constants.EMPTY_DIR_GLOB)
            # < 50 kb .thumbs and file3
            expected_number_of_items = 0 if ".thumb" in Constants.FILTER_SUFFIXES else 1
            self.assertEqual(len(files_dict), expected_number_of_items)  #


if __name__ == "__main__":
    unittest.main()
