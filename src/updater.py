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

class ModuleGrabber:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def update_module(self, module_name: str, zip_filename: str) -> bool:
        zip_url = f"{self.base_url}/{zip_filename}"
        response = requests.get(zip_url)
        if response.status_code != 200:
            return False

        temp_extract_path = f"temp_update/{module_name}"

        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(temp_extract_path)

            extracted_folder = os.path.join(temp_extract_path, module_name)
            target_folder = os.path.join("src", "generation", module_name)

            if os.path.exists(target_folder):
                shutil.rmtree(target_folder)

            shutil.move(extracted_folder, target_folder)
            shutil.rmtree("temp_update")
            return True
        except Exception:
            if os.path.exists("temp_update"):
                shutil.rmtree("temp_update")
            return False


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