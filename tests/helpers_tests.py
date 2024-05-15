import unittest
from helper_modules import helpers, constants

class TestHumanReadableSizeMethod(unittest.TestCase):
    def test_human_size_zero_bytes(self):
        test_size: int = 0
        size: str = helpers.get_human_readable_size(test_size)
        self.assertEqual(size, "0.0 B")

    def test_human_size_bytes(self):
        test_size: int = 150
        size: str = helpers.get_human_readable_size(test_size)
        self.assertEqual(size, "150.0 B")

    def test_human_size_kilobytes(self):
        test_size: int = 1 * constants.KILOBYTE
        size: str = helpers.get_human_readable_size(test_size)
        self.assertEqual(size, "1.0 KiB")

    def test_human_size_megabytes(self):
        test_size: int = 1 * constants.MEGABYTE
        size: str = helpers.get_human_readable_size(test_size)
        self.assertEqual(size, "1.0 MiB")

    def test_human_size_gigabytes(self):
        test_size = 1 * constants.GIGABYTE
        size: str = helpers.get_human_readable_size(test_size)
        self.assertEqual(size, "1.0 GiB")

    def test_human_size_terabytes(self):
        test_size: int = 1500 * constants.GIGABYTE
        size: str = helpers.get_human_readable_size(test_size)
        self.assertEqual(size, "1500.0 GiB")