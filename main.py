from pathlib import Path
from app_modules.persistence_handler import PersistenceHandler
from app_modules.command_parser import Commander
from app_modules.user_input_handler import InputHandler
from app_modules.settings import Settings


def main() -> None:
    settings = Settings()
    persistence = PersistenceHandler("app_modules/path_history.txt")
    cmd = Commander(settings.get_all_suffixes())
    input_handler = InputHandler(cmd, persistence)
    user_input: tuple[Path, int] = input_handler.start()
    cmd.start(*user_input)


if __name__ == "__main__":
    main()
