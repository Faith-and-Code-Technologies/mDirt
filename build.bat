pyinstaller src/main.py ^
  --name mDirt-2.5.1 ^
  --onedir ^
  --add-data "src/details.py;src" ^
  --add-data "src/select_item.py;src" ^
  --add-data "src/ui_updater.py;src" ^
  --add-data "src/ui.py;src" ^
  --add-data "src/updater.py;src" ^
  --add-data "lib;lib"
