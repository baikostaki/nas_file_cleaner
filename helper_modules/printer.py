from enum import Enum
from pathlib import Path
import os
from helper_modules import helpers
import helper_modules.constants as constants
from helper_modules import terminal_colors as bcolors #as bcolors because otherwise I have to change in below




def print_files_in_path_recursively(
    path: Path, pattern: str = "*", additional_text: str = ""
) -> None:
    print("\n\n" + additional_text)
    for item in path.rglob(pattern):
        print(item)


def print_files_from_list(files: list[Path], additional_text: str = "") -> None:
    print("\n\n" + additional_text)
    for x in files:
        print(x)


def print_emptylike_folders(items: dict[Path, int], root_dir: Path) -> None:
    print(
        bcolors.WARNING
        + f"Listing items less than {helpers.get_human_readable_size(constants.FILE_SIZE_THRESHOLD)} in {root_dir}:"
        + bcolors.ENDC
    )

    total_size: int = 0
    for k, v in items.items():
        print(f"{str(k)} -> {helpers.get_human_readable_size(v)}")
        total_size = total_size + v

    print(
        bcolors.WARNING
        + f'Total size for {len(items)} folder{"s" if len(items)>1 else ""} is {helpers.get_human_readable_size(total_size)}'
        + bcolors.ENDC
    )


def print_items(dirs: dict[Path, int], colors: str, total: bool = True) -> None:
    total_sum = 0
    for k, v in dirs.items():
        print(colors + f"{k} -> {helpers.get_human_readable_size(v)}" + bcolors.ENDC)
        total_sum: int = total_sum + v
    if total:
        print("total sum: " + helpers.get_human_readable_size(total_sum))


def print_unpacked_archives(items: dict[Path, int], path: Path) -> None:
    print(bcolors.OKGREEN + f"Listing unpacked archives in {path}: " + bcolors.ENDC)
    print_items(items, bcolors.ENDC)
    print(
        bcolors.OKGREEN
        + f'Total size for {len(items)} unpacked archive{"s" if len(items)>1 else ""} is {helpers.get_human_readable_size(sum(items.values()))}'
        + bcolors.ENDC
    )


def remove_redundant_dir(path: Path) -> None:
    os.chdir(path)
    pass


class App_Modes(Enum):
    DELETE_EMPTYLIKE_DIRS = 1
    DELETE_UNPACKED_ARCHIVES = 2
    EXTRACT_ARCHIVES = 3
    REMOVE_NESTED_DIRECTORIES = 4

        