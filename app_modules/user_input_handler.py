from pathlib import Path
from app_modules.command_parser import Commander
from app_modules.persistence_handler import PersistenceHandler
from helper_modules import helpers


# BUG: somehow it messes up
class InputHandler:
    input_path: Path = Path()

    def __init__(
        self, cmd_parser: Commander, persistence_handler: PersistenceHandler
    ) -> None:
        self.cmd_parser: Commander = cmd_parser
        self.persistence_handler: PersistenceHandler = persistence_handler

    def print_commands(self) -> None:
        """Print all app commands for the user to use"""
        print("Please choose one of the following:")
        print("1: delete empty-like folders")
        print("2: extract archives")
        print("3: delete already unpacked archives")
        print("4: remove nested folders after unpacking")
        print("5: options 2 and 3 together NOT IMPLEMENTED YET")
        print("6: options 3 and 4 together")

    def start(self) -> tuple[Path, int]:
        """Prints message to user and takes input

        Returns:
            tuple[Path, int]: tuple with Path to directory to act upon and operation mode for the app
        """
        print(r"choose a path from list or enter a new one")
        self.persistence_handler.print_paths()
        # BUG here something bad happens with paths
        input_path: str = input()
        if helpers.is_int(input_path):
            self.input_path = self.persistence_handler.retrieve_path_by_index(
                int(input_path)
            )
        else:
            self.persistence_handler.store_path(input_path)

        curr_path: Path = Path(input_path.rstrip())
        self.print_commands()
        operation_mode: int = int(input())
        return (curr_path, operation_mode)
