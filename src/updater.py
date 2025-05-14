import os
import sys
import json
import zipfile
import shutil
import tempfile
import subprocess
import requests
from packaging import version
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QMessageBox, QProgressBar
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal

# --- Constants ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VERSION_FILE = os.path.join(BASE_DIR, 'version.json')

# --- Load Config ---
with open(VERSION_FILE, 'r') as f:
    config = json.load(f)

github_url = config['GITHUB_URL']
current_version = config['CURRENT_VERSION']
include_beta = config.get('INCLUDE_BETA', False)

# --- Fetch Latest Release ---
def get_latest_release(allow_beta: bool):
    url = github_url.replace("/releases/latest", "/releases")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch releases: {response.status_code}")

    releases = response.json()
    for release in releases:
        if allow_beta or not release.get("prerelease", False):
            return release

    raise Exception("No valid releases found.")

# --- Helper Threaded Worker ---
class UpdateWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal()

    def run(self):
        self.status.emit("Checking for updates...")
        try:
            release_data = get_latest_release(include_beta)
        except Exception as e:
            self.status.emit(f"Error: {str(e)}")
            return
        
        latest_tag = release_data['tag_name']
        if version.parse(latest_tag) <= version.parse(current_version):
            self.status.emit("No updates available.")
            return
        
        self.status.emit(f"New version found: {latest_tag}. Downloading...")

        zip_url = None
        zip_name = None

        for asset in release_data['assets']:
            if asset['name'].endswith('.zip'):
                zip_url = asset['browser_download_url']
                zip_name = asset['name']
                break

        if not zip_url:
            self.status.emit("No .zip asset found.")
            return

        zip_path = os.path.join(BASE_DIR, zip_name)
        with requests.get(zip_url, stream=True) as r:
            with open(zip_path, 'wb') as f:
                total = int(r.headers.get('content-length', 0))
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        self.progress.emit(int(downloaded * 100 / total))

        self.status.emit("Extracting update...")
        temp_path = tempfile.mkdtemp()
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_path)

        # Get extracted folder (first one inside temp_path)
        extracted_root = next((os.path.join(temp_path, d) for d in os.listdir(temp_path)), None)

        # Delete old .exes (except self and new)
        existing_exes = [f for f in os.listdir(BASE_DIR) if f.endswith('.exe')]
        new_exes = [f for f in os.listdir(extracted_root) if f.endswith('.exe')]

        for exe in existing_exes:
            if exe != os.path.basename(sys.executable) and exe not in new_exes:
                try:
                    os.remove(os.path.join(BASE_DIR, exe))
                except Exception:
                    pass

        # Copy new files
        for item in os.listdir(extracted_root):
            s = os.path.join(extracted_root, item)
            d = os.path.join(BASE_DIR, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        # Update version
        config['CURRENT_VERSION'] = latest_tag
        with open(VERSION_FILE, 'w') as f:
            json.dump(config, f, indent=4)

        # Cleanup
        os.remove(zip_path)
        shutil.rmtree(temp_path)

        # Launch the new .exe
        new_executable = None
        for exe in new_exes:
            if exe != os.path.basename(sys.executable):
                new_executable = os.path.join(BASE_DIR, exe)
                break

        if new_executable and os.path.isfile(new_executable):
            subprocess.Popen([new_executable], cwd=BASE_DIR)

        self.finished.emit()

# --- Main UI ---
class UpdaterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mDirt Updater")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        self.title = QLabel("mDirt Updater")
        self.title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.status = QLabel("Waiting to start...")
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.button = QPushButton("Check for Updates")
        self.button.clicked.connect(self.start_update)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def start_update(self):
        self.button.setEnabled(False)
        self.worker = UpdateWorker()
        self.worker.progress.connect(self.progress.setValue)
        self.worker.status.connect(self.status.setText)
        self.worker.finished.connect(self.close)
        self.worker.start()

# --- App Run ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UpdaterUI()
    ui.show()
    sys.exit(app.exec())
