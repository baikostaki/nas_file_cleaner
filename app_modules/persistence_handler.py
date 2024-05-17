from typing import List


# TODO: Test it
class PersistenceHandler:
    """
    Handles the reading from and writing to a txt file, serving as a command history from previous runs

    """

    paths: List[str] = [str()]
    file_with_paths: str = str()

    def __init__(self, file_with_paths: str):
        """
        Reads file with stored paths from prevoius execution from disk and loads it into memory.
        File must contain one path on each line, as strings.
        Args:
            file_with_paths (str): path to file, e.g. "path_history.txt"
        """
        self.load_paths_from_file(file_with_paths)
        self.file_with_paths = file_with_paths

    def load_paths_from_file(self, file_with_paths: str):
        """_summary_

        Args:
            file_with_paths (str): Path to persistent file
        """
        with open(file_with_paths, "r") as f:
            self.paths: list[str] = f.readlines()
        return self.paths

    def store_path(self, path: str) -> None:
        """Adds path to persistent file and after that to path memory object

        Args:
            path (str): _description_
        """
        if path not in self.paths:
            print("Path already saved!")
            return

        if path != "\n":
            with open(self.file_with_paths, "a") as f:
                f.write(f"{path}" + "\n")
            self.paths.append(path)

    def retrieve_path_by_index(self, index: int) -> str:
        """Retrieves path by the index of printed paths.

        Args:
            index (int): index of chosen command from list

        Raises:
            IndexError: Safeguards against invalid index

        Returns:
            str: Returns the path, corresponding to index
        """
        if len(self.file_with_paths) >= index:
            return self.file_with_paths[index]
        else:
            raise IndexError("Please choose a valid index")

    def find_line_number_in_paths(self, path: str) -> int:
        """Queries path object for a path and returns its index

        Args:
            path (str): _description_

        Returns:
            int: _description_
        """
        return self.paths.index(path)

    # was == 1, not sure why
    def print_paths(self) -> None:
        """Prints persistent paths to user"""
        if len(self.paths) == 0:
            print("no paths saved.")
        for index, value in enumerate(self.paths):
            print(f"{index}: {value.strip()}")
