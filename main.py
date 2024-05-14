from pathlib import Path
import command_parser
from helpers import Helper, App_Modes
from constants import Constants
from prompt import CmdPrompt

def main() -> None:
    threshold: int = 1 * Constants.MEGABYTE
    prompt = CmdPrompt()
    print(r"choose a path from list or enter a new one")
    prompt.print_paths()
    input_path: str = input()
    if Helper.is_int(input_path):
        input_path: str = prompt.retrieve_path_by_index(int(input_path))
    else:
        prompt.store_path(input_path)

    curr_path: Path = Path(input_path.rstrip())
    prompt.print_commands()
    operation_mode: int = int(input())
    cmd = command_parser.CommandParser()

    if operation_mode == App_Modes.DELETE_EMPTYLIKE_DIRS.value:
        cmd.delete_emptylike_directories(threshold, curr_path)
    elif operation_mode == App_Modes.DELETE_UNPACKED_ARCHIVES.value:
        cmd.delete_unpacked_archives(curr_path)
    elif operation_mode == App_Modes.EXTRACT_ARCHIVES.value:
        cmd.extract_archives(curr_path)
    elif operation_mode == App_Modes.REMOVE_NESTED_DIRECTORIES.value:
        nested_dirs: list[Path] = Helper.find_nested_directories(curr_path)
        for dir in nested_dirs:
            cmd.remove_nested_directory(dir)
            cmd.remove_nested_directory(dir, delete_only=True)

#TODO: Fix unpacking - won't unpack if already unpacked + somehow got stuck at WiAB-Chapter3-pc.zip - for others it created only empty dirs
#TODO: _saves & html_saves should be added to file with excluded dirnames or better add logic to search for commonn empty dir patterns (maybe .save whitelist) first and then according to size
if __name__ == "__main__":
    main()
