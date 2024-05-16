# TODO: refactor to read file once or maybe twice, it makes no sense to read it and close it 3-4 times


def print_commands() -> None:
    print("Please choose one of the following:")
    print("1: delete empty-like folders")
    print("2: delete already unpacked archives")
    print("3: unpack archives")
    print("4: remove nested folders after unpacking")
    print("5: options 3 and 4 together")


def store_path(path: str) -> None:
    if path != "\n":
        with open("path_history.csv", "a") as f:
            f.write(f"{path}" + "\n")


def retrieve_path_by_index(index: int) -> str:
    with open("path_history.csv", "r") as f:
        lines: list[str] = f.readlines()
        if len(lines) >= index:
            return lines[index]
        else:
            raise IndexError("Please choose a valid index")


def find_line_number_in_paths(path: str) -> int:
    with open("path_history.csv", "r") as f:
        lines: list[str] = [line.rstrip() for line in f.readlines()]
        if path in lines:
            return lines.index(path)
        return -1


def print_paths() -> bool:
    with open("path_history.csv") as f:
        lines: list[str] = f.readlines()
        if lines:
            for index, value in enumerate(lines):
                print(f"{index}: {value.strip()}")
            return True
        else:
            print("no paths saved.")
            return False
