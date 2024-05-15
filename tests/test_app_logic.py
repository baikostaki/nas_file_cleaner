from pathlib import Path
#TODO: Use fixtures and rewrite all current test from unittest to pytest
def seed_empty_directories(path: Path) -> None:
    d1: Path = Path(path, "lvl1/", "lvl2/", "lvl3/")
    d2: Path = Path(path, ".thumb/")
    d1.mkdir(parents=True)
    d2.mkdir()

def seed_files_in_dirtree(path: Path) -> None:
    items: list[Path] = [item for item in path.glob('*')]
    
    
    [dir for dir in path.glob('*')]

