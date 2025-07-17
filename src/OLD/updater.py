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
import time

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
        try:
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
            
            # Download with better error handling
            try:
                with requests.get(zip_url, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open(zip_path, "wb") as f:
                        total = int(r.headers.get("content-length", 0))
                        downloaded = 0
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:  # Filter out keep-alive chunks
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total:
                                    self.progress_callback(int(downloaded * 100 / total))
            except Exception as e:
                self.status_callback(f"Download failed: {str(e)}")
                return

            self.status_callback("Extracting update...")
            self.progress_callback(0)  # Reset progress bar
            
            # Create temp directory with better path handling
            temp_path = tempfile.mkdtemp(prefix="updater_")
            
            try:
                # Extract with progress feedback
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    file_list = zip_ref.namelist()
                    total_files = len(file_list)
                    
                    for i, file in enumerate(file_list):
                        zip_ref.extract(file, temp_path)
                        progress = int((i + 1) * 100 / total_files)
                        self.progress_callback(progress)
                        
                        # Add small delay to show progress and prevent UI freezing
                        if i % 10 == 0:  # Update every 10 files
                            time.sleep(0.01)
                
                self.status_callback("Processing files...")
                
                # Find the extracted root directory more reliably
                temp_contents = os.listdir(temp_path)
                if not temp_contents:
                    raise Exception("Extracted archive is empty")
                
                # Handle both single folder extraction and direct file extraction
                if len(temp_contents) == 1 and os.path.isdir(os.path.join(temp_path, temp_contents[0])):
                    extracted_root = os.path.join(temp_path, temp_contents[0])
                else:
                    extracted_root = temp_path
                
                if not os.path.exists(extracted_root):
                    raise Exception(f"Extracted root directory not found: {extracted_root}")

                self.status_callback("Stopping running processes...")
                # Terminate other processes more safely
                terminated_processes = []
                for proc in psutil.process_iter(['pid', 'name', 'exe']):
                    try:
                        if (proc.info['exe'] and 
                            proc.info['exe'].endswith(".exe") and
                            proc.info['exe'] != sys.executable):
                            
                            exe_name = os.path.basename(proc.info['exe'])
                            exe_path = os.path.join(BASE_DIR, exe_name)
                            
                            if os.path.exists(exe_path):
                                proc.terminate()
                                terminated_processes.append(proc)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass

                # Wait for processes to terminate
                for proc in terminated_processes:
                    try:
                        proc.wait(timeout=3)
                    except (psutil.TimeoutExpired, psutil.NoSuchProcess):
                        try:
                            proc.kill()  # Force kill if terminate doesn't work
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass

                self.status_callback("Cleaning up old files...")
                # Delete old .exes (except self and new)
                existing_exes = [f for f in os.listdir(BASE_DIR) if f.endswith(".exe")]
                new_exes = [f for f in os.listdir(extracted_root) if f.endswith(".exe")]

                for exe in existing_exes:
                    if exe != os.path.basename(sys.executable) and exe not in new_exes:
                        exe_path = os.path.join(BASE_DIR, exe)
                        max_retries = 5
                        for attempt in range(max_retries):
                            try:
                                os.remove(exe_path)
                                break
                            except (PermissionError, FileNotFoundError):
                                if attempt < max_retries - 1:
                                    time.sleep(0.5)  # Wait before retry
                                pass

                self.status_callback("Installing new files...")
                # Copy new files with better error handling
                items_to_copy = os.listdir(extracted_root)
                for i, item in enumerate(items_to_copy):
                    s = os.path.join(extracted_root, item)
                    d = os.path.join(BASE_DIR, item)
                    
                    try:
                        if os.path.isdir(s):
                            if os.path.exists(d):
                                shutil.rmtree(d)
                            shutil.copytree(s, d)
                        else:
                            # For files, handle potential permission issues
                            max_retries = 3
                            for attempt in range(max_retries):
                                try:
                                    shutil.copy2(s, d)
                                    break
                                except PermissionError:
                                    if attempt < max_retries - 1:
                                        time.sleep(0.5)
                                    else:
                                        raise
                    except Exception as e:
                        print(f"Warning: Failed to copy {item}: {str(e)}")
                    
                    # Update progress
                    progress = int((i + 1) * 100 / len(items_to_copy))
                    self.progress_callback(progress)

                # Update version info
                config["CURRENT_VERSION"] = latest_tag
                with open(VERSION_FILE, "w") as f:
                    json.dump(config, f, indent=4)

                self.status_callback("Finalizing update...")
                
                # Find and launch new executable
                new_executable = None
                for exe in new_exes:
                    if exe != os.path.basename(sys.executable):
                        potential_path = os.path.join(BASE_DIR, exe)
                        if os.path.isfile(potential_path):
                            new_executable = potential_path
                            break

                if new_executable:
                    try:
                        subprocess.Popen([new_executable], cwd=BASE_DIR, 
                                       creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0)
                    except Exception as e:
                        print(f"Warning: Failed to launch new executable: {str(e)}")

                self.finish_callback()

            except Exception as e:
                self.status_callback(f"Extraction failed: {str(e)}")
                return
            finally:
                # Cleanup
                try:
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
                    if os.path.exists(temp_path):
                        shutil.rmtree(temp_path)
                except Exception as e:
                    print(f"Warning: Cleanup failed: {str(e)}")

        except Exception as e:
            self.status_callback(f"Update failed: {str(e)}")
            print(f"Full error: {str(e)}")


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