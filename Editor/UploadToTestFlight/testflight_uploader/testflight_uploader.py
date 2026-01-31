from .command_utility import *
from .upload_configuration import UploadConfiguration


class TestflightUploader:
    verbose: bool
    last_altool_output = []
    configuration: UploadConfiguration

    def __init__(self, configuration: UploadConfiguration, verbose=False) -> None:
        self.verbose = verbose
        self.configuration = configuration

    def upload(self):
        self._log("TestFlightUploader started...")
        self._log(self.configuration)
        self._log(pretty_command(self._get_upload_command()))

        for attempt_number in range(self.configuration.max_upload_attempts):
            self._log(f"Upload attempt {attempt_number + 1} of {self.configuration.max_upload_attempts}")
            success = self._try_upload()
            if success:
                return 0

        self._log("Out of upload attempts!")
        return 1
            
    def _try_upload(self) -> bool:
        upload_command = self._get_upload_command()
        self.last_altool_output = []

        runner = CommandRunner(upload_command)
        runner.verbose = self.verbose
        runner.stdout_parser = lambda line: self._capture_command_output(line)
        runner.execute() 
    
        success = runner.output.success()

        if success:
            self._log("Upload succeeded!", "#00FF00")
        else:
            self._log(f"Upload failure: \"{runner.output.reason}\", return code={runner.output.return_code}", "#FF0000")
        
        return success

    def _get_upload_command(self) -> list:
        command = ["fastlane", "pilot", "upload"]
        command += ["-i", str(self.configuration.ipa_path)]
        command += ["--api_key_path", str(self.configuration.app_store_key_path)]
        command += ["--changelog", self._read_changelog()]

        if self.configuration.test_groups:
            if self.configuration.test_groups.strip() != "":
                command += ["--groups", self.configuration.test_groups]

        command += ["--verbose"]
        return command

    def _read_changelog(self) -> str:
        with open(self.configuration.changelog_path, "r") as file:
            return file.read()

    def _capture_command_output(self, line: str):
        if "[altool]" in line:
            self.last_altool_output.append(line)
            return

        if len(self.last_altool_output) == 0:
            return

        if line.strip() == "":
            return

        # TODO check for error in altool

        return

    def _log(self, text, color_hex=None) -> None:
        RESET = "\033[0m"
        prefix = "[TestFlightUploader]"
        if self.verbose:
            color = TestflightUploader.hex_to_ansi(color_hex) if color_hex else ""
            print(f"{prefix} {color}{text}{RESET if color else ''}")

    @staticmethod
    def hex_to_ansi(hex_color: str) -> str:
        """Convert hex color (#RRGGBB) to ANSI escape sequence."""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"\033[38;2;{r};{g};{b}m"  # 24-bit foreground color