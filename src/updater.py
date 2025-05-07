################################################################
# Grabs new Minecraft Versions and mDirt Updates automatically #
################################################################

import requests
import zipfile
import io
import os
import shutil
import sys
import subprocess
from io import BytesIO

class ModuleGrabber:
    def __init__(self, base_url: str, download_folder: str = "src/generation"):
        self.base_url = base_url.rstrip("/")
        self.download_folder = download_folder

    def update_module(self, version: str) -> bool:
        formatted_version = self.format_version(version)
        zip_url = f"{self.base_url}/modules/{formatted_version}.zip"
        response = requests.get(zip_url)
        if response.status_code != 200:
            return False
        return self._extract_zip(response.content, formatted_version)

    def _extract_zip(self, zip_data: bytes, module_name: str) -> bool:
        try:
            target_dir = os.path.join(self.download_folder, module_name)
            os.makedirs(target_dir, exist_ok=True)
            with zipfile.ZipFile(BytesIO(zip_data)) as zip_ref:
                zip_ref.extractall(target_dir)
            return True
        except Exception:
            return False

    def format_version(self, version: str) -> str:
        return f"v{version.replace('.', '_')}"


class Updater:
    def __init__(self, repo_url: str, current_version: str):
        """
        :param repo_url: GitHub repo URL (e.g., 'https://github.com/user/repo')
        :param current_version: Current version of the app (e.g., '1.0.0')
        """
        self.repo_url = repo_url.rstrip("/")  # Remove trailing slashes if any
        self.current_version = current_version
        # Construct the correct API URL to fetch the latest release
        self.api_url = f"https://api.github.com/repos/{self.repo_url.split('/')[-2]}/{self.repo_url.split('/')[-1]}/releases/latest"
        
    def get_latest_release_info(self):
        """Fetch the latest release information from GitHub."""
        try:
            response = requests.get(self.api_url)
            if response.status_code != 200:
                return None
            
            release_info = response.json()
            
            return release_info
        except Exception as e:
            return None

    def is_update_available(self):
        release_info = self.get_latest_release_info()
        if release_info:
            latest_version = release_info["tag_name"]
            return latest_version > self.current_version
        return False

    def download_and_replace_app(self, exe_name: str) -> bool:
        release_info = self.get_latest_release_info()
        if not release_info:
            return False

        # Get the latest release ZIP link
        asset_url = next(
            (asset["browser_download_url"] for asset in release_info["assets"] if asset["name"].endswith(".zip")), 
            None
        )
        if not asset_url:
            return False

        try:
            # Download the release ZIP
            response = requests.get(asset_url, stream=True)
            if response.status_code != 200:
                return False

            # Extract the ZIP to a temporary folder
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall("app_update")

            # Path to the extracted files
            extracted_exe_path = os.path.join("app_update", exe_name)
            current_exe_path = sys.argv[0]

            if not os.path.exists(extracted_exe_path):
                shutil.rmtree("app_update")
                return False

            # Update all files, including the internal folder
            internal_folder = os.path.join("app_update", "_internal")
            if os.path.exists(internal_folder):
                target_internal_folder = os.path.join("_internal")
                if os.path.exists(target_internal_folder):
                    shutil.rmtree(target_internal_folder)
                shutil.move(internal_folder, target_internal_folder)

            # Replace the exe file (this requires a workaround to restart the app)
            updater_script = f"""
            import time, shutil, os
            time.sleep(1)
            shutil.copyfile(r'{extracted_exe_path}', r'{current_exe_path}')
            shutil.rmtree('app_update')
            os.startfile(r'{current_exe_path}')
            """
            with open("run_updater.py", "w", encoding="utf-8") as f:
                f.write(updater_script)

            subprocess.Popen([sys.executable, "run_updater.py"])
            sys.exit(0)
            return True
        except Exception:
            shutil.rmtree("app_update")
            return False