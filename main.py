from pathlib import Path
from app_modules.persistence_handler import PersistenceHandler
from app_modules.command_parser import Commander
from app_modules.user_input_handler import InputHandler
from app_modules.settings import Settings


# TODO: move those thing below to CommandParser.parse_commands and create the parser as a Module, instead of class, don't think it needs to be instantiated.
def main() -> None:
    settings = Settings()
    persistence = PersistenceHandler("app_modules/path_history.txt")
    cmd = Commander(settings.get_all_suffixes())
    input_handler = InputHandler(cmd, persistence)
    user_input: tuple[Path, int] = input_handler.start()
    cmd.start(*user_input)

    # threshold: int = 1 * constants.MEGABYTE
    # print(r"choose a path from list or enter a new one")
    # prompt.print_paths()
    # input_path: str = input()
    # if helpers.is_int(input_path):
    #     input_path: str = prompt.retrieve_path_by_index(int(input_path))
    # else:
    #     prompt.store_path(input_path)

    # curr_path: Path = Path(input_path.rstrip())
    # prompt.print_commands()
    # operation_mode: int = int(input())
    # cmd = Commander(helpers.settings.get_all_suffixes())


if __name__ == "__main__":
    main()
