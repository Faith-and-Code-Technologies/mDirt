pyinstaller src/main.py ^
  --name mDirt-3.0.0-Beta1 ^
  --onedir ^
  --add-data "lib;lib" ^
  --add-data "src;src" ^
  --add-data "workspaces;workspaces"
