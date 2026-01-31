"""
Creates [cwd]/AppStoreConnectKey.json from environment variables in the format (without newlines):
{
    "key_id": $APP_STORE_CONNECT_API_KEY_KEY_ID,
    "issuer_id": $APP_STORE_CONNECT_API_KEY_ISSUER_ID,
    "key": $APP_STORE_CONNECT_API_KEY_ALL_CONTENT
}
"""
import json
import os
from pathlib import Path


def create_from_environment_variables(file_path: Path = Path("AppStoreConnectAPIKey.json")) -> Path:
    data = get_data()
    with open(file_path, "w") as f:
        json.dump(data, f)
    return file_path


def get_data() -> dict:
    return {
        "key_id": get_environment_variable("APP_STORE_CONNECT_API_KEY_KEY_ID"),
        "issuer_id": get_environment_variable("APP_STORE_CONNECT_API_KEY_ISSUER_ID"),
        "key": get_environment_variable("APP_STORE_CONNECT_API_KEY_ALL_CONTENT").replace("\n", "\\n")
    }


def get_environment_variable(key: str) -> str:
    if not key in os.environ:
        raise KeyError(f"No environment variable \"{key}\" exists!")
    return os.environ[key]


if __name__ == "__main__":
    # TODO use command line args
    create_from_environment_variables(Path("AppStoreConnectKey.json"))