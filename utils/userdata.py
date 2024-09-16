import os
import json
from typing import Any, Dict, List, Union

# Define available settings with their default values and types
AVAILABLE_SETTINGS: Dict[str, Dict[str, Union[Any, type]]] = {
    "Global: Compact mode": {"default": False, "type": bool},
    # rolling
    "Rolling: Default roll": {"default": "1d100", "type": str},
    # define
    "Define: English-only": {"default": False, "type": bool},
}

def get_available_settings() -> List[str]:
    return list(AVAILABLE_SETTINGS.keys())

def get_setting_type(setting: str) -> type:
    if setting not in AVAILABLE_SETTINGS:
        raise ValueError(f"Invalid setting: {setting}")
    return AVAILABLE_SETTINGS[setting]["type"]

def get_user_settings(user_id: int) -> Dict[str, Any]:
    file_path = f'data/users/{user_id}.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            user_settings = json.load(f)
        # Check for and add any new fields
        updated = False
        for key, value in AVAILABLE_SETTINGS.items():
            if key not in user_settings:
                user_settings[key] = value["default"]
                updated = True
        if updated:
            _save_user_settings(user_id, user_settings)
        return user_settings
    else:
        # Create new user with default settings
        user_settings = {k: v["default"] for k, v in AVAILABLE_SETTINGS.items()}
        _save_user_settings(user_id, user_settings)
        return user_settings

def change_user_setting(user_id: int, setting: str, value: Any) -> None:
    if setting not in AVAILABLE_SETTINGS:
        raise ValueError(f"Invalid setting: {setting}")

    expected_type = AVAILABLE_SETTINGS[setting]["type"]
    if not isinstance(value, expected_type):
        raise TypeError(f"Invalid type for setting '{setting}'. Expected {expected_type.__name__}, got {type(value).__name__}")

    user_settings = get_user_settings(user_id)  # This will add any new fields
    user_settings[setting] = value
    _save_user_settings(user_id, user_settings)

def _save_user_settings(user_id: int, settings: Dict[str, Any]) -> None:
    file_path = f'data/users/{user_id}.json'
    with open(file_path, 'w') as f:
        json.dump(settings, f, indent=2)

# Example usage:
if __name__ == "__main__":
    # Get all available settings
    print("Available settings:", get_available_settings())

    # Get a user's settings (creates new user if not exists)
    print("Initial user settings:", get_user_settings(1))

    # Change a user setting
    change_user_setting(1, "compact_rolling", True)

    # Get updated user settings
    print("Updated user settings:", get_user_settings(1))

    # Simulate adding a new field to AVAILABLE_SETTINGS
    AVAILABLE_SETTINGS["foo"] = {"default": "bar", "type": str}

    # Get user settings again, which should now include the new field
    print("User settings after adding new field:", get_user_settings(1))

    # Try to change an invalid setting
    try:
        change_user_setting(1, "invalid_setting", "value")
    except ValueError as e:
        print(f"Error: {e}")

    # Try to change an invalid setting
    try:
        change_user_setting(1, "compact_rolling", "value")
    except TypeError as e:
        print(f"Error: {e}")
