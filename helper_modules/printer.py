# TODO fix printer - maybe make it a class - it
from pathlib import Path
import os
from typing import Any
from helper_modules import helpers
import helper_modules.constants as constants
from helper_modules import (
    terminal_colors as bcolors,
)  # as bcolors because otherwise I have to change in below


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
        + f"Listing items less than {helpers.get_human_readable_size(constants.FILE_SIZE_THRESHOLD)} in {repr(str(root_dir))}:"
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


# TODO: add logic to fallback to default color if you write color = "white"
# TODO: maybe write decorators for each color if it is possible?
def ppath(path: Any, color: str = bcolors.WARNING) -> None:  # type: ignore
    """short for print path - it equally whether the argument is of type Path or str

    Args:
        path (Any): path to file/directory
        color (string, optional, defaults to bcolors.Warning): uses bcolors ANSI things to set color to console

    Raises:
        TypeError: if you call it on other printable types -> you shouldn't :)
    """

    if isinstance(path, str):
        print(color + repr(path) + bcolors.ENDC)
    elif isinstance(path, Path):
        print(color + repr(str(path)) + bcolors.ENDC)
    else:
        raise TypeError(
            f"{path}: {type(path)} is not a supported type. Expected Path or str"
        )


def print_no_emptylike_message(path: Path) -> None:
    ppath(f"No emptylike folders found in {(path)}")


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
