import os
import requests
import zipfile
import io


class ModuleDownloader:
    """
    Downloads and extracts versioned modules from the mDirt GitHub repository.
    """

    REPO_URL = "https://github.com/Faith-and-Code-Technologies/mDirt"
    MODULE_BASE = "https://raw.githubusercontent.com/Faith-and-Code-Technologies/mDirt/main/modules"

    def __init__(self, target_dir="src/generation"):
        self.target_dir = target_dir
        os.makedirs(self.target_dir, exist_ok=True)

    def download_and_extract(self, version: str):
        """
        Downloads a ZIP file for the given version and extracts it into the target directory.

        :param version: Version identifier, e.g., 'v1_21_4'
        """
        zip_url = f"{self.MODULE_BASE}/{version}.zip"

        try:
            response = requests.get(zip_url)
            response.raise_for_status()
        except requests.RequestException as e:
            return False

        # Extract the zip file from memory
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                extract_path = os.path.join(self.target_dir, version)
                zf.extractall(extract_path)
        except zipfile.BadZipFile:
            return False
        return True


if __name__ == "__main__":
    downloader = ModuleDownloader()
    version = "v1_21_3"  # Example version
    downloader.download_and_extract(version)
