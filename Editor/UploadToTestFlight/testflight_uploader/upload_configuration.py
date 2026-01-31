import json
import os
from pathlib import Path
from testflight_uploader.build_file_finder import find_build_file_path


class UploadConfiguration:

    ipa_path: Path
    app_store_key_path: Path
    changelog_path: Path
    test_groups = None
    max_upload_attempts: int = 10

    verbose: bool

    def __init__(self, api_key_path: Path, verbose = False):
        self.verbose = verbose
        self.app_store_key_path = api_key_path
        self._populate()
        self.verify()

    def _populate(self):
        self._log("TODO: expose changelog somewhere")
        self.changelog_path = Path("Assets/Editor/CICD/newest_changelog.txt")
        self.ipa_path = find_build_file_path(".ipa", self.verbose)

        self.test_groups = os.getenv("TEST_GROUPS", None)
        if self.test_groups is None:
            self._log(f"TEST_GROUPS environment variable not set. No test groups will be added.")

        self.max_upload_attempts = self._get_max_upload_attempts(self.max_upload_attempts)

    def _get_max_upload_attempts(self, fallback=10) -> int:
        key = "MAX_UPLOAD_ATTEMPTS"
        if not key in os.environ:
            self._log(f"$MAX_UPLOAD_ATTEMPTS not set. Falling back to {fallback}")
            return fallback

        try:
            env_value = os.getenv("MAX_UPLOAD_ATTEMPTS", str(self.max_upload_attempts))
            parsed_value = int(env_value)
        except ValueError:
            self._log(f"Cannot parse $MAX_UPLOAD_ATTEMPTS as int ({env_value}). Falling back to {fallback}")
            return fallback

        if parsed_value <= 0:
            self._log(f"$MAX_UPLOAD_ATTEMPTS needs to be at least 1! Got ({env_value}). Falling back to {fallback}")
            return fallback

        return parsed_value

    def verify(self) -> None:
        self._verify_is_file(self.app_store_key_path, "App Store Connect key")
        self._verify_app_store_key_format()
        self._verify_is_file(self.changelog_path, "changelog")
        self._verify_is_file(self.ipa_path, "build file")

    def _verify_app_store_key_format(self):
        with open(self.app_store_key_path, "r") as file:
            self._verify_app_store_key_content(file.read())

    def _verify_is_file(self, path: Path, data_name: str):
        if not self.app_store_key_path.exists():
            raise FileNotFoundError(f"Error loading {data_name}! Nothing found at {path}")

        if not self.app_store_key_path.is_file():
            raise FileNotFoundError(f"Error loading {data_name}. Item at {path} is not a file!")

    def _verify_app_store_key_content(self, content: str):
        data = json.loads(content)
        self._verify_dictionary_value_not_env_reference("key_id", data, str(self.app_store_key_path))
        self._verify_dictionary_value_not_env_reference("issuer_id", data, str(self.app_store_key_path))
        self._verify_dictionary_value_not_env_reference("key", data, str(self.app_store_key_path))
        
    def _verify_dictionary_value_not_env_reference(self, key: str, data: dict, data_name: str):
        if not key in data:
            raise KeyError(f"\"{key}\" not found in \"{data_name}\"")
        key_id = data[key]
        if key_id.startswith("$"):
            raise ValueError(f"{data_name} \"{key}\" invalid. Got \"{key_id}\"")

    def _log(self, text: str) -> None:
        if self.verbose:
            print(f"[UploadConfiguration] {text}")

    def __str__(self) -> str:
        indent = "\t"

        result = "Upload configuration: {\n"

        for item in ["ipa_path", "changelog_path", "app_store_key_path", "max_upload_attempts", "test_groups"]:
            if item == "":
                result += "\n"
                continue
            result += f"{indent}{item}: {getattr(self, item)}\n"

        result += "}"

        return result