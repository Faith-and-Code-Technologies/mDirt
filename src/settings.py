import json
import os

DEFAULT_SETTINGS = {
    "general": {
        "auto_save_interval": "5 Minutes",
        "open_last_project": True,
        "workspace_path": "default",
        "language": "English",
    },
    "appearance": {
        "theme": "Earthy Dark",
        "font_size": 9,
        "show_tips": True
    },
    "editor": {
        "confirm_deletes": True,
        "enable_experiments": False
    },
    "file_export": {
        "default_export_location": "default",
        "pack_format_override": "",
        "verbose_logging": False,
    },
    "network": {
        "check_updates": True,
        "custom_update_url": "",
        "get_betas": False
    },
    "data": {
        "last_project_path": "",
        "last_project_namespace": ""
    }
}


class SettingsManager:
    def __init__(self, settings_path="settings.json", beta_path="src/version.json"):
        self.settings_path = settings_path
        self.beta_path = beta_path
        self.settings = self.load_settings()
        self.save_settings()

    def load_settings(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r") as file:
                    return json.load(file)
            except Exception as e:
                print(f"Failed to load settings, using defaults. Error: {e}")
        return DEFAULT_SETTINGS.copy()

    def save_settings(self):
        try:
            with open(self.settings_path, "w") as file:
                json.dump(self.settings, file, indent=4)
        except Exception as e:
            print(f"Failed to save settings. Error: {e}")

    def get(self, category, key):
        if category == "network" and key == "get_betas":
            return self.get_beta()
        return self.settings.get(category, {}).get(key, DEFAULT_SETTINGS[category][key])

    def set(self, category, key, value):
        if category == "network" and key == "get_betas":
            self.handle_beta_change(value)
            return

        if category not in self.settings:
            self.settings[category] = {}

        self.settings[category][key] = value

    def reset_to_defaults(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.save_settings()

    def handle_beta_change(self, value):
        try:
            data = {}
            if os.path.exists(self.beta_path):
                with open(self.beta_path, "r") as file:
                    data = json.load(file)

            data["INCLUDE_BETA"] = value  # Correct field name
            with open(self.beta_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Failed to update beta setting. Error: {e}")

    def get_beta(self):
        try:
            if os.path.exists(self.beta_path):
                with open(self.beta_path, "r") as file:
                    data = json.load(file)
                    return data.get("INCLUDE_BETA", DEFAULT_SETTINGS["network"]["get_betas"])
        except Exception as e:
            print(f"Failed to read beta setting. Error: {e}")
        return DEFAULT_SETTINGS["network"]["get_betas"]
