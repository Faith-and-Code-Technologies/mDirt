#!/bin/bash
set -e

# ================================
# CONFIGURABLE VERSION NUMBER
# ================================
VERSION="3.0.1"
ZIP_NAME="mDirt-${VERSION}.zip"
RELEASE_DIR="release"
MAIN_APP_DIR="dist/mDirt-${VERSION}"
UPDATER_EXE="dist/mDirtUpdater"

echo "========================================"
echo "Building mDirt Application and Updater"
echo "Version: $VERSION"
echo "========================================"

# ========================================
# BUILD MAIN APPLICATION
# ========================================
echo
echo "Building main application..."

pyinstaller src/main.py \
  --name "mDirt-${VERSION}" \
  --icon "assets/icon.ico" \
  --onedir \
  --windowed \
  --add-data "lib:lib" \
  --add-data "assets:assets" \
  --add-data "src:src" \
  --hidden-import=jinja2 \
  --hidden-import=jinja2.ext

echo
echo "Building updater..."
pyinstaller --onefile --windowed --name="mDirtUpdater" --icon="assets/icon.ico" src/updater.py

# ========================================
# MOVE UPDATER INTO MAIN APP DIRECTORY
# ========================================
echo
echo "Moving updater into main application folder..."

if [[ ! -d "$MAIN_APP_DIR" ]]; then
    echo "ERROR: Main application directory not found!"
    exit 1
fi

if [[ ! -f "$UPDATER_EXE" ]]; then
    echo "ERROR: Updater executable not found!"
    exit 1
fi

mv "$UPDATER_EXE" "$MAIN_APP_DIR/"

# ========================================
# COPY VERSION FILE
# ========================================
echo "Copying version.json..."
if [[ -f "version.json" ]]; then
    cp version.json "$MAIN_APP_DIR/"
    echo "version.json copied successfully"
else
    echo "WARNING: version.json not found in root directory"
fi

# ========================================
# CREATE RELEASE DIRECTORY AND COPY APP
# ========================================
echo
echo "Creating release directory..."
mkdir -p "$RELEASE_DIR"

echo "Copying application to release directory..."
cp -r "$MAIN_APP_DIR" "$RELEASE_DIR/mDirt-${VERSION}"

# ========================================
# CREATE ZIP ARCHIVE
# ========================================
echo "Creating ZIP archive..."
if command -v zip > /dev/null; then
    cd "$RELEASE_DIR"
    zip -r "../$ZIP_NAME" "mDirt-${VERSION}" > /dev/null
    cd ..
    echo "ZIP archive created successfully: $ZIP_NAME"
else
    echo "ERROR: 'zip' command not found. Please install zip or manually archive the release."
    echo "Please manually zip the contents of: '$RELEASE_DIR' -> '$ZIP_NAME'"
    exit 1
fi

# ========================================
# CLEAN RELEASE DIRECTORY
# ========================================
echo
echo "Cleaning extras in release folder..."
mv "$ZIP_NAME" "$RELEASE_DIR/"

# Remove everything in release except the ZIP file
#find "$RELEASE_DIR" ! -name "$ZIP_NAME" -type f -exec rm -f {} +
#find "$RELEASE_DIR" ! -name "$ZIP_NAME" -type d -exec rm -rf {} + 2>/dev/null || true

# ========================================
# FINAL CLEANUP
# ========================================
echo
echo "Cleaning up build artifacts..."
rm -rf build dist __pycache__
rm -f ./*.spec

# ========================================
# SUCCESS MESSAGE
# ========================================
echo
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo
echo "Files created:"
echo "- Main application: $MAIN_APP_DIR"
echo "- Updater: $MAIN_APP_DIR/mDirtUpdater"
echo "- Version file: $MAIN_APP_DIR/version.json"
echo "- Release ZIP: $RELEASE_DIR/$ZIP_NAME"
echo

read -rp "Open release folder? (y/n): " OPEN_FOLDER
if [[ "$OPEN_FOLDER" =~ ^[Yy]$ ]]; then
    xdg-open "$RELEASE_DIR" >/dev/null 2>&1 &
fi

echo
echo "Build process complete!"
