pyinstaller src/main.py ^
  --name mDirt-3.0.0-Beta1 ^
  --onedir ^
  --windowed ^
  --add-data "lib;lib" ^
  --add-data "src;src" ^
  --add-data "workspaces;workspaces" ^
  --hidden-import=jinja2 ^
  --hidden-import=jinja2.ext