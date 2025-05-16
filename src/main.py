import datetime
import json
import os
import sys
import requests
import importlib
import shutil
import string
import subprocess
import logging
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QEvent, QObject
from PySide6.QtGui import QImage, QPixmap, QFont, QDropEvent, QDragEnterEvent
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget, QTreeWidgetItem

from utils.field_validator import FieldValidator
from utils.field_resetter import FieldResetter
from utils.enums import BlockFace, ElementPage
from utils.alert import alert

import ui.select_item as select_item
import ui.load_project as load_project
from ui.ui import Ui_MainWindow

from settings import SettingsManager
from module import ModuleDownloader

APP_VERSION = '3.0.0'
FULL_APP_VERSION = '3.0.0-beta.2'
LIB_URL = 'https://raw.githubusercontent.com/Faith-and-Code-Technologies/mDirt/main/lib'
ISSUE_URL = 'https://github.com/Faith-and-Code-Technologies/mDirt/issues'


class DropHandler(QObject):
    def __init__(self, button, func):
        super().__init__()
        self.button = button
        self.func = func
        self.png_path = None
        self.button.setAcceptDrops(True)
        self.button.installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched == self.button:
            if event.type() == QEvent.DragEnter:
                return self.dragEnter(event)
            elif event.type() == QEvent.Drop:
                return self.dropEvent(event)
        return False

    def dragEnter(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.png'):
                    event.acceptProposedAction()
                    return True
        event.ignore()
        return True

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith('.png'):
                self.png_path = path
                self.func(path)
                break
        return True


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if getattr(sys, 'frozen', False):
            # Binary mode
            self.mainDirectory = Path(sys._MEIPASS)
        else:
            # Dev mode
            self.mainDirectory = Path(__file__).resolve().parent.parent
        self.ui.menuNew_Element.setEnabled(False)

        self.workspacePath = "default"

        self.settings = SettingsManager()

        self.autoSaveTimer = QTimer(self)
        self.autoSaveTimer.timeout.connect(self.saveProject)
        self.setAutoSaveInterval()

        self.logger = logging.getLogger("mDirt")
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        self.file_handler = logging.FileHandler("mdirt.log", mode='w')
        self.file_handler.setFormatter(self.formatter)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

        if self.settings.get("file_export", "verbose_logging"):
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)

        self.disableUnusedSettings()

        if self.settings.get('general', 'open_last_project'):
            project = self.settings.get('data', 'last_project_path')
            if os.path.exists(project):
                self.loadProject(self.settings.get('data', 'last_project_namespace'))
        
        showTips = self.settings.get('appearance', 'show_tips')
        if not showTips:
            self.ui.textEdit.setText("")

        # CONNECTIONS
        self.ui.actionNew_Project.triggered.connect(self.openProjectMenu)
        self.ui.createProjectButton.clicked.connect(self.newProject)
        self.ui.actionOpen_Project.triggered.connect(self.loadProjectUI)
        self.ui.actionExport_Project.triggered.connect(self.generate)
        self.ui.actionSave_2.triggered.connect(self.saveProject)
        self.ui.actionSettings.triggered.connect(self.openSettings)

        self.ui.settingsApplyButton.clicked.connect(self.saveSettings)
        self.ui.settingsRestoreDefaultsButton.clicked.connect(self.restoreSettings)
        self.ui.settingsCancelButton.clicked.connect(self.cancelSettings)

        self.ui.elementViewer.itemDoubleClicked.connect(self.elementClicked)

        self.ui.actionBlock.triggered.connect(self.newBlock)
        self.ui.actionItem.triggered.connect(self.newItem)
        self.ui.actionRecipe.triggered.connect(self.newRecipe)
        self.ui.actionPainting.triggered.connect(self.newPainting)

        # Block Specific Connections
        self.ui.blockTextureButtonTop.clicked.connect(lambda: self.addBlockTexture(BlockFace.TOP))
        self.ui.blockTextureButtonLeft.clicked.connect(lambda: self.addBlockTexture(BlockFace.LEFT))
        self.ui.blockTextureButtonBack.clicked.connect(lambda: self.addBlockTexture(BlockFace.BACK))
        self.ui.blockTextureButtonRight.clicked.connect(lambda: self.addBlockTexture(BlockFace.RIGHT))
        self.ui.blockTextureButtonFront.clicked.connect(lambda: self.addBlockTexture(BlockFace.FRONT))
        self.ui.blockTextureButtonBottom.clicked.connect(lambda: self.addBlockTexture(BlockFace.BOTTOM))

        self.dropTop = DropHandler(self.ui.blockTextureButtonTop, lambda path: self.addBlockTexture(BlockFace.TOP, path))
        self.dropLeft = DropHandler(self.ui.blockTextureButtonLeft, lambda path: self.addBlockTexture(BlockFace.LEFT, path))
        self.dropBack = DropHandler(self.ui.blockTextureButtonBack, lambda path: self.addBlockTexture(BlockFace.BACK, path))
        self.dropRight = DropHandler(self.ui.blockTextureButtonRight, lambda path: self.addBlockTexture(BlockFace.RIGHT, path))
        self.dropFront = DropHandler(self.ui.blockTextureButtonFront, lambda path: self.addBlockTexture(BlockFace.FRONT, path))
        self.dropBottom = DropHandler(self.ui.blockTextureButtonBottom, lambda path: self.addBlockTexture(BlockFace.BOTTOM, path))

        self.dropBlockModel = DropHandler(self.ui.blockModel, self.getBlockModel)

        self.ui.blockModel.currentTextChanged.connect(self.getBlockModel)
        self.ui.blockConfirmButton.clicked.connect(self.addBlock)

        # Item Specific Connections
        self.ui.itemTextureButton.clicked.connect(self.addItemTexture)
        self.ui.itemConfirmButton.clicked.connect(self.addItem)

        self.dropItem = DropHandler(self.ui.itemTextureButton, self.addItemTexture)
        self.dropItemModel = DropHandler(self.ui.itemModel, self.getItemModel)

        # Recipe Specific Connections
        self.ui.slot0Button.clicked.connect(lambda: self.getRecipeItem(0))
        self.ui.slot1Button.clicked.connect(lambda: self.getRecipeItem(1))
        self.ui.slot2Button.clicked.connect(lambda: self.getRecipeItem(2))
        self.ui.slot3Button.clicked.connect(lambda: self.getRecipeItem(3))
        self.ui.slot4Button.clicked.connect(lambda: self.getRecipeItem(4))
        self.ui.slot5Button.clicked.connect(lambda: self.getRecipeItem(5))
        self.ui.slot6Button.clicked.connect(lambda: self.getRecipeItem(6))
        self.ui.slot7Button.clicked.connect(lambda: self.getRecipeItem(7))
        self.ui.slot8Button.clicked.connect(lambda: self.getRecipeItem(8))
        self.ui.slot9Button.clicked.connect(lambda: self.getRecipeItem(9))

        self.ui.smeltingInputButton.clicked.connect(lambda: self.getRecipeItem(10))
        self.ui.smeltingOutputButton.clicked.connect(lambda: self.getRecipeItem(11))

        self.ui.stoneCuttingInputButton.clicked.connect(lambda: self.getRecipeItem(12))
        self.ui.stoneCuttingOutputButton.clicked.connect(lambda: self.getRecipeItem(13))

        self.ui.recipeConfirmButton.clicked.connect(self.addRecipe)

        # Painting Specific Connections
        self.ui.paintingTextureButton.clicked.connect(self.addPaintingTexture)
        self.ui.paintingConfirmButton.clicked.connect(self.addPainting)

        self.dropPainting = DropHandler(self.ui.paintingTextureButton, self.addPaintingTexture)

        # Settings Specific Connections
        self.ui.settingsWorkspacePathButton.clicked.connect(self.workspacePathChanged)
        self.ui.settingsDefaultExportButton.clicked.connect(self.exportPathChanged)

        self.checkUpdates()

    def checkUpdates(self):
        if not self.settings.get('network', 'check_updates'): return
        updaterPath = self.mainDirectory / 'mDirtUpdater.exe'
        if os.path.exists(updaterPath):
            subprocess.Popen(updaterPath)
            # sys.exit() <- Need to do this only if there IS an update available, AND the user decides to INSTALL it
        else:
            alert("The mDirt Updater is missing! Reinstall mDirt to fix it.", 'critical')
            # sys.exit() <- PROBABLY want ot do this, cuz it MIGHT mean other things are broken. Eh. Can't be bothered

    #######################
    # SETUP PROJECT       #
    #######################

    def pullSupportedVersions(self):
        version_url = f'{LIB_URL}/version_list.json'
        
        try:
            response = requests.get(version_url, timeout=5)
            response.raise_for_status()

            data = response.json()
            self.version_json = data
            self.supportedVersions = data.get("versions", [])

        except requests.exceptions.RequestException as e:
            alert(f'Failed to download supported versions. Error: {e}\n\nPlease relaunch mDirt and try again. If the problem persists, report it here:\n{ISSUE_URL}')
        except ValueError:
            alert(f'Received invalid JSON from server.\n\nPlease try again or report the issue:\n{ISSUE_URL}')

    def openProjectMenu(self):
        self.pullSupportedVersions()                   # Pulls the supported version list from the server.

        self.ui.packVersion.clear()
        for version in self.supportedVersions:
            self.ui.packVersion.addItem(version)       # Adds the versions to the dropdown.

        self.ui.elementEditor.setCurrentIndex(ElementPage.PROJECT_SETUP)
    
    def validatePackDetails(self):
        if not FieldValidator.validate_text_field(self.ui.packName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Name"):
            return 0
        if not FieldValidator.validate_text_field(self.ui.packNamespace, "abcdefghijklmnopqrstuvwxyz_0123456789", "Namespace"):
            return 0
        if not FieldValidator.validate_text_field(self.ui.packDescription, string.printable, "Description"):
            return 0
        if not FieldValidator.validate_text_field(self.ui.packAuthor, "abcdefghijklmnopqrstuvwxyz_0123456789", "Author"):
            return 0

        return 1

    def pullData(self):
        version = self.packDetails["version"]
        local_path = self.mainDirectory / 'lib' / f'{version}_data.json'
        url = f'{LIB_URL}/{version}_data.json'

        if not os.path.exists(local_path):
            response = requests.get(url)
            if response.status_code == 200:
                os.makedirs("lib", exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(response.content)
            else:
                alert(f'Failed to download data file for version {version}. (HTTP {response.status_code}). \nCheck your internet connection, and relaunch mDirt. If the issue persists, report it here:\n{ISSUE_URL}')

            try: # Opens the JSON to ensure it is not corrupted.
                with open(local_path, "r") as f:
                    json.load(f)
            except json.JSONDecodeError:
                os.remove(local_path)
                alert(f'Downloaded data file is corrupt or invalid JSON.\nCheck your internet connection, and relaunch mDirt. If the issue persists, report it here:\n{ISSUE_URL}')
        self.grabModule()

    def grabModule(self):
        version = f'v{self.packDetails["version"].replace(".", "_")}'
        dir = self.mainDirectory / 'src' / 'generation'
        self.moduleGrab = ModuleDownloader(target_dir=dir)
        self.moduleGrab.download_and_extract(version)

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

        self.ui.elementEditor.setCurrentIndex(ElementPage.HOME)
        self.ui.textEdit.setHtml(f'<h1>Welcome to mDirt. Create a new Element to get started.</h1>')

    def setupProjectData(self):
        with open(f'{self.mainDirectory}/lib/{self.packDetails["version"]}_data.json', "r") as f:
            self.data = json.load(f)
        
        self.dataFormat = self.version_json["dataformat"][self.packDetails["version"]]
        self.resourceFormat = self.version_json["resourceformat"][self.packDetails["version"]]

        self.ui.menuNew_Element.setEnabled(True)

        self.blocks = {}
        self.items = {}
        self.recipes = {}
        self.paintings = {}

        self.exists = {}

        self.blocks_tree = QTreeWidgetItem(self.ui.elementViewer, ["Blocks"])
        self.items_tree = QTreeWidgetItem(self.ui.elementViewer, ["Items"])
        self.recipes_tree = QTreeWidgetItem(self.ui.elementViewer, ["Recipes"])
        self.paintings_tree = QTreeWidgetItem(self.ui.elementViewer, ["Paintings"])

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
        if self.workspacePath == 'default':
            projectDirectory = self.mainDirectory / 'workspaces' / f'{self.packDetails["namespace"]}'
        else:
            if os.path.exists(self.workspacePath):
                projectDirectory = self.workspacePath
            else:
                projectDirectory = self.mainDirectory / 'workspaces' / f'{self.packDetails["namespace"]}'
        self.settings.set('data', 'last_project_path', str(projectDirectory))
        self.settings.set('data', 'last_project_namespace', self.packDetails["namespace"])
        self.settings.save_settings()
        
        os.makedirs(projectDirectory, exist_ok=True)

        with open(projectDirectory / 'project.dat', 'w') as file:
            data = {
            "app_version": APP_VERSION,
            "metadata": {
                "last_edited": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            "packDetails": self.packDetails
        }
            json.dump(data, file, indent=4)
            
        with open(projectDirectory / 'blocks.json', 'w') as file:
            json.dump(self.blocks, file, indent=4)
        with open(projectDirectory / 'items.json', 'w') as file:
            json.dump(self.items, file, indent=4)
        with open(projectDirectory / 'recipes.json', 'w') as file:
            json.dump(self.recipes, file, indent=4)
        with open(projectDirectory / 'paintings.json', 'w') as file:
            json.dump(self.paintings, file, indent=4)
        
        os.makedirs(projectDirectory / 'assets', exist_ok=True)
        os.makedirs(projectDirectory / 'assets' / 'blocks', exist_ok=True)
        os.makedirs(projectDirectory / 'assets' / 'items', exist_ok=True)
        os.makedirs(projectDirectory / 'assets' / 'paintings', exist_ok=True)

        manifestPath = self.mainDirectory / 'workspaces' / 'manifest.json'

        # Load existing manifest if it exists, otherwise start fresh
        if os.path.exists(manifestPath):
            with open(manifestPath, 'r') as f:
                manifest = json.load(f)
        else:
            manifest = {"workspaces": []}

        # Add current workspace if it's not already listed
        namespace = self.packDetails["namespace"]
        if namespace not in manifest["workspaces"]:
            manifest["workspaces"].append(namespace)
            with open(manifestPath, 'w') as f:
                json.dump(manifest, f, indent=4)

    def loadProjectUI(self):
        self.projectList = QWidget()
        self.projectForm = load_project.Ui_Form()
        self.projectForm.setupUi(self.projectList)

        manifest_path = self.mainDirectory / 'workspaces' / 'manifest.json'
        projects = []

        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                if "workspaces" in manifest and isinstance(manifest["workspaces"], list):
                    projects = manifest["workspaces"]
            except json.JSONDecodeError:
                alert("There was an error reading the manifest.json!\nIt is either missing or malformed.")

        self.projectForm.listWidget.clear()
        self.projectForm.listWidget.addItems(projects)

        self.projectForm.pushButton.clicked.connect(lambda: self.loadProject(self.projectForm.listWidget.item(self.projectForm.listWidget.currentRow()).text()))

        self.projectList.show()

    def loadProject(self, projectNamespace):
        if projectNamespace == "":
            alert("Please select a valid project!")
            return
        
        projectDirectory = self.mainDirectory / 'workspaces' / f'{projectNamespace}'
        if not os.path.exists(projectDirectory):
            alert("This project doesn't exist or is corrupted!")
            return
        
        with open(projectDirectory / 'project.dat', 'r') as file:
            data = json.load(file)
            self.packDetails = data["packDetails"]
        if data["app_version"] != APP_VERSION:
            alert("Warning: This project was created with a different version of the app, and may cause crashes or corruption!")
        
        self.pullSupportedVersions()
        self.pullData()
        self.setupProjectData()

        with open(projectDirectory / 'blocks.json', 'r') as file:
            self.blocks = json.load(file)
        with open(projectDirectory / 'items.json', 'r') as file:
            self.items = json.load(file)
        with open(projectDirectory / 'recipes.json', 'r') as file:
            self.recipes = json.load(file)
        with open(projectDirectory / 'paintings.json', 'r') as file:
            self.paintings = json.load(file)
        
        try:
            self.projectList.close()
        except:
            pass
       
        for item in self.blocks:
            QTreeWidgetItem(self.blocks_tree, [self.blocks[item]["name"]])
        
        for item in self.items:
            QTreeWidgetItem(self.items_tree, [self.items[item]["name"]])
        
        for item in self.recipes:
            QTreeWidgetItem(self.recipes_tree, [self.recipes[item]["name"]])
        
        for item in self.paintings:
            QTreeWidgetItem(self.paintings_tree, [self.paintings[item]["name"]])

    #######################
    # SETTINGS            #
    #######################

    def disableUnusedSettings(self):
        self.ui.settingsLanguageCombo.setDisabled(True)
        self.ui.settingsExperimentsCheckbox.setDisabled(True)
        self.ui.settingsPackFormatOverride.setDisabled(True)
        self.ui.settingsUpdateURL.setDisabled(True)

    def setAutoSaveInterval(self):
        mode = self.settings.get('general', 'auto_save_interval').lower()
        if mode == "1 minute":
            self.autoSaveTimer.start(60 * 1000)
        elif mode == "5 minutes":
            self.autoSaveTimer.start(5 * 60 * 1000)
        elif mode == "off":
            self.autoSaveTimer.stop()

    def workspacePathChanged(self):
        loc = QFileDialog.getExistingDirectory(self, "Select Workspace Directory", "")
        self.ui.settingsWorkspacePathButton.setText(loc)

    def exportPathChanged(self):
        loc = QFileDialog.getExistingDirectory(self, "Select Export Directory", "")
        self.ui.settingsDefaultExportButton.setText(loc)

    def openSettings(self):
        self.refreshSettings()
        self.ui.elementEditor.setCurrentIndex(ElementPage.SETTINGS)
    
    def saveSettings(self):
        self.settings.set('general', 'auto_save_interval', self.ui.settingsAutoSaveInt.currentText())
        self.settings.set('general', 'open_last_project', self.ui.settingsOpenLastCheckbox.isChecked())
        self.settings.set('general', 'workspace_path', self.ui.settingsWorkspacePathButton.text())
        self.settings.set('general', 'language', self.ui.settingsLanguageCombo.currentText())
        self.settings.set('appearance', 'theme', self.ui.settingsThemeCombo.currentText())
        self.settings.set('appearance', 'font_size', self.ui.settingsFontSizeSlider.value())
        self.settings.set('appearance', 'show_tips', self.ui.settingsTipsCheckbox.isChecked())
        self.settings.set('editor', 'confirm_deletes', self.ui.settingsConfirmElementDeleteCheckbox.isChecked())
        self.settings.set('editor', 'enable_experiments', self.ui.settingsExperimentsCheckbox.isChecked())
        self.settings.set('file_export', 'default_export_location', self.ui.settingsDefaultExportButton.text())
        self.settings.set('file_export', 'pack_format_override', self.ui.settingsPackFormatOverride.text())
        self.settings.set('file_export', 'verbose_logging', self.ui.settingsVerboseLoggingCheckbox.isChecked())
        self.settings.set('network', 'check_updates', self.ui.settingsCheckUpdatesCheckbox.isChecked())
        self.settings.set('network', 'custom_update_url', self.ui.settingsUpdateURL.text())
        self.settings.set('network', 'get_betas', self.ui.settingsBetaUpdatesCheckbox.isChecked())

        self.settings.save_settings()
        self.refreshSettings()

        alert("Settings updated!")

    def restoreSettings(self):
        self.settings.reset_to_defaults()
        self.refreshSettings()
        alert("Settings have been restored to defaults!")

    def cancelSettings(self):
        self.ui.elementEditor.setCurrentIndex(ElementPage.HOME)

    def refreshSettings(self):
        self.ui.settingsAutoSaveInt.setCurrentText(self.settings.get('general', 'auto_save_interval'))
        self.ui.settingsOpenLastCheckbox.setChecked(self.settings.get('general', 'open_last_project'))
        self.ui.settingsWorkspacePathButton.setText(self.settings.get('general', 'workspace_path'))
        self.ui.settingsLanguageCombo.setCurrentText(self.settings.get('general', 'language'))
        self.ui.settingsThemeCombo.setCurrentText(self.settings.get('appearance', 'theme'))
        self.ui.settingsFontSizeSlider.setValue(self.settings.get('appearance', 'font_size'))
        self.ui.settingsTipsCheckbox.setChecked(self.settings.get('appearance', 'show_tips'))
        self.ui.settingsConfirmElementDeleteCheckbox.setChecked(self.settings.get('editor', 'confirm_deletes'))
        self.ui.settingsExperimentsCheckbox.setChecked(self.settings.get('editor', 'enable_experiments'))
        self.ui.settingsDefaultExportButton.setText(self.settings.get('file_export', 'default_export_location'))
        self.ui.settingsPackFormatOverride.setText(self.settings.get('file_export', 'pack_format_override'))
        self.ui.settingsVerboseLoggingCheckbox.setChecked(self.settings.get('file_export', 'verbose_logging'))
        self.ui.settingsCheckUpdatesCheckbox.setChecked(self.settings.get('network', 'check_updates'))
        self.ui.settingsUpdateURL.setText(self.settings.get('network', 'custom_update_url'))
        self.ui.settingsBetaUpdatesCheckbox.setChecked(self.settings.get('network', 'get_betas'))

        self.setAutoSaveInterval()
        self.workspacePath = self.settings.get('general', 'workspace_path')
        self.setFont(QFont("Segoe UI", self.settings.get('appearance', 'font_size')))

    #######################
    # ELEMENT MANAGER     #
    #######################

    def elementClicked(self, item, column):
        element_type = item.parent()
        if element_type is None: return

        if element_type.text(column) == "Blocks":
            self.editBlock(item.text(column)) 
        elif element_type.text(column) == "Items":
            self.editItem(item.text(column))
        elif element_type.text(column) == "Recipes":
            self.editRecipe(item.text(column))
        elif element_type.text(column) == "Paintings":
            self.editPainting(item.text(column))

    #######################
    # BLOCKS TAB          #
    #######################

    def addBlockTexture(self, face: BlockFace, path=None):
        if not path:
            texture, _ = QFileDialog.getOpenFileName(self, "Open Texture File", "", "PNG Files (*.png)")
            if not texture:
                return
        else:
            texture = path

        filename = os.path.basename(texture)
        destinationPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/blocks/{filename}'
        shutil.copyfile(texture, destinationPath)

        self.blockTexture[face] = destinationPath

        image = QImage(self.blockTexture[face])
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        label_map = {
            BlockFace.TOP: self.ui.blockTextureLabelTop,
            BlockFace.LEFT: self.ui.blockTextureLabelLeft,
            BlockFace.BACK: self.ui.blockTextureLabelBack,
            BlockFace.RIGHT: self.ui.blockTextureLabelRight,
            BlockFace.FRONT: self.ui.blockTextureLabelFront,
            BlockFace.BOTTOM: self.ui.blockTextureLabelBottom,
        }

        label_map[face].setPixmap(pixmap)

    def newBlock(self):
        self.populateBlockDrop()
        self.ui.elementEditor.setCurrentIndex(ElementPage.BLOCKS)

    def populateBlockDrop(self):
        self.ui.blockDropBox.clear()
        self.ui.blockDropBox.addItem('self')
        for block in self.blocks:
            self.ui.blockDropBox.addItem(block)
        for item in self.items:
            self.ui.blockDropBox.addItem(item)
        for item in self.data["items"]:
            self.ui.blockDropBox.addItem(item)

    def getBlockModel(self, path=None):
        if path:
            filePath = path
            fileName = os.path.basename(filePath)
            destPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/blocks/{fileName}'
            shutil.copy(filePath, destPath)
            self.ui.blockModel.addItem(destPath)
            self.ui.blockModel.setCurrentText(destPath)
        
        elif self.ui.blockModel.currentText() != "Custom": return
        
        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if filePath:
            fileName = os.path.basename(filePath)
            destPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/blocks/{fileName}'
            shutil.copy(filePath, destPath)
            self.ui.blockModel.addItem(destPath)
            self.ui.blockModel.setCurrentText(destPath)

    def validateBlockDetails(self):
        if not FieldValidator.validate_text_field(self.ui.blockDisplayName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Display Name"):
            return 0
        if not FieldValidator.validate_text_field(self.ui.blockName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Name"):
            return 0
        if not FieldValidator.validate_dropdown_selection(self.ui.blockBaseBlock, list(self.data["blocks"]), "Base Block"):
            return 0

        return 1

    def clearBlockFields(self):
        FieldResetter.clear_line_edits(
        self.ui.blockName,
        self.ui.blockDisplayName,
        self.ui.blockBaseBlock
        )

        FieldResetter.reset_combo_boxes(
            self.ui.blockDropBox,
            self.ui.blockModel
        )

        FieldResetter.clear_labels(
            self.ui.blockTextureLabelTop,
            self.ui.blockTextureLabelLeft,
            self.ui.blockTextureLabelBack,
            self.ui.blockTextureLabelRight,
            self.ui.blockTextureLabelFront,
            self.ui.blockTextureLabelBottom
        )

        FieldResetter.uncheck_boxes(self.ui.blockDirectional)
        FieldResetter.clear_tree_selection(self.ui.elementViewer)

        self.blockTexture = {}
        self.populateBlockDrop()

    def addBlock(self):
        if self.validateBlockDetails() == 0: return

        self.blockProperties = {
            "name": self.ui.blockName.text(),
            "displayName": self.ui.blockDisplayName.text(),
            "baseBlock": self.ui.blockBaseBlock.text(),
            "textures": self.blockTexture,
            "placeSound": self.ui.blockPlaceSound.text(),
            "blockDrop": self.ui.blockDropBox.currentText(),
            "directional": self.ui.blockDirectional.isChecked(),
            "model": self.ui.blockModel.currentText(),
        }
        if not self.blockProperties["name"] in self.blocks:
            self.blocks[self.blockProperties["name"]] = self.blockProperties
            QTreeWidgetItem(self.blocks_tree, [self.blockProperties["name"]])
        else:
            self.blocks[self.blockProperties["name"]] = self.blockProperties

        self.clearBlockFields()

    def editBlock(self, block):
        properties = self.blocks[block]

        self.ui.blockName.setText(properties["name"])
        self.ui.blockDisplayName.setText(properties["displayName"])
        self.ui.blockBaseBlock.setText(properties["baseBlock"])
        self.ui.blockDropBox.setCurrentText(properties["blockDrop"])
        self.ui.blockPlaceSound.setText(properties["placeSound"])
        self.ui.blockDirectional.setChecked(properties["directional"])
        self.ui.blockModel.setCurrentText(properties["model"])
        self.blockTexture = properties["textures"]

        for face, path in self.blockTexture.items():
            pixmap = QPixmap.fromImage(QImage(path)).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

            label_map = {
                BlockFace.TOP: self.ui.blockTextureLabelTop,
                BlockFace.LEFT: self.ui.blockTextureLabelLeft,
                BlockFace.BACK: self.ui.blockTextureLabelBack,
                BlockFace.RIGHT: self.ui.blockTextureLabelRight,
                BlockFace.FRONT: self.ui.blockTextureLabelFront,
                BlockFace.BOTTOM: self.ui.blockTextureLabelBottom,
            }

            label = label_map.get(BlockFace(int(face)))
            if label:
                label.setPixmap(pixmap)

        
        self.ui.elementEditor.setCurrentIndex(ElementPage.BLOCKS)

    #######################
    # ITEMS TAB           #
    #######################

    def addItemTexture(self, path=None):
        if not path:
            texture, _ = QFileDialog.getOpenFileName(self, "Open Texture File", "", "PNG Files (*.png)")
            if not texture:
                return
        else:
            texture = path
        
        filename = os.path.basename(texture)
        destinationPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/items/{filename}'
        shutil.copyfile(texture, destinationPath)

        self.itemTexture = destinationPath

        image = QImage(self.itemTexture)
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        self.ui.itemTexture.setPixmap(pixmap)

    def newItem(self):
        self.ui.elementEditor.setCurrentIndex(ElementPage.ITEMS)

    def getItemModel(self, path=None):
        if path:
            filePath = path
            fileName = os.path.basename(filePath)
            destPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/items/{fileName}'
            shutil.copy(filePath, destPath)
            self.ui.itemModel.addItem(destPath)
            self.ui.itemModel.setCurrentText(destPath)
        
        elif self.ui.itemModel.currentText() != "Custom": return
        
        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if filePath:
            fileName = os.path.basename(filePath)
            destPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/items/{fileName}'
            shutil.copy(filePath, destPath)
            self.ui.itemModel.addItem(destPath)
            self.ui.itemModel.setCurrentText(destPath)

    def validateItemDetails(self):
        if not FieldValidator.validate_text_field(self.ui.itemDisplayName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Display Name"):
            return 0
        if not FieldValidator.validate_text_field(self.ui.itemName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Item Name"):
            return 0
        if not self.ui.itemBaseItem.text() in self.data["items"]:
            self.ui.itemBaseItem.setStyleSheet("QLineEdit { border: 1px solid red; }")
            alert("Please input a Minecraft item to the Base Item field!")
            return 0
        else:
            self.ui.itemBaseItem.setStyleSheet("")
        if self.itemTexture == None:
            self.ui.itemTextureButton.setStyleSheet("QLineEdit { border: 1px solid red; }")
            alert("Please select a valid texture!")
            return 0
        else:
            self.ui.itemTextureButton.setStyleSheet("")
        
        return 1

    def clearItemFields(self):
        FieldResetter.clear_line_edits(
            self.ui.itemName,
            self.ui.itemDisplayName,
            self.ui.itemBaseItem
        )

        FieldResetter.reset_combo_boxes(
            self.ui.itemModel,
            self.ui.itemRightClickMode
        )

        FieldResetter.reset_spin_boxes(
            self.ui.itemStackSize
        )

        FieldResetter.clear_text_edits(
            self.ui.itemRightClickFunc
        )

        FieldResetter.clear_labels(
            self.ui.itemTexture
        )

        FieldResetter.uncheck_boxes(
            self.ui.itemRightClickCheck
        )

        FieldResetter.clear_tree_selection(self.ui.elementViewer)

        self.itemTexture = None

    def addItem(self):
        if self.validateItemDetails() == 0: return

        rightClick = {"enabled":self.ui.itemRightClickCheck.isChecked(),"function":self.ui.itemRightClickFunc.toPlainText(),"mode":self.ui.itemRightClickMode.currentText().lower()}

        self.itemProperties = {
            "name": self.ui.itemName.text(),
            "displayName": self.ui.itemDisplayName.text(),
            "baseItem": self.ui.itemBaseItem.text(),
            "texture": self.itemTexture,
            "model": self.ui.itemModel.currentText().lower(),
            "stackSize": self.ui.itemStackSize.value(),
            "rightClick": rightClick,
        }

        if not self.itemProperties["name"] in self.items:
            QTreeWidgetItem(self.items_tree, [self.itemProperties["name"]])

        self.items[self.itemProperties["name"]] = self.itemProperties

        self.clearItemFields()

    def editItem(self, item):
        properties = self.items[item]

        self.ui.itemName.setText(properties["name"])
        self.ui.itemDisplayName.setText(properties["displayName"])
        self.ui.itemBaseItem.setText(properties["baseItem"])
        self.ui.itemModel.setCurrentText(properties["model"])
        self.ui.itemStackSize.setValue(properties["stackSize"])
        self.ui.itemRightClickFunc.setPlainText(properties["rightClick"]["function"])
        self.ui.itemRightClickMode.setCurrentText(properties["rightClick"]["mode"])
        self.ui.itemRightClickCheck.setChecked(properties["rightClick"]["enabled"])
        
        self.itemTexture = properties["texture"]

        pixmap = QPixmap.fromImage(QImage(properties["texture"])).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.itemTexture.setPixmap(pixmap)

        self.ui.elementEditor.setCurrentIndex(ElementPage.ITEMS)

    #######################
    # RECIPES TAB         #
    #######################

    def getRecipeItem(self, id_):
        slotId = id_
        self.block_popup = QWidget()
        self.ui_form = select_item.Ui_Form()
        self.ui_form.setupUi(self.block_popup)

        item_list = self.data["items"]

        if slotId in (9, 11, 13):
            for block in self.blocks: self.ui_form.itemsBox.addItem(f'{self.blocks[block]["name"]}')
            for item in self.items: self.ui_form.itemsBox.addItem(f'{self.items[item]["name"]}')

        for item in item_list: self.ui_form.itemsBox.addItem(item)

        self.ui_form.pushButton.clicked.connect(lambda: self.recipeCloseForm(slotId, self.ui_form.itemsBox.currentText()))

        self.block_popup.show()

    def recipeCloseForm(self, id_, item):
        self.recipe[id_] = item

        match id_:
            case 0:
                self.ui.slot0.setText(item)
            case 1:
                self.ui.slot1.setText(item)
            case 2:
                self.ui.slot2.setText(item)
            case 3:
                self.ui.slot3.setText(item)
            case 4:
                self.ui.slot4.setText(item)
            case 5:
                self.ui.slot5.setText(item)
            case 6:
                self.ui.slot6.setText(item)
            case 7:
                self.ui.slot7.setText(item)
            case 8:
                self.ui.slot8.setText(item)
            case 9:
                self.ui.slot9.setText(item)
            case 10:
                self.ui.smeltingInput.setText(item)
            case 11:
                self.ui.smeltingOutput.setText(item)
            case 12:
                self.ui.stoneCuttingInput.setText(item)
            case 13:
                self.ui.stoneCuttingOutput.setText(item)

        self.block_popup.close()

    def newRecipe(self):
        self.ui.elementEditor.setCurrentIndex(ElementPage.RECIPES)

    def validateRecipeDetails(self):
        if not FieldValidator.validate_text_field(self.ui.recipeName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Recipe Name"): 
            return 0
        if self.ui.slot9.text() == "" and self.ui.smeltingOutput.text() == "" and self.ui.stoneCuttingOutput.text() == "":
            alert("Recipes require outputs! Please add one before confirming!")
            return 0
        
        return 1

    def clearRecipeFields(self):
        FieldResetter.clear_line_edits(
            self.ui.recipeName,
            self.ui.slot0,
            self.ui.slot1,
            self.ui.slot2,
            self.ui.slot3,
            self.ui.slot4,
            self.ui.slot5,
            self.ui.slot6,
            self.ui.slot7,
            self.ui.slot8,
            self.ui.slot9,
            self.ui.smeltingInput,
            self.ui.smeltingOutput,
            self.ui.stoneCuttingInput,
            self.ui.stoneCuttingOutput
        )

        FieldResetter.reset_spin_boxes(
            self.ui.stoneCuttingCount,
            self.ui.slot9Count
        )

        FieldResetter.uncheck_boxes(
            self.ui.shapelessRadio,
            self.ui.exactlyRadio
        )

        self.recipe = {}

    def addRecipe(self):
        if self.validateRecipeDetails() == 0: return

        mode = "crafting"

        if self.ui.recipeSubTabs.tabText(self.ui.recipeSubTabs.currentIndex()).lower() == "crafting":
            mode = "crafting"
        elif self.ui.recipeSubTabs.tabText(self.ui.recipeSubTabs.currentIndex()).lower() == "smelting":
            mode = self.ui.smeltingModeBox.currentText().lower()
        elif self.ui.recipeSubTabs.tabText(self.ui.recipeSubTabs.currentIndex()).lower() == "stonecutting":
            mode = "stonecutting"

        self.recipeProperties = {
            "name": self.ui.recipeName.text(),
            "items": self.recipe,
            "outputCount": self.ui.slot9Count.value(),
            "outputCount2": self.ui.stoneCuttingCount.value(),
            "exact": self.ui.exactlyRadio.isChecked(),
            "shapeless": self.ui.shapelessRadio.isChecked(),
            "type": mode
        }

        if not self.recipeProperties["name"] in self.recipes:
            QTreeWidgetItem(self.recipes_tree, [self.recipeProperties["name"]])

        self.recipes[self.recipeProperties["name"]] = self.recipeProperties

        self.clearRecipeFields()

    def editRecipe(self, recipe):
        properties = self.recipes[recipe]

        self.ui.recipeName.setText(properties["name"])
        self.ui.shapelessRadio.setChecked(properties["shapeless"])
        self.ui.exactlyRadio.setChecked(properties["exact"])
        self.ui.slot9Count.setValue(properties["outputCount"])

        self.ui.slot0.setText(properties["items"][0])
        self.ui.slot1.setText(properties["items"][1])
        self.ui.slot2.setText(properties["items"][2])
        self.ui.slot3.setText(properties["items"][3])
        self.ui.slot4.setText(properties["items"][4])
        self.ui.slot5.setText(properties["items"][5])
        self.ui.slot6.setText(properties["items"][6])
        self.ui.slot7.setText(properties["items"][7])
        self.ui.slot8.setText(properties["items"][8])
        self.ui.slot9.setText(properties["items"][9])
        self.ui.smeltingInput.setText(properties["items"][10])
        self.ui.smeltingOutput.setText(properties["items"][11])

        self.ui.elementEditor.setCurrentIndex(ElementPage.RECIPES)

    #######################
    # PAINTINGS TAB       #
    #######################

    def addPaintingTexture(self, path=None):
        if not path:
            texture, _ = QFileDialog.getOpenFileName(self, "Open Texture File", "", "PNG Files (*.png)")
            if not texture:
                return
        else:
            texture = path

        filename = os.path.basename(texture)
        destinationPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/paintings/{filename}'
        shutil.copyfile(texture, destinationPath)

        self.paintingTexture = destinationPath

        image = QImage(self.paintingTexture)
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        self.ui.paintingTexture.setPixmap(pixmap)

    def newPainting(self):
        self.ui.elementEditor.setCurrentIndex(ElementPage.PAINTINGS)

    def validatePaintingDetails(self): 
        if not FieldValidator.validate_text_field(self.ui.paintingDisplayName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Display Name"):
            return 0
        if not FieldValidator.validate_text_field(self.ui.paintingName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Item Name"):
            return 0
        if self.paintingTexture == None:
            self.ui.paintingTextureButton.setStyleSheet("QLineEdit { border: 1px solid red; }")
            alert("Please select a valid texture!")
            return 0
        else:
            self.ui.paintingTextureButton.setStyleSheet("")

        return 1

    def clearPaintingFields(self):
        FieldResetter.clear_line_edits(
            self.ui.paintingDisplayName,
            self.ui.paintingName
        )

        FieldResetter.reset_spin_boxes(
            self.ui.paintingWidth,
            self.ui.paintingHeight
        )

        FieldResetter.clear_labels(
            self.ui.paintingTexture
        )

        FieldResetter.uncheck_boxes(
            self.ui.paintingPlaceable
        )

        self.paintingTexture = None

    def addPainting(self):
        if self.validatePaintingDetails() == 0: return

        self.paintingProperties = {
            "name": self.ui.paintingName.text(),
            "displayName": self.ui.paintingDisplayName.text(),
            "width": self.ui.paintingWidth.value(),
            "height": self.ui.paintingHeight.value(),
            "placeable": self.ui.paintingPlaceable.isChecked(),
            "texture": self.paintingTexture
        }

        if not self.paintingProperties["name"] in self.paintings:
            QTreeWidgetItem(self.paintings_tree, [self.paintingProperties["name"]])

        self.paintings[self.paintingProperties["name"]] = self.paintingProperties

        self.clearPaintingFields()

    def editPainting(self, painting):
        properties = self.paintings[painting]

        self.ui.paintingDisplayName.setText(properties["displayName"])
        self.ui.paintingName.setText(properties["name"])
        self.ui.paintingWidth.setValue(properties["width"])
        self.ui.paintingHeight.setValue(properties["height"])
        self.ui.paintingPlaceable.setChecked(properties["placeable"])
        
        self.paintingTexture = properties["texture"]
        pixmap = QPixmap.fromImage(QImage(properties["texture"])).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.paintingTexture.setPixmap(pixmap)

        self.ui.elementEditor.setCurrentIndex(ElementPage.PAINTINGS)

    #######################
    # PACK GENERATION     #
    #######################

    def generate(self):    
        version = self.packVersion.replace(".", "_")

        if getattr(sys, 'frozen', False):
            internal = 'src.'
        else:
            internal = ''

        generator = importlib.import_module(f'{internal}generation.v{version}.generator').Generator()

        loc = self.settings.get('file_export', 'defeault_export_location')
        if loc == 'default':
            loc = self.mainDirectory / 'exports'
            os.makedirs(loc, exist_ok=True)

        generator = generator(
            APP_VERSION,
            self.packDetails,
            self.dataFormat,
            self.resourceFormat,
            self.header,
            self.blocks,
            self.items,
            self.recipes,
            self.paintings,
            self.data,
            loc
        )

        generator.generateDatapack()

        alert("Pack Generated!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    app.setStyle("Fusion")
    sys.exit(app.exec())