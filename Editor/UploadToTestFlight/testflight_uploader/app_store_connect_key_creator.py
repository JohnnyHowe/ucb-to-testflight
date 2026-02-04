"""
Creates [cwd]/AppStoreConnectKey.json from environment variables in the format (without newlines):
{
    "key_id": $APP_STORE_CONNECT_API_KEY_ID,
    "issuer_id": $APP_STORE_CONNECT_API_KEY_ISSUER_ID,
    "key": $APP_STORE_CONNECT_API_KEY_ALL_CONTENT
}
"""
import json
from pathlib import Path
from env_accessor import *


def create_api_key_file(file_path: Path = Path("AppStoreConnectAPIKey.json")) -> Path:
    """ Returns file path. """
    data = _get_data()
    with open(file_path, "w") as f:
        json.dump(data, f)
    return file_path


def _get_data() -> dict:
    return {
        "key_id": APP_STORE_CONNECT_API_KEY_ID,
        "issuer_id": APP_STORE_CONNECT_API_KEY_ISSUER_ID,
        "key": APP_STORE_CONNECT_API_KEY_CONTENT
    }