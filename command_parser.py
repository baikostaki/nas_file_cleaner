from pathlib import Path
import shutil
from helpers import Helper, Printer
from constants import bcolors, Constants
import os
import patoolib  # type: ignore

class CommandParser:
    def extract_archives(self, curr_path: Path) -> None:
        archives: dict[Path, int] = Helper.find_archives(curr_path)
        sorted_by_size_desc = dict(
            sorted(archives.items(), key=lambda x: x[1], reverse=True)
        )
        Printer.print_items(sorted_by_size_desc, bcolors.ENDC)
        os.chdir(curr_path)
        for a in archives:
            if not Path(a.stem).is_dir():
                os.mkdir(a.stem)

        patoolib.extract_archive(str(a), outdir=rf"{a.stem}\.")  # type: ignore

    def delete_unpacked_archives(self, curr_path: Path):
        archives_to_delete: dict[Path, int] = Helper.find_extracted_archives(curr_path)
        Printer.print_unpacked_archives(archives_to_delete, curr_path)
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
                Helper.delete_items(archives_to_delete)

    def delete_emptylike_directories(self, threshold: int, curr_path: Path) -> None:
        dirs_to_delete: dict[Path, int] = Helper.filter_by_size(
            curr_path, Constants.EMPTY_DIR_GLOB, threshold
        )
        Printer.print_emptylike_folders(dirs_to_delete, curr_path)
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
                Helper.delete_empty_dirs(dirs_to_delete)  # type: ignore

    def remove_nested_directory(self, path: Path, delete_only: bool = False) -> None:
        dir_contents = list(path.glob("*"))
        print('Listing nested directories')
        print('Nested dir is empty') if not dir_contents else [print(f'{x}') for x in dir_contents]
        
        
        # [print(f".....{x}") for x in items_to_move]

        # empty directory
        if Path.exists(path) and not dir_contents:
            os.rmdir(path)
            print(f'path {path} removed')
            if delete_only:
                return

        for item in dir_contents:
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

        # sum(file.stat().st_size for file in Path(folder).rglob("*"))

        
