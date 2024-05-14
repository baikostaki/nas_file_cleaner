from enum import Enum
from pathlib import Path
import shutil
from typing import Generator
from constants import Constants, bcolors
import os


class Helper:
    # TODO: move sum_directory_tree on filtered list, instead of on all files
    @staticmethod
    def sum_directory_tree(path: Path, glob: str) -> int:
        return sum(f.stat().st_size for f in path.rglob(glob))

    # TODO: check if item.is_file is needed below in for loop
    @staticmethod
    def filter_by_size(
        path: Path, glob: str, threshold: int = 50 * Constants.KILOBYTE
    ) -> dict[Path, int]:
        batch_list: dict[Path, int] = {}
        current_size: int = -1
        # test: list[Path]  =  [x for x in Path(path).rglob(glob)]
        # processed: list[Path] = []
        for item in path.glob(glob):
            if item.is_file() and item.stem not in Constants.FILTER_SUFFIXES:
                current_size = item.stat().st_size
            elif item.is_dir():
                current_size = Helper.sum_directory_tree(item, glob=glob)

            if current_size < threshold and not item.is_file():
                # get_human_readable_size(current_size)
                batch_list[item] = current_size
        return batch_list

    @staticmethod
    def create_folders(path: str) -> tuple[Path, Path]:
        d1: Path = Path(path, "lvl1/", "lvl2/", "lvl3/")
        d2: Path = Path(path, ".thumb/")
        d1.mkdir(parents=True)
        d2.mkdir()
        return (d1, d2)

    @staticmethod
    def get_human_readable_size(size: int = 0) -> str:
        suffix: str = "B"
        current_size: float = float(size)

        if size >= Constants.KILOBYTE and size < Constants.MEGABYTE:
            suffix = "KiB"
            current_size = size / Constants.KILOBYTE

        if size >= Constants.MEGABYTE and size < Constants.GIGABYTE:
            current_size = size / Constants.MEGABYTE
            suffix = "MiB"

        if size >= Constants.GIGABYTE:
            current_size = size / Constants.GIGABYTE
            suffix = "GiB"

        return str(round(current_size, 2)) + " " + suffix

    # TODO - move this to tests, makes no sense to be here
    @staticmethod
    def create_files(path: str) -> tuple[Path, Path, Path, Path]:
        d1: Path = Path(path, "lvl1/", "lvl2/", "lvl3/")
        f1: Path = Path(d1, "file1.file")
        f2: Path = Path(d1, "file2.file")
        f3: Path = Path(d1.parent, "file3.file")
        f4: Path = Path(d1, "bigger_than_1mb_file.file")
        with open(f1, "w") as file:
            file.truncate(100 * Constants.KILOBYTE)
        with open(f2, "w") as file:
            file.truncate(110 * Constants.KILOBYTE)
        with open(f3, "w") as file:
            file.truncate(20 * Constants.KILOBYTE)
        with open(f4, "w") as file:
            file.truncate(1 * Constants.MEGABYTE + 1)
        return (f1, f2, f3, f4)

    @staticmethod
    def change_base_dir_in_path(paths: tuple[Path], tmp_dir: str) -> list[Path]:
        """
        changes temp folder part in path.parts for case when path created in another Temporary Directory
        """

        path_list: list[Path] = list(paths)
        for i, p in enumerate(path_list):
            parts: list[str] = list(p.parts)
            parts[6] = tmp_dir
            path_list[i] = Path(*parts)
        return path_list

    #TODO: Unit test it and use the dict comprehension afterwards
    @staticmethod
    def find_archives(path: Path) -> dict[Path, int]:
        archives: dict[Path, int] = {}
        items: Generator[Path, None, None] = path.glob("*")
        size = 0
        for p in list(items):
            if p.is_file() and p.suffix in Constants.ARCHIVE_SUFFIXES:
                archives[p] = p.stat().st_size
                size += archives[p]
        archives2: dict[Path, int] = {
            p: p.stat().st_size
            for p in path.glob("*")
            if p.is_file() and p.suffix in Constants.ARCHIVE_SUFFIXES
        }
        return archives

    #TODO: check why -1 is needed
    @staticmethod
    def find_extracted_archives(path: Path) -> dict[Path, int]:
        folders: dict[Path, int] = {}
        files: dict[Path, int] = {}
        result: dict[Path, int] = {}
        items: Generator[Path, None, None] = path.glob("*")
        for p in list(items):
            if p.is_dir():
                folders[p] = -1
            else:
                if p.suffix in Constants.ARCHIVE_SUFFIXES:
                    files[p] = p.stat().st_size

        total_size: float = 0
        for p in files:
            if (
                p.is_file()
                and Path(p.parent, p.stem) in folders
                and p.suffix in Constants.ARCHIVE_SUFFIXES
            ):
                size: int = p.stat().st_size
                result[p] = size
                total_size = total_size + size

        return result

    @staticmethod
    def list_files(path: Path) -> dict[Path, int]:
        files: dict[Path, int] = {}
        result: dict[Path, int] = {}
        items: Generator[Path, None, None] = path.glob("*")
        for p in list(items):
            if p.is_dir():
                pass
            if p.is_file():
                files[p] = p.stat().st_size

        total_size: float = 0
        for p in files:
            if p.is_file():
                size: int = p.stat().st_size
                result[p] = size
                total_size = total_size + size

        return result

    # @staticmethod
    # def find_and_print_archives_to_delete(path: Path) -> dict[Path, int]:
    #     result: dict[Path, int] = Helper.find_extracted_archives(Path(path))
    #     return result

    @staticmethod
    def find_unextracted_archives(path: Path) -> dict[Path, int]:
        return {path: -1}

    @staticmethod
    def is_int(s: str) -> bool:
        try:
            int(s)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def delete_items(paths: dict[Path, int]) -> None:
        for item in paths:
            os.remove(item)

    @staticmethod
    def find_nested_directories(curr_path: Path) -> list[Path]:
        batch_list: list[Path] = []
        items: Generator[Path, None, None] = curr_path.glob("*")
        parent_folder_name: str
        for i in items:
            if i.is_dir():
                parent_folder_name = i.name
                sub_folders = list(i.glob("*/"))
                for sub_folder in sub_folders:
                    if sub_folder.name == parent_folder_name:
                        batch_list.append(Path(sub_folder.parent, parent_folder_name))
        [print(x) for x in batch_list]
        return batch_list

    @staticmethod
    def get_folder_size(folder: Path):
        return sum(file.stat().st_size for file in Path(folder).rglob("*"))

    @staticmethod
    def delete_empty_dirs(paths: dict[Path, int]) -> None:
        pass
        # delete batch files, make it ask for prompt, then uncomment :)
        for item in paths:
            shutil.rmtree(item)

    @staticmethod
    def filter_directories(
        path: Path, threshold: int = 50 * Constants.KILOBYTE
    ) -> dict[Path, int]:
        batch_list: dict[Path, int] = {}
        current_size: int = -1
        for item in path.rglob("*"):
            if not item.is_dir() or item.stem in Constants.FILTER_SUFFIXES:
                continue
            if item.is_file():
                current_size = item.stat().st_size
            elif item.is_dir():
                current_size = Helper.sum_directory_tree(item, glob="*")
            if current_size < threshold:
                Helper.get_human_readable_size(current_size)
                batch_list[item] = current_size
        return batch_list


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
    def print_emptylike_folders(items: dict[Path, int], root_dir: Path) -> None:
        print(
            bcolors.WARNING
            + f"Listing folders less than {Helper.get_human_readable_size(Constants.FILE_SIZE_THRESHOLD)} in {root_dir}:"
            + bcolors.ENDC
        )

        total_size: int = 0
        for k, v in items.items():
            print(f"{str(k)} -> {Helper.get_human_readable_size(v)}")
            total_size = total_size + v

        print(
            bcolors.WARNING
            + f'Total size for {len(items)} folder{"s" if len(items)>1 else ""} is {Helper.get_human_readable_size(total_size)}'
            + bcolors.ENDC
        )

    @staticmethod
    def print_items(dirs: dict[Path, int], colors: str, total: bool = True) -> None:
        total_sum = 0
        for k, v in dirs.items():
            print(colors + f"{k} -> {Helper.get_human_readable_size(v)}" + bcolors.ENDC)
            total_sum: int = total_sum + v
        if total:
            print("total sum: " + Helper.get_human_readable_size(total_sum))

    @staticmethod
    def print_unpacked_archives(items: dict[Path, int], path: Path) -> None:
        print(bcolors.OKGREEN + f"Listing unpacked archives in {path}: " + bcolors.ENDC)
        Printer.print_items(items, bcolors.ENDC)
        print(
            bcolors.OKGREEN
            + f'Total size for {len(items)} unpacked archive{"s" if len(items)>1 else ""} is {Helper.get_human_readable_size(sum(items.values()))}'
            + bcolors.ENDC
        )

    @staticmethod
    def remove_redundant_dir(path: Path) -> None:
        os.chdir(path)
        pass


class App_Modes(Enum):
    DELETE_EMPTYLIKE_DIRS = 1
    DELETE_UNPACKED_ARCHIVES = 2
    EXTRACT_ARCHIVES = 3
    REMOVE_NESTED_DIRECTORIES = 4


# for a in archives:
#             if not Path(a.stem).is_dir():
#                 os.mkdir(a.stem)
#             #Archive(str(a)).extractall(fr'{a.stem}\.')
#             #patoolib.extract_archive(str(a), outdir=fr'{a.stem}\.')
#             patoolib.search_archive(a.stem, str(a)) # type: ignore
