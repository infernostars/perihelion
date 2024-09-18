import os
import json
from typing import Any, Dict, List, Literal, Optional, Union

# Define available settings for users
USER_AVAILABLE_DATA: Dict[str, Dict[str, Union[Any, type]]] = {
    "Global: Compact mode": {"default": False, "type": bool, 'locked': False},
    "Rolling: Default roll": {"default": "1d100", "type": str, 'locked': False},
    "Define: English-only": {"default": False, "type": bool, 'locked': False},
    "RngSim: Highscore": {"default": 0, "type": int, 'locked': True},
}

# Define available settings for guilds (currently empty)
GUILD_AVAILABLE_DATA: Dict[str, Dict[str, Union[Any, type]]] = {
}

class SettingsManager:
    """
    Handles settings like a dictionary. You cannot write new keys, but setting pre-existing keys and getting them works.

    For writes that are mostly done by the user, use `write_protected()` to protect non-setting data values.
    """
    def __init__(self, entity_type: str, entity_id: Union[int, str], available_data: Dict[str, Dict[str, Union[Any, type]]]):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.available_data = available_data
        self.file_path = f'data/{entity_type}s/{entity_id}.json'
        self._data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                settings = json.load(f)
            # Check for and add any new fields
            updated = False
            for key, value in self.available_data.items():
                if key not in settings:
                    settings[key] = value["default"]
                    updated = True
            if updated:
                self._save_data(settings)
            return settings
        else:
            # Create new entity with default settings
            settings = {k: v["default"] for k, v in self.available_data.items()}
            self._save_data(settings)
            return settings

    def _save_data(self, settings: Dict[str, Any]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(settings, f, indent=2)

    def __getitem__(self, key: str) -> Any:
        if key not in self.available_data:
            raise KeyError(f"Invalid setting: {key}")
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if key not in self.available_data:
            raise KeyError(f"Invalid setting: {key}")

        expected_type = self.available_data[key]["type"]
        if not isinstance(value, expected_type):
            raise TypeError(f"Invalid type for setting '{key}'. Expected {expected_type.__name__}, got {type(value).__name__}")

        self._data[key] = value
        self._save_data(self._data)

    def write_protected(self, key: str, value: Any) -> None:
        """Same as a direct settings[] write, but locked data fails to write. Use in direct user input."""
        if key not in self.available_data:
            raise KeyError(f"Invalid setting: {key}")

        expected_type = self.available_data[key]["type"]
        if not isinstance(value, expected_type):
            raise TypeError(f"Invalid type for setting '{key}'. Expected {expected_type.__name__}, got {type(value).__name__}")

        if self.available_data[key]["locked"]:
            raise PermissionError(f"The setting '{key}' is locked and cannot be modified.")

        self._data[key] = value
        self._save_data(self._data)

    def get_available_data_keys(self, bypass_locked: bool = True) -> List[str]:
        """Gets all keys of the database.

        Parameters
        ------------
        bypass_locked: `bool`

        If false, only shows unlocked keys."""
        if bypass_locked:
            return list(self.available_data.keys())
        else:
            return [key for key, value in self.available_data.items() if not value.get('locked', False)]

    def get_data_type(self, setting: str) -> type:
        """Gets the type of a setting by string name."""
        if setting not in self.available_data:
            raise KeyError(f"Invalid setting: {setting}")
        return self.available_data[setting]["type"]

    def get_data(self) -> Dict[str, Any]:
        """Gets a direct copy of the dictionary."""
        return self._data.copy()

class UserSettingsManager(SettingsManager):
    def __init__(self, user_id: int):
        super().__init__("user", user_id, USER_AVAILABLE_DATA)

class GuildSettingsManager(SettingsManager):
    def __init__(self, guild_id: int):
        super().__init__("guild", guild_id, GUILD_AVAILABLE_DATA)

def get_settings_manager(entity_type: Literal["user", "guild"], entity_id: int) -> SettingsManager:
    """Returns a SettingsManager based on entity type and entity id."""
    if entity_type == "user":
        return UserSettingsManager(entity_id)
    elif entity_type == "guild":
        return GuildSettingsManager(entity_id)
    else:
        raise ValueError(f"Invalid entity type: {entity_type}")
