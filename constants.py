from pathlib import Path

class Constants:
    # PATH:str = r'Z:\Movies'
    # PATH:str = r'tmpvnysder_'
    PATH:Path = Path(r'Z:\pron')
    # PATH:Path = Path(r'C:\Gamez')
    # PATH:str = r'C:\Users\konst\Downloads'
    
    KILOBYTE:int = 1024
    MEGABYTE:int = KILOBYTE * 1024
    GIGABYTE:int = MEGABYTE * 1024

    FILE_SIZE_THRESHOLD: int = 3 * MEGABYTE
    FILTER_SUFFIXES:list[str] = ['.srt', '.sub', '.thumb']
    FILE_GLOB: str = r'*.*/'
    EMPTY_DIR_GLOB: str = r'*'
    ARCHIVE_SUFFIXES: list[str] = ['.rar', '.zip', '.7z']
    ARCHIVER_PATH: str = r'C:\Portable Program Files\7zr.exe'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'