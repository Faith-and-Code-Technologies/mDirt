import os
import sys
import json
import zipfile
import shutil
import tempfile
import subprocess
import requests
from packaging import version
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import psutil
import pathlib

# --- Constants ---
if getattr(sys, "frozen", False):
    BASE_DIR = pathlib.Path(sys.executable).resolve().parent
else:
    BASE_DIR = pathlib.Path(__file__).resolve().parent

VERSION_FILE = os.path.join(BASE_DIR, "version.json")

# --- Load Config ---
with open(VERSION_FILE, "r") as f:
    config = json.load(f)

github_url = config["GITHUB_URL"]
current_version = config["CURRENT_VERSION"]
include_beta = config.get("INCLUDE_BETA", False)


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


# --- Worker for update ---
class UpdateWorker:
    def __init__(self, progress_callback, status_callback, finish_callback):
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.finish_callback = finish_callback

    def run(self):
        self.status_callback("Checking for updates...")
        try:
            release_data = get_latest_release(include_beta)
        except Exception as e:
            self.status_callback(f"Error: {str(e)}")
            return

        latest_tag = release_data["tag_name"]
        if version.parse(latest_tag) <= version.parse(current_version):
            self.status_callback("No updates available.")
            return

        self.status_callback(f"New version found: {latest_tag}. Downloading...")

        zip_url = None
        zip_name = None

        for asset in release_data["assets"]:
            if asset["name"].endswith(".zip"):
                zip_url = asset["browser_download_url"]
                zip_name = asset["name"]
                break

        if not zip_url:
            self.status_callback("No .zip asset found.")
            return

        zip_path = os.path.join(BASE_DIR, zip_name)
        with requests.get(zip_url, stream=True) as r:
            with open(zip_path, "wb") as f:
                total = int(r.headers.get("content-length", 0))
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        self.progress_callback(int(downloaded * 100 / total))

        self.status_callback("Extracting update...")
        temp_path = tempfile.mkdtemp()
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_path)

        extracted_root = next(
            (os.path.join(temp_path, d) for d in os.listdir(temp_path)), None
        )

        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] and proc.info['exe'].endswith(".exe"):
                    exe_name = os.path.basename(proc.info['exe'])
                    if exe_name != os.path.basename(sys.executable) and exe_name in os.listdir(BASE_DIR):
                        proc.terminate()
                        proc.wait(timeout=5)
            except Exception:
                pass
        # Delete old .exes (except self and new)
        existing_exes = [f for f in os.listdir(BASE_DIR) if f.endswith(".exe")]
        new_exes = [f for f in os.listdir(extracted_root) if f.endswith(".exe")]

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

        config["CURRENT_VERSION"] = latest_tag
        with open(VERSION_FILE, "w") as f:
            json.dump(config, f, indent=4)

        os.remove(zip_path)
        shutil.rmtree(temp_path)

        new_executable = None
        for exe in new_exes:
            if exe != os.path.basename(sys.executable):
                new_executable = os.path.join(BASE_DIR, exe)
                break

        if new_executable and os.path.isfile(new_executable):
            subprocess.Popen([new_executable], cwd=BASE_DIR)

        self.finish_callback()


# --- Main UI ---
class UpdaterUI(tk.Tk):
    def __init__(self, update_found: bool):
        super().__init__()

        if not update_found:
            self.quit()

        self.title("mDirt Updater")
        self.geometry("400x250")
        self.configure(bg="#2e2e2e")
        self.resizable(False, False)

        self.title_label = tk.Label(
            self,
            text="mDirt Updater",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#2e2e2e",
        )
        self.title_label.pack(pady=(20, 10))

        self.status_label = tk.Label(
            self,
            text="A new update is available!\nDo you want to download it?",
            font=("Segoe UI", 12),
            fg="#ffffff",
            bg="#2e2e2e",
        )
        self.status_label.pack(pady=10)

        self.progress = ttk.Progressbar(self, length=300, mode="determinate")
        self.progress.pack(pady=(5, 15))

        btn_frame = tk.Frame(self, bg="#2e2e2e")
        btn_frame.pack(pady=10)

        button_style = {
            "font": ("Segoe UI", 11),
            "width": 10,
            "height": 1,
            "bg": "#4CAF50",
            "fg": "#ffffff",
            "activebackground": "#45a049",
            "activeforeground": "#ffffff",
            "relief": "flat",
            "bd": 0,
        }

        self.yes_btn = tk.Button(
            btn_frame, text="Yes", command=self.start_update, **button_style
        )
        self.yes_btn.grid(row=0, column=0, padx=10)

        self.no_btn = tk.Button(btn_frame, text="No", command=self.quit, **button_style)
        self.no_btn.grid(row=0, column=1, padx=10)

        self.center_window()

    def start_update(self):
        self.yes_btn.config(state=tk.DISABLED)
        self.no_btn.config(state=tk.DISABLED)
        worker = UpdateWorker(
            self.update_progress, self.update_status, self.finish_update
        )
        threading.Thread(target=worker.run, daemon=True).start()

    def update_progress(self, value):
        self.progress["value"] = value
        self.update_idletasks()

    def update_status(self, status):
        self.status_label.config(text=status)
        self.update_idletasks()

    def finish_update(self):
        messagebox.showinfo("Update Finished", "The update was completed successfully.")
        self.quit()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"+{x}+{y}")


# --- Check Before Running ---
def check_for_update():
    try:
        release_data = get_latest_release(include_beta)
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    latest_tag = release_data["tag_name"]
    return version.parse(latest_tag) > version.parse(current_version)


if __name__ == "__main__":
    if check_for_update():
        app = UpdaterUI(update_found=True)
        app.mainloop()
    else:
        sys.exit()
