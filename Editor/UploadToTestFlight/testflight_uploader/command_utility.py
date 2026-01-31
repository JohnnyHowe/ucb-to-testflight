import subprocess
import time
from typing import Callable


class CommandOutput:
    stdout_lines: list = []
    stderr_lines: list = []
    return_code: int = -1
    reason: str = ""

    def success(self) -> bool:
        return self.return_code == 0


class CommandRunner:
    command: list
    log_prefix: str = ""
    timeout_seconds: int = 600
    stdout_parser: Callable
    output: CommandOutput = CommandOutput()
    verbose = False

    def __init__(self, command: list) -> None:
        self.command = command
        self.stdout_parser = CommandRunner._do_nothing

    def execute(self) -> None:
        self.command_output = CommandOutput()
        start_time = time.time()

        process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        assert process.stdout is not None

        def terminate():
            process.terminate()
            assert process.stdout is not None
            process.stdout.close()

        for line in process.stdout:
            self._log_stdout(line)
            self.command_output.stdout_lines.append(line)

            parser_result = self.stdout_parser(line)
            if parser_result is not None:
                terminate()
                self.command_output.reason = parser_result
                return 

            if time.time() - start_time > self.timeout_seconds:
                process.kill()
                terminate()
                self.command_output.reason = "Timeout"
                self.command_output.return_code = 1
                return 

        process.wait()
        self.command_output.return_code = process.returncode

    def _log_stdout(self, line: str):
        if self.verbose:
            print(f"\033[0m[CommandRunner]\033[0m {line}", end="")
            

    @staticmethod
    def _do_nothing(*args):
        pass


def pretty_command(command: list, flag_separator:str="\t") -> str:
    result = ""
    for item in command:
        is_flag = item.startswith("-")
        if is_flag:
            result += "\\\n" + flag_separator

        quote_item = "\n" in result and not is_flag
        if quote_item:
            result += f"\"{item}\" " 
        else:
            result += f"{item} " 
    return result