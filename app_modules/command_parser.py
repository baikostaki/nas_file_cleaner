from enum import Enum
from pathlib import Path
import shutil
import os

import patoolib  # type: ignore
from typing import List

from helper_modules import helpers, printer, constants
from helper_modules.printer import bcolors

# TODO: Refactor user input out of function performing tasks


class App_Modes(Enum):
    DELETE_EMPTYLIKE_DIRS = 1
    DELETE_UNPACKED_ARCHIVES = 2
    EXTRACT_ARCHIVES = 3
    REMOVE_NESTED_DIRECTORIES = 4


class Commander:
    filenode_extensions: List[str] = []
    threshold: int = 1 * constants.MEGABYTE
    operation_mode: int = 0

    # TODO: Move all settings in this class maybe?
    def __init__(
        self, settings: List[str], threshhold: int = 1 * constants.MEGABYTE
    ) -> None:
        """Inits the class with a list of filesystem nodes to ignore.

        Args:
            settings (List[str]): List of filesystem nodes to ignore.
            threshhold (int, optional): max size (bytes) of folders to delete (all directories less than). Defaults to 1 * constants.MEGABYTE.
        """
        self.filenode_extensions = settings
        self.threshold = threshhold

    def start(self, path: Path, operation_mode: int) -> None:
        """_summary_

        Args:
            operation_mode (int): User-selectable, chooses app action
            path (Path): User-selectable, chooses Path for action
        """
        self.operation_mode = operation_mode
        if self.operation_mode == App_Modes.DELETE_EMPTYLIKE_DIRS.value:
            self.delete_emptylike_directories(self.threshold, path)
        elif self.operation_mode == App_Modes.DELETE_UNPACKED_ARCHIVES.value:
            self.delete_unpacked_archives(path)
        elif self.operation_mode == App_Modes.EXTRACT_ARCHIVES.value:
            self.extract_archives(path)
        elif self.operation_mode == App_Modes.REMOVE_NESTED_DIRECTORIES.value:
            nested_dirs: list[Path] = helpers.find_nested_directories(path)
            for dir in nested_dirs:
                self.remove_nested_directory(dir)
                self.remove_nested_directory(dir, delete_only=True)

    # TODO: move print archives from here, call it somehow differently, maybe return something
    def extract_archives(self, path: Path) -> None:
        """Finds all archives in a path (non-recursive) and extracts them to the same directory.

        Args:
            path (Path): Path to look for and extract archives to.
        """
        archives: dict[Path, int] = helpers.find_archives(path)
        sorted_by_size_desc = dict(
            sorted(archives.items(), key=lambda x: x[1], reverse=True)
        )
        printer.print_items(sorted_by_size_desc, bcolors.ENDC)
        os.chdir(path)
        for a in archives:
            if not Path(a.stem).is_dir():
                os.mkdir(a.stem)
            patoolib.extract_archive(str(a), outdir=rf"{a.stem}\.", verbosity=0)  # type: ignore

    # TODO: Move the printing elsewhere, maybe has to return the list of archives?
    # TODO: Move user input somewhere else - maybe first input, then check, then action
    # TODO: Check for size of folders, so that it doesn't delete an empty folder.
    def delete_unpacked_archives(self, path: Path):
        """Looks foldernames with the name of archives in directory. Lists all matches and asks user to delete them.

        Args:
            path (Path): path to archives
        """
        archives_to_delete: dict[Path, int] = helpers.find_extracted_archives(path)
        printer.print_unpacked_archives(archives_to_delete, path)
        if len(archives_to_delete) > 0:
            delete_files: bool = (
                True
                if input(
                    'delete extracted archives? Press "y" to confirm or something else to decline: '
                )
                == "y"
                else False
            )
            if delete_files:
                helpers.delete_items(archives_to_delete)

    def delete_emptylike_directories(self, threshold: int, path: Path) -> None:
        """Deletes emptylike directories - those that are empty or contain only thumbs.db; Bear in mind that it can delete something unintended, look closely at the printed list.

        Args:
            threshold (int): file size threshold in MiB. Anything less than that and not in exception list (settings) will be deleted
            path (Path): base dir in which to search for archives.
        """
        dirs_to_delete: dict[Path, int] = helpers.filter_by_size(
            path,
            constants.EMPTY_DIR_GLOB,
            self.filenode_extensions,
            threshold,
        )
        printer.print_emptylike_folders(dirs_to_delete, path)
        if len(dirs_to_delete) > 0:
            delete_dirs: bool = (
                True
                if input(
                    'delete emptylike dirs? Press "y" to confirm or something else to decline: '
                )
                == "y"
                else False
            )
            if delete_dirs:
                helpers.delete_empty_dirs(dirs_to_delete)  # type: ignore

    # TODO: Test it, I am not sure it works
    def remove_nested_directory(self, path: Path, delete_only: bool = False) -> None:

        dirs: list[Path] = [p for p in list(path.glob("*")) if p.is_dir()]
        print("Listing nested directories")
        print("Nested dir is empty") if not dirs else [print(f"{x}") for x in dirs]

        # [print(f".....{x}") for x in items_to_move]

        # empty directory
        if Path.exists(path) and not dirs:
            os.rmdir(path)
            print(f"path {path} removed")
            if delete_only:
                return

        for item in dirs:
            destination = item.parents[1]
            if os.path.isfile(item):
                shutil.move(item, destination)
            else:
                # dir_size = sum(
                #     file.stat().st_size for file in Path(item.parent).rglob("*")
                # )
                # if dir_size == 0:
                #     shutil.rmtree(item)
                shutil.move(item, destination, copy_function=shutil.copytree)
