import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

def load_ui(file_path):
    loader = QUiLoader()
    ui_file = QFile(file_path)
    ui_file.open(QFile.ReadOnly)
    window = loader.load(ui_file)
    ui_file.close()
    return window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    with open("new_ui/theme_darkearth.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = load_ui("new_ui/experemental_ui.ui")
    window.show()
    sys.exit(app.exec())
