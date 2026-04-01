"""UCB adapter that delegates TestFlight upload execution to pyliot."""
from pathlib import Path

from pyliot.upload_to_testflight import upload_to_testflight as pyliot_upload_to_testflight
from .build_file_finder import BuildFileFinder


def upload_to_testflight(
	app_store_connect_api_key_issuer_id: str,
	app_store_connect_api_key_id: str,
	app_store_connect_api_key_content: str,
	output_directory: Path,
	changelog_path: Path,
	groups: list[str] = [],
	max_upload_attempts: int = 10,
	attempt_timeout_seconds: int = 600,
	show_fastlane_logs: bool = False
):
	with open(changelog_path, "r") as file:
		changelog = file.read()

	print("\nFound Changelog ".ljust(32, "="))
	print(changelog)
	print("=" * 32)

	ipa_path = BuildFileFinder(output_directory, ".ipa").file_path

	pyliot_upload_to_testflight(
		app_store_connect_api_key_issuer_id=app_store_connect_api_key_issuer_id,
		app_store_connect_api_key_id=app_store_connect_api_key_id,
		app_store_connect_api_key_content=app_store_connect_api_key_content,
		ipa_path=ipa_path,
		changelog=changelog,
		groups=groups,
		max_upload_attempts=max_upload_attempts,
		attempt_timeout_seconds=attempt_timeout_seconds,
		show_fastlane_logs=show_fastlane_logs
	)
