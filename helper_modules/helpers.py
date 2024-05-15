from pathlib import Path
import shutil
from typing import Dict, Generator, List
from helper_modules import constants
import os
from settings import Settings


settings = Settings()

suffixes: Dict[str, List[str]] = settings.get_suffixes()
inodes: List[str] = suffixes["FILES_AND_FOLDERS"]
archive_suffixes: List[str] = suffixes["ARCHIVES"]

# TODO: move sum_directory_tree on filtered list, instead of on all files

def sum_directory_tree(path: Path, glob: str) -> int:
    return sum(f.stat().st_size for f in path.rglob(glob))

# FIXME: refactor method and edit docstring, why should I pass glob to it? Why call it filter by size when
# method returns dict with dirpath and its size?

def filter_by_size(
    path: Path,
    glob: str,
    threshold: int = 50 * constants.KILOBYTE,
    suffixes: list[str] = inodes,
) -> dict[Path, int]:
    """Traverses all items and dirs in path and returns those less than **threshold**. Skips those that are in **suffixes** (dirnames and file extensions) and 

    Args:
        path (Path):
        glob (str):
        threshold (int, optional): Defaults to 50 KiB.
        suffixes[str]: filters those out

    Returns:
        dict[Path, int]: dict with dirpath as key and its size as value
    """
    result: dict[Path, int] = {}
    for item in path.glob(glob):
        if item.is_file() and item.suffix not in suffixes:
            current_size: int = item.stat().st_size
        elif item.is_dir() and item.stem not in suffixes:
            current_size = sum_directory_tree(item, glob=glob)
        else:
            continue

        if current_size < threshold:
            result[item] = current_size
    return result


def get_human_readable_size(size: int = 0) -> str:
    suffix: str = "B"
    current_size: float = float(size)

    if size >= constants.KILOBYTE and size < constants.MEGABYTE:
        suffix = "KiB"
        current_size = size / constants.KILOBYTE

    if size >= constants.MEGABYTE and size < constants.GIGABYTE:
        current_size = size / constants.MEGABYTE
        suffix = "MiB"

    if size >= constants.GIGABYTE:
        current_size = size / constants.GIGABYTE
        suffix = "GiB"

    return str(round(current_size, 2)) + " " + suffix

# TODO: Unit test it and use the dict comprehension afterwards
def find_archives(path: Path) -> dict[Path, int]:
    # archives: dict[Path, int] = {}
    # items: Generator[Path, None, None] = path.glob("*")
    # size = 0
    # for p in list(items):
    #     if p.is_file() and p.suffix in archive_suffixes:
    #         archives[p] = p.stat().st_size
    #         size += archives[p]

    # TODO: implement this: (ChatGPT)
    archives: dict[Path, int] = {  
        p: p.stat().st_size
        for p in path.glob("*")
        if p.is_file() and p.suffix in archive_suffixes
    }
    return archives

# TODO: check why -1 is needed

def find_extracted_archives(path: Path) -> dict[Path, int]:
    folders: dict[Path, int] = {}
    files: dict[Path, int] = {}
    result: dict[Path, int] = {}
    items: Generator[Path, None, None] = path.glob("*")
    for p in list(items):
        if p.is_dir():
            folders[p] = -1
        else:
            if p.suffix in archive_suffixes:
                files[p] = p.stat().st_size

    total_size: float = 0
    for p in files:
        if (
            p.is_file()
            and Path(p.parent, p.stem) in folders
            and p.suffix in archive_suffixes
        ):
            size: int = p.stat().st_size
            result[p] = size
            total_size = total_size + size

    return result


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

def find_unextracted_archives(path: Path) -> dict[Path, int]:
    return {path: -1}

def is_int(s: str) -> bool:
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True

def delete_items(paths: dict[Path, int]) -> None:
    for item in paths:
        os.remove(item)


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


def get_folder_size(folder: Path):
    return sum(file.stat().st_size for file in Path(folder).rglob("*"))


def delete_empty_dirs(paths: dict[Path, int]) -> None:
    pass
    # delete batch files, make it ask for prompt, then uncomment :)
    for item in paths:
        shutil.rmtree(item)

@staticmethod
def filter_directories(
    path: Path, threshold: int = 50 * constants.KILOBYTE
) -> dict[Path, int]:
    batch_list: dict[Path, int] = {}
    current_size: int = -1
    for item in path.rglob("*"):
        if not item.is_dir() or item.stem in inodes:
            continue
        if item.is_file():
            current_size = item.stat().st_size
        elif item.is_dir():
            current_size = sum_directory_tree(item, glob="*")
        if current_size < threshold:
            get_human_readable_size(current_size)
            batch_list[item] = current_size
    return batch_list
