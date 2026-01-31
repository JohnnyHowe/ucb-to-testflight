import argparse
from pathlib import Path
from typing import Callable
from testflight_uploader.upload_configuration import UploadConfiguration
from testflight_uploader.testflight_uploader import TestflightUploader
from testflight_uploader.app_store_connect_key_creator import create_from_environment_variables as create_api_key_file


def main():
    args = _parse_command_line_args()
    verbose = args.verbose

    is_api_key_auto_generated = args.api_key_path is None
    api_key_path = get_api_key_path(args.api_key_path)

    # Run the uploader safely
    def get_configuration_and_upload():
        configuration = UploadConfiguration(api_key_path, verbose)
        uploader = TestflightUploader(configuration, verbose)
        uploader.upload()
    error = _run_safe(get_configuration_and_upload)

    # Delete key if this script made it
    if is_api_key_auto_generated and api_key_path.exists():
        api_key_path.unlink()

    # Raise an error if there was one
    if error:
        raise error


def _parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-key-path",
        type=Path,
        help="Path to API key JSON file",
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=True,   # ON by default
        help="Enable verbose output (default)",
    )
    parser.add_argument(
        "--no-verbose",
        dest="verbose",
        action="store_false",
        help="Disable verbose output",
    )
    return parser.parse_args()


def get_api_key_path(user_provided) -> Path:
    if user_provided is not None:
        return Path(user_provided) 
    else:
        return create_api_key_file()


def _run_safe(func: Callable):
    try:
        func()
        return None
    except Exception as exception:
        return exception


if __name__ == "__main__":
    main()