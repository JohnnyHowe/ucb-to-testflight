"""
Helper to find the Unity build file.

Made for Unity Cloud Build .ipa and .aab files but will search CWD if the UCB environment variables don't exist.
Executable path is OUTPUT_DIRECTORY/executable_name.type for UCB.
PS. UCB does expose the full path but it's in an API that I can't be bothered touching (https://build-api.cloud.unity3d.com/docs).
"""
import argparse
import os
from pathlib import Path
from typing import Iterator


class BuildFileFinder:
    verbose: bool
    file_extension: str
    file_path: Path

    def __init__(self, file_extension: str, verbose=False):
        self.verbose = verbose
        self._set_file_extension(file_extension)
        self._find_and_set_file()

    def _set_file_extension(self, file_extension: str) -> None:
        lowered_extension = file_extension.lower()
        if lowered_extension != file_extension:
            self._log(f"Setting file extension to lowercase. (\"{file_extension}\" -> \"{lowered_extension}\")")
            file_extension = lowered_extension

        if not file_extension.startswith("."):
            prefixed_extension = "." + file_extension
            self._log(f"Recieved extension without \".\" prefix, adding it. (\"{file_extension}\" -> \"{prefixed_extension}\")")
            file_extension = prefixed_extension

        self.file_extension = lowered_extension

    def _set_output_directory(self) -> None:
        if "OUTPUT_DIRECTORY" in os.environ:
            self._output_directory = Path(os.environ["OUTPUT_DIRECTORY"])
            self._log(f"OUTPUT_DIRECTORY environment variable found: {BuildFileFinder._get_pretty_path_string(self._output_directory)}")
        else:
            self._output_directory = Path("./")
            self._log(f"OUTPUT_DIRECTORY environment variable not set! Using {BuildFileFinder._get_pretty_path_string(self._output_directory)}")

    def _find_and_set_file(self) -> None:
        self.file_path = self._find_file()
        if self.file_path is None:
            raise FileNotFoundError(f"No {self.file_extension} found.")

    def _find_file(self) -> Path:
        def log_warning():
            self._log("TODO: implement searcher for [Bb]uild folder!")
            return None

        for searcher in [self._search_ucb_path, log_warning, self._search_everywhere]:
            path = searcher()
            if path: 
                return path

        raise FileNotFoundError(f"No {self.file_extension} file found!")

    def _search_ucb_path(self):
        """
        Get file at $OUTPUT_DIRECTORY/build_name.type
        If $OUTPUT_DIRECTORY doesn't exist or the file doesn't, return None
        """
        if not "OUTPUT_DIRECTORY" in os.environ:
            self._log(f"OUTPUT_DIRECTORY environment variable not set! Skipping UCB default location search.")
            return None
        
        output_directory = Path(os.environ["OUTPUT_DIRECTORY"])
        self._log(f"$OUTPUT_DIRECTORY environment variable found: {BuildFileFinder._get_pretty_path_string(self._output_directory)}")

        if not output_directory.exists():
            self._log(f"$OUTPUT_DIRECTORY ({BuildFileFinder._get_pretty_path_string(self._output_directory)}) doesn't exist!")
            return None
        
        return self._choose_file(list(self._search_path(output_directory)))

    def _search_everywhere(self):
        self._log("TODO: ignore unity Temp and Library folders")
        self._log(f"Searching entire working directory for {self.file_extension} file.")
        return self._choose_file(list(self._search_path(Path("./"), True)))

    def _choose_file(self, paths: list):
        if len(paths) == 0:
            self._log(f"Found 0 {self.file_extension} files")
            return None

        if len(paths) == 1:
            self._log(f"Found 1 {self.file_extension} file: {paths[0]}")
            return paths[0]

        self._log(f"Found {len(paths)} {self.file_extension} files:")
        for file_path in paths:
            self._log(f"  - {file_path}")

        self._log("TODO: choose smarter. Taking first...")
        return paths[0]

    def _search_path(self, root: Path, recursive=False) -> Iterator:
        for file_name in os.listdir(root):
            file_path = Path(os.path.join(root, file_name))

            if file_path.is_dir() and recursive:
                yield from self._search_path(file_path, recursive)

            if not file_path.is_file(): continue
            if not file_path.suffix.lower() == self.file_extension: continue

            yield file_path

    def _log(self, text: str):
        if self.verbose:
            print(BuildFileFinder._get_log_text(text))

    @staticmethod
    def _get_log_text(text: str) -> str:
        return "[BuildFileFinder] " + text

    @staticmethod
    def _get_pretty_path_string(path: Path) -> str:
        return f"{path} ({path.absolute()})"


def find_build_file_path(extension: str, verbose=False) -> Path:
    return BuildFileFinder(extension, verbose).file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "extension",
        help="File extension to search for (e.g. .aab or .ipa)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()
    print(find_build_file_path(args.extension, args.verbose))
