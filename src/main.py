import datetime, json, os, re, sys, requests, importlib, shutil, pickle, html, string

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QStandardItem
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QWidget, QDialog, QTreeWidget, QTreeWidgetItem

import select_item, load_project
from ui import Ui_MainWindow

from updater import Updater, ModuleGrabber

APP_VERSION = '3.0.0'
LIB_URL = 'https://raw.githubusercontent.com/Faith-and-Code-Technologies/mDirt/main/lib'
ISSUE_URL = 'https://github.com/Faith-and-Code-Technologies/mDirt/issues'

def alert(message):
    messageBox = QMessageBox()
    messageBox.setIcon(QMessageBox.Icon.Information)
    messageBox.setText(message)
    messageBox.setWindowTitle("Alert")
    messageBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    messageBox.exec()

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mainDirectory = f"{os.path.dirname(os.path.abspath(__file__))}/.."
        self.ui.menuNew_Element.setEnabled(False)

        # CONNECTIONS
        self.ui.actionNew_Project.triggered.connect(self.openProjectMenu)
        self.ui.createProjectButton.clicked.connect(self.newProject)
        self.ui.actionOpen_Project.triggered.connect(self.loadProjectUI)

        self.ui.actionBlock.triggered.connect(self.newBlock)
        # self.ui.actionItem.triggered.connect(self.newItem)
        # self.ui.actionRecipe.triggered.connect(self.newRecipe)
        # self.ui.actionPainting.triggered.connect(self.newPainting)

        # Block Specific Connections
        self.ui.blockTextureButtonTop.clicked.connect(lambda: self.addBlockTexture(0))
        self.ui.blockTextureButtonLeft.clicked.connect(lambda: self.addBlockTexture(1))
        self.ui.blockTextureButtonBack.clicked.connect(lambda: self.addBlockTexture(2))
        self.ui.blockTextureButtonRight.clicked.connect(lambda: self.addBlockTexture(3))
        self.ui.blockTextureButtonFront.clicked.connect(lambda: self.addBlockTexture(4))
        self.ui.blockTextureButtonBottom.clicked.connect(lambda: self.addBlockTexture(5))

        self.ui.blockConfirmButton.clicked.connect(self.addBlock)

    #######################
    # SETUP PROJECT       #
    #######################

    def pullSupportedVersions(self):
        version_url = f"{LIB_URL}/version_list.json"
        
        try:
            response = requests.get(version_url, timeout=5)
            response.raise_for_status()

            data = response.json()
            self.version_json = data
            self.supportedVersions = data.get("versions", [])

        except requests.exceptions.RequestException as e:
            alert(f"Failed to download supported versions. Error: {e}\n\nPlease relaunch mDirt and try again. If the problem persists, report it here:\n{ISSUE_URL}")
        except ValueError:
            alert(f"Received invalid JSON from server.\n\nPlease try again or report the issue:\n{ISSUE_URL}")

    def openProjectMenu(self):
        self.pullSupportedVersions()                   # Pulls the supported version list from the server.

        self.ui.packVersion.clear()
        for version in self.supportedVersions:
            self.ui.packVersion.addItem(version)       # Adds the versions to the dropdown.

        self.ui.elementEditor.setCurrentIndex(5)
    
    def validatePackDetails(self):
        def validate(field, allowed_chars, field_name):
            text = field.text()
            if not text:
                field.setStyleSheet("QLineEdit { border: 1px solid red; }")
                alert("Please fill in all fields!")
                return False
            if any(c not in allowed_chars for c in text):
                field.setStyleSheet("QLineEdit { border: 1px solid red; }")
                alert(f"{field_name} contains an illegal character!")
                return False
            field.setStyleSheet("")
            return True

        if not validate(self.ui.packName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Name"):
            return 0
        if not validate(self.ui.packNamespace, "abcdefghijklmnopqrstuvwxyz_0123456789", "Namespace"):
            return 0
        if not validate(self.ui.packDescription, string.printable, "Description"):
            return 0
        if not validate(self.ui.packAuthor, "abcdefghijklmnopqrstuvwxyz_0123456789", "Author"):
            return 0

        return 1

    def pullData(self):
        version = self.packDetails["version"]
        local_path = f"lib/{version}_data.json"
        url = f"{LIB_URL}/{version}_data.json"

        if not os.path.exists(local_path):
            response = requests.get(url)
            if response.status_code == 200:
                os.makedirs("lib", exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(response.content)
            else:
                alert(f"Failed to download data file for version {version}. (HTTP {response.status_code}). \nCheck your internet connection, and relaunch mDirt. If the issue persists, report it here:\n{ISSUE_URL}")

            try: # Opens the JSON to ensure it is not corrupted.
                with open(local_path, "r") as f:
                    json.load(f)
            except json.JSONDecodeError:
                os.remove(local_path)
                alert(f"Downloaded data file is corrupt or invalid JSON.\nCheck your internet connection, and relaunch mDirt. If the issue persists, report it here:\n{ISSUE_URL}")

    def newProject(self):
        if self.validatePackDetails() == 0: return      # Make sure all fields aren't empty and only contain valid characters.

        self.packDetails = {
            "name": self.ui.packName.text(),
            "namespace": self.ui.packNamespace.text(),
            "description": self.ui.packDescription.text(),
            "author": self.ui.packAuthor.text(),
            "version": self.ui.packVersion.currentText()
        }

        self.pullData()
        self.setupProjectData()

        self.saveProjectAs()
        self.ui.menuNew_Element.setEnabled(True) # Enable the Element buttons so user can add things to their pack

        self.ui.elementEditor.setCurrentIndex(0)
        self.ui.textEdit.setHtml(f"<h1>To get started with <strong>{self.packDetails["name"]}</strong>, create a New Element!</h1>")

    def setupProjectData(self):
        self.mainDirectory = f"{os.path.dirname(os.path.abspath(__file__))}/.."
        
        with open(f"{self.mainDirectory}/lib/{self.packDetails["version"]}_data.json", "r") as f:
            self.data = json.load(f)
        
        self.dataFormat = self.version_json["dataformat"][self.packDetails["version"]]
        self.resourceFormat = self.version_json["resourceformat"][self.packDetails["version"]]

        self.blocks = {}
        self.items = {}
        self.recipes = {}
        self.paintings = {}

        self.blocks_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Blocks"])
        self.items_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Items"])
        self.recipes_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Recipes"])
        self.paintings_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Paintings"])

        self.blockTexture = {}
        self.itemTexture = None
        self.recipe = {}
        self.paintingTexture = None

        self.header = f"""#####################################
#   This File Was Created By mDirt  #
#               v{APP_VERSION}              #
#   Copyright 2025 by Jupiter Dev   #
#####################################\n"""

    #######################
    # SAVE / LOAD         #
    #######################
    
    def saveProject(self):
        self.saveProjectAs()

    def saveProjectAs(self):
        projectDirectory = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}'
        os.makedirs(projectDirectory, exist_ok=True)

        with open(f'{projectDirectory}/project.dat', 'w') as file:
            data = {
            "app_version": APP_VERSION,
            "metadata": {
                "last_edited": datetime.datetime.now(datetime.UTC).isoformat()
            },
            "packDetails": self.packDetails
        }
            json.dump(data, file, indent=4)
            
        with open(f'{projectDirectory}/blocks.json', 'w') as file:
            json.dump(self.blocks, file, indent=4)
        with open(f'{projectDirectory}/items.json', 'w') as file:
            json.dump(self.items, file, indent=4)
        with open(f'{projectDirectory}/recipes.json', 'w') as file:
            json.dump(self.recipes, file, indent=4)
        with open(f'{projectDirectory}/paintings.json', 'w') as file:
            json.dump(self.paintings, file, indent=4)
        
        os.makedirs(f'{projectDirectory}/assets', exist_ok=True)
        os.makedirs(f'{projectDirectory}/assets/blocks', exist_ok=True)
        os.makedirs(f'{projectDirectory}/assets/items', exist_ok=True)
        os.makedirs(f'{projectDirectory}/assets/paintings', exist_ok=True)

    def loadProjectUI(self):
        self.projectList = QWidget()
        self.projectForm = load_project.Ui_Form()
        self.projectForm.setupUi(self.projectList)

        workspaceDirectory = f'{self.mainDirectory}/workspaces'
        projects = []

        if os.path.exists(workspaceDirectory):
            for name in os.listdir(workspaceDirectory):
                path = os.path.join(workspaceDirectory, name)
                if os.path.isdir(path):
                    projects.append(name)
        
        self.projectForm.listWidget.clear()
        self.projectForm.listWidget.addItems(projects)

        self.projectForm.pushButton.clicked.connect(lambda: self.loadProject(self.projectForm.listWidget.item(self.projectForm.listWidget.currentRow()).text()))

        self.projectList.show()

    def loadProject(self, projectNamespace):
        if projectNamespace == "":
            alert("Please select a valid project!")
            return
        
        projectDirectory = f'{self.mainDirectory}/workspaces/{projectNamespace}'
        if not os.path.exists(projectDirectory):
            alert("This project doesn't exist or is corrupted!")
            return
        
        with open(f'{projectDirectory}/project.dat', 'r') as file:
            data = json.load(file)
            self.packDetails = data["packDetails"]
        if data["app_version"] != APP_VERSION:
            alert("Warning: This project was created with a different version of the app, and may cause crashes or corruption!")
        
        with open(f'{projectDirectory}/blocks.json', 'r') as file:
            self.blocks = json.load(file)
        with open(f'{projectDirectory}/items.json', 'r') as file:
            self.items = json.load(file)
        with open(f'{projectDirectory}/recipes.json', 'r') as file:
            self.recipes = json.load(file)
        with open(f'{projectDirectory}/paintings.json', 'r') as file:
            self.paintings = json.load(file)
        
        self.projectList.close()

    #######################
    # BLOCKS TAB          #
    #######################

    def addBlockTexture(self, id_):
        textureId = id_
        texture, _ = QFileDialog.getOpenFileName(self, "Open Texture File", "", "PNG Files (*.png)")
        if not texture:
            return
        
        filename = os.path.basename(texture)
        destinationPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/blocks/{filename}'
        shutil.copyfile(texture, destinationPath)

        self.blockTexture[textureId] = destinationPath

        image = QImage(self.blockTexture[textureId])
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        if textureId == 0:
            self.ui.blockTextureLabelTop.setPixmap(pixmap)
        if textureId == 1:
            self.ui.blockTextureLabelLeft.setPixmap(pixmap)
        if textureId == 2:
            self.ui.blockTextureLabelBack.setPixmap(pixmap)
        if textureId == 3:
            self.ui.blockTextureLabelRight.setPixmap(pixmap)
        if textureId == 4:
            self.ui.blockTextureLabelFront.setPixmap(pixmap)
        if textureId == 5:
            self.ui.blockTextureLabelBottom.setPixmap(pixmap)

    def newBlock(self):
        self.ui.elementEditor.setCurrentIndex(1)

    def validateBlockDetails(self):
        def validate(field, allowed_chars, field_name):
            text = field.text()
            if not text:
                field.setStyleSheet("QLineEdit { border: 1px solid red; }")
                alert("Please fill in all fields!")
                return False
            if any(c not in allowed_chars for c in text):
                field.setStyleSheet("QLineEdit { border: 1px solid red; }")
                alert(f"{field_name} contains an illegal character!")
                return False
            field.setStyleSheet("")
            return True

        if not validate(self.ui.blockDisplayName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Display Name"):
            return 0
        if not validate(self.ui.blockName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Name"):
            return 0
        if not self.ui.blockBaseBlock.text() in self.data["blocks"]:
            return 0

        return 1

    def addBlock(self):
        if self.validateBlockDetails == 0: return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.setStyle("Fusion")
    sys.exit(app.exec())