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
from PySide6.QtWidgets import QMessageBox

def alert(message):
    messageBox = QMessageBox()
    messageBox.setIcon(QMessageBox.Icon.Information)
    messageBox.setText(message)
    messageBox.setWindowTitle("Alert")
    messageBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    messageBox.exec()

class ModuleGrabber:
    def __init__(self, base_url: str, download_folder: str = "src/generation", data_folder: str = "lib"):
        self.base_url = base_url.rstrip("/")
        # If bundled into an exe, set paths to the '_internal' folder
        if getattr(sys, 'frozen', False):
            self.download_folder = os.path.join(os.path.dirname(sys.executable), '_internal', 'src', 'generation')
            self.data_folder = os.path.join(os.path.dirname(sys.executable), '_internal', 'lib')
        else:
            self.download_folder = download_folder
            self.data_folder = data_folder

    def update_module(self, version: str) -> bool:
        formatted_version = self.format_version(version)
        zip_url = f"{self.base_url}/modules/{formatted_version}.zip"
        response = requests.get(zip_url)
        if response.status_code != 200:
            alert(f"Error downloading mDirt Modules. Failed with status code {response.status_code}. Check your internet connection and try again. If the problem persists, submit an issue here: https://github.com/Faith-and-Code-Technologies/mDirt-2/issues")
            return False
        extracted = self._extract_zip(response.content, formatted_version)
        data_downloaded = self.download_data_file(version)
        return extracted and data_downloaded

    def download_data_file(self, version: str) -> bool:
        data_url = f"{self.base_url}/lib/{version}_data.json"
        response = requests.get(data_url)
        if response.status_code != 200:
            alert(f"Error downloading mDirt Data. Failed with status code {response.status_code}. Check your internet connection and try again. If the problem persists, submit an issue here: https://github.com/Faith-and-Code-Technologies/mDirt-2/issues")
            return False
        try:
            # Ensure 'lib' is created at the root level of '_internal' when bundled
            os.makedirs(self.data_folder, exist_ok=True)
            target_path = os.path.join(self.data_folder, f"{version}_data.json")
            with open(target_path, "wb") as f:
                f.write(response.content)
            return True
        except Exception:
            alert(f"Error downloading mDirt Modules. Check your internet connection and try again. If the problem persists, submit an issue here: https://github.com/Faith-and-Code-Technologies/mDirt-2/issues")
            return False

    def _extract_zip(self, zip_data: bytes, module_name: str) -> bool:
        try:
            # Ensure 'src/generation/module_name' is created at the root level of '_internal' when bundled
            target_dir = os.path.join(self.download_folder, module_name)
            os.makedirs(target_dir, exist_ok=True)
            with zipfile.ZipFile(BytesIO(zip_data)) as zip_ref:
                zip_ref.extractall(target_dir)
            return True
        except Exception:
            alert(f"Error extracting mDirt Modules. Check your internet connection and try again. If the problem persists, submit an issue here: https://github.com/Faith-and-Code-Technologies/mDirt-2/issues")
            return False

    def format_version(self, version: str) -> str:
        return f"v{version.replace('.', '_')}"


class Updater:
    def __init__(self, repo_url: str, current_version: str):
        self.repo_url = repo_url.rstrip("/")
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{self.repo_url.split('/')[-2]}/{self.repo_url.split('/')[-1]}/releases/latest"
        
    def get_latest_release_info(self):
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

        asset_url = next(
            (asset["browser_download_url"] for asset in release_info["assets"] if asset["name"].endswith(".zip")), 
            None
        )
        if not asset_url:
            return False

        try:
            response = requests.get(asset_url, stream=True)
            if response.status_code != 200:
                return False

            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall("app_update")

            extracted_exe_path = os.path.join("app_update", exe_name)
            current_exe_path = sys.argv[0]

            if not os.path.exists(extracted_exe_path):
                shutil.rmtree("app_update")
                return False
            
            internal_folder = os.path.join("app_update", "_internal")
            if os.path.exists(internal_folder):
                target_internal_folder = os.path.join("_internal")
                if os.path.exists(target_internal_folder):
                    shutil.rmtree(target_internal_folder)
                shutil.move(internal_folder, target_internal_folder)

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