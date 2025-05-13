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
        self.ui.actionExport_Project.triggered.connect(self.generateDatapack)

        self.ui.elementVeiwer.itemDoubleClicked.connect(self.elementClicked)

        self.ui.actionBlock.triggered.connect(self.newBlock)
        self.ui.actionItem.triggered.connect(self.newItem)
        self.ui.actionRecipe.triggered.connect(self.newRecipe)
        self.ui.actionPainting.triggered.connect(self.newPainting)

        # Block Specific Connections
        self.ui.blockTextureButtonTop.clicked.connect(lambda: self.addBlockTexture(0))
        self.ui.blockTextureButtonLeft.clicked.connect(lambda: self.addBlockTexture(1))
        self.ui.blockTextureButtonBack.clicked.connect(lambda: self.addBlockTexture(2))
        self.ui.blockTextureButtonRight.clicked.connect(lambda: self.addBlockTexture(3))
        self.ui.blockTextureButtonFront.clicked.connect(lambda: self.addBlockTexture(4))
        self.ui.blockTextureButtonBottom.clicked.connect(lambda: self.addBlockTexture(5))

        self.ui.blockModel.currentTextChanged.connect(self.getBlockModel)
        self.ui.blockConfirmButton.clicked.connect(self.addBlock)

        # Item Specific Connections
        self.ui.itemTextureButton.clicked.connect(self.addItemTexture)
        self.ui.itemConfirmButton.clicked.connect(self.addItem)

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

        self.exists = {}

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

        self.blocks_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Blocks"])
        for name in self.blocks:
            QTreeWidgetItem(self.blocks_tree, [name["name"]])
        
        self.items_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Items"])
        for name in self.items:
            QTreeWidgetItem(self.items_tree, [name["name"]])
        
        self.recipes_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Recipes"])
        for name in self.recipes:
            QTreeWidgetItem(self.recipes_tree, [name["name"]])
        
        self.paintings_tree = QTreeWidgetItem(self.ui.elementVeiwer, ["Paintings"])
        for name in self.paintings:
            QTreeWidgetItem(self.paintings, [name["name"]])

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

        label_map = {
            0: self.ui.blockTextureLabelTop,
            1: self.ui.blockTextureLabelLeft,
            2: self.ui.blockTextureLabelBack,
            3: self.ui.blockTextureLabelRight,
            4: self.ui.blockTextureLabelFront,
            5: self.ui.blockTextureLabelBottom,
        }
        label_map[textureId].setPixmap(pixmap)

    def newBlock(self):
        self.populateBlockDrop()
        self.ui.elementEditor.setCurrentIndex(1)

    def populateBlockDrop(self):
        self.ui.blockDropBox.clear()
        self.ui.blockDropBox.addItem('self')
        for block in self.blocks:
            self.ui.blockDropBox.addItem(block)
        for item in self.items:
            self.ui.blockDropBox.addItem(item)
        for item in self.data["items"]:
            self.ui.blockDropBox.addItem(item)

    def getBlockModel(self):
        if self.ui.blockModel.currentText() == "Custom":
            fileDialog = QFileDialog()
            filePath, _ = fileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
            fileName = os.path.basename(filePath)
            destPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/blocks/{fileName}'

            shutil.copy(filePath, destPath)

            if filePath:
                self.ui.blockModel.addItem(destPath)
                self.ui.blockModel.setCurrentText(destPath)

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

    def clearBlockFields(self):
        self.ui.blockName.setText("")
        self.ui.blockDisplayName.setText("")
        self.ui.blockBaseBlock.setText("")
        self.ui.blockDropBox.setCurrentText("")
        self.ui.blockPlaceSound.setText("")
        self.ui.blockDirectional.setChecked(False)
        self.ui.blockModel.setCurrentText("")

        self.ui.blockTextureLabelTop.clear()
        self.ui.blockTextureLabelLeft.clear()
        self.ui.blockTextureLabelBack.clear()
        self.ui.blockTextureLabelRight.clear()
        self.ui.blockTextureLabelFront.clear()
        self.ui.blockTextureLabelBottom.clear()

        self.blockTexture = {}

        self.ui.elementVeiwer.clearSelection()

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

        for textureId in self.blockTexture:
            image = QImage(self.blockTexture[textureId])
            pixmap = QPixmap.fromImage(image).scaled(
                50, 50, Qt.AspectRatioMode.KeepAspectRatio
            )

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

    #######################
    # ITEMS TAB           #
    #######################

    def addItemTexture(self):
        texture, _ = QFileDialog.getOpenFileName(self, "Open Texture File", "", "PNG Files (*.png)")
        if not texture:
            return
        
        filename = os.path.basename(texture)
        destinationPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/items/{filename}'
        shutil.copyfile(texture, destinationPath)

        self.itemTexture = destinationPath

        image = QImage(self.itemTexture)
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        self.ui.itemTexture.setPixmap(pixmap)

    def newItem(self):
        self.ui.elementEditor.setCurrentIndex(3)

    def validateItemDetails(self):
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

        if not validate(self.ui.itemDisplayName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Display Name"):
            return 0
        if not validate(self.ui.itemName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Item Name"):
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
        self.ui.itemName.setText("")
        self.ui.itemDisplayName.setText("")
        self.ui.itemBaseItem.setText("")
        self.ui.itemModel.setCurrentText("Generated")
        self.ui.itemStackSize.setValue(64)
        self.ui.itemRightClickFunc.clear()
        self.ui.itemRightClickMode.setCurrentText("Tick")
        self.ui.itemRightClickCheck.setChecked(False)

        self.ui.itemTexture.clear()

        self.itemTexture = None

        self.ui.elementVeiwer.clearSelection()

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
        self.ui.elementEditor.setCurrentIndex(2)

    def validateRecipeDetails(self):
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
        
        if not validate(self.ui.recipeName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Recipe Name"): 
            return 0
        if self.ui.slot9.text() == "" and self.ui.smeltingOutput.text() == "" and self.ui.stoneCuttingOutput.text() == "":
            alert("Recipes require outputs! Please add one before confirming!")
            return 0
        
        return 1

    def clearRecipeFields(self):
        self.recipe = {}
        self.ui.recipeName.setText("")
        self.ui.shapelessRadio.setChecked(False)
        self.ui.exactlyRadio.setChecked(False)
        self.ui.slot0.setText("")
        self.ui.slot1.setText("")
        self.ui.slot2.setText("")
        self.ui.slot3.setText("")
        self.ui.slot4.setText("")
        self.ui.slot5.setText("")
        self.ui.slot6.setText("")
        self.ui.slot7.setText("")
        self.ui.slot8.setText("")
        self.ui.slot9.setText("")
        self.ui.smeltingInput.setText("")
        self.ui.smeltingOutput.setText("")
        self.ui.stoneCuttingCount.setValue(1)
        self.ui.stoneCuttingOutput.setText("")
        self.ui.stoneCuttingInput.setText("")

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

    #######################
    # PAINTINGS TAB       #
    #######################

    def addPaintingTexture(self):
        texture, _ = QFileDialog.getOpenFileName(self, "Open Texture File", "", "PNG Files (*.png)")
        if not texture:
            return
        
        filename = os.path.basename(texture)
        destinationPath = f'{self.mainDirectory}/workspaces/{self.packDetails["namespace"]}/assets/paintings/{filename}'
        shutil.copyfile(texture, destinationPath)

        self.paintingTexture = destinationPath

        image = QImage(self.itemTexture)
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        self.ui.paintingTexture.setPixmap(pixmap)

    def newPainting(self):
        self.ui.elementEditor.setCurrentIndex(4)

    def validatePaintingDetails(self):
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
        
        if not validate(self.ui.paintingDisplayName, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-!0123456789", "Display Name"):
            return 0
        if not validate(self.ui.paintingName, "abcdefghijklmnopqrstuvwxyz_0123456789", "Item Name"):
            return 0
        if self.paintingTexture == None:
            self.ui.paintingTextureButton.setStyleSheet("QLineEdit { border: 1px solid red; }")
            alert("Please select a valid texture!")
            return 0
        else:
            self.ui.paintingTextureButton.setStyleSheet("")

        return 1

    def clearPaintingFields(self):
        self.paintingTexture = None
        self.ui.paintingDisplayName.setText("")
        self.ui.paintingName.setText("")
        self.ui.paintingWidth.setValue(1)
        self.ui.paintingHeight.setValue(1)
        self.ui.paintingPlaceable.setChecked(False)
        self.ui.paintingTexture.clear()

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

    #######################
    # PACK GENERATION     #
    #######################

    def generateResourcePack(self):
        self.resPackDirectory = os.path.join(self.outputDir, f"{self.packName} Resource Pack")
        os.makedirs(self.resPackDirectory, exist_ok=True)
        assets_dir = os.path.join(self.resPackDirectory, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        version = self.packVersion.replace(".", "_")
        is_legacy = self.packVersion == "1.21.3"

        if is_legacy:
            # Legacy 1.21.3 folder structure
            mc_path = os.path.join(assets_dir, "minecraft")
            os.makedirs(os.path.join(mc_path, "atlases"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "models"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "textures"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "textures", "item"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "models", "item"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "models", self.packNamespace), exist_ok=True)

            # Atlas
            atlas_path = os.path.join(mc_path, "atlases", "blocks.json")
            with open(atlas_path, "w") as file:
                json.dump({
                    "sources": [{
                        "type": "directory",
                        "source": self.packNamespace,
                        "prefix": f"{self.packNamespace}/"
                    }]
                }, file, indent=4)
        else:
            # Modern format
            ns_path = os.path.join(assets_dir, self.packNamespace)
            os.makedirs(os.path.join(ns_path, "items"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "models", "item"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "textures", "item"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "textures", "painting"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "models"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "textures"), exist_ok=True)

        # pack.mcmeta
        with open(os.path.join(self.resPackDirectory, "pack.mcmeta"), "w") as pack:
            json.dump({
                "pack": {
                    "pack_format": self.resourceFormat,
                    "description": self.packDescription
                }
            }, pack, indent=4)

        # Load resource generators
        internal = 'src.' if getattr(sys, 'frozen', False) else ''
        BlockResourcer = importlib.import_module(f"{internal}generation.v{version}.blocks").BlockResourcer
        ItemResourcer = importlib.import_module(f"{internal}generation.v{version}.items").ItemResourcer
        if not is_legacy:
            PaintingResourcer = importlib.import_module(f"{internal}generation.v{version}.paintings").PaintingResourcer

        # Generate resources
        if self.blocks:
            blockResourcer = BlockResourcer(self.resPackDirectory, self.packNamespace, self.blocks)
            blockResourcer.generate()

        if self.items:
            itemResourcer = ItemResourcer(
                self.resPackDirectory,
                self.packNamespace,
                self.exists,
                self.data,
                self.items,
            )
            itemResourcer.generate()

        if self.paintings and not is_legacy:
            paintingResourcer = PaintingResourcer(
                self.resPackDirectory,
                self.packNamespace,
                self.paintings
            )
            paintingResourcer.generate()

    def generateDatapack(self):
        self.outputDir = QFileDialog.getExistingDirectory(self, "Output Directory", "")
        if not self.outputDir:
            alert("Please select a valid output directory!")
            return
        
        self.packName = self.packDetails["name"]
        self.packNamespace = self.packDetails["namespace"]
        self.packDescription = self.packDetails["description"]
        self.packAuthor = self.packDetails["author"]
        self.packVersion = self.packDetails["version"]
        
        self.packDirectory = os.path.join(self.outputDir, self.packName)

        # Create base directories
        os.makedirs(self.packDirectory, exist_ok=True)
        os.makedirs(os.path.join(self.packDirectory, "data"), exist_ok=True)

        self.namespaceDirectory = os.path.join(self.packDirectory, "data", self.packNamespace)
        self.minecraftDirectory = os.path.join(self.packDirectory, "data", "minecraft")

        os.makedirs(self.minecraftDirectory, exist_ok=True)
        os.makedirs(self.namespaceDirectory, exist_ok=True)

        # Write pack.mcmeta
        pack_meta = {
            "pack": {
                "pack_format": self.dataFormat,
                "description": self.packDescription
            }
        }
        with open(os.path.join(self.packDirectory, "pack.mcmeta"), "w") as f:
            json.dump(pack_meta, f, indent=4)

        # Create feature folders
        os.makedirs(os.path.join(self.namespaceDirectory, "function"), exist_ok=True)
        if self.blocks or self.items:
            os.makedirs(os.path.join(self.namespaceDirectory, "advancement"), exist_ok=True)
        if self.blocks:
            os.makedirs(os.path.join(self.namespaceDirectory, "loot_table"), exist_ok=True)
        if self.recipes:
            os.makedirs(os.path.join(self.namespaceDirectory, "recipe"), exist_ok=True)

        # Create tags folders
        tags_function_dir = os.path.join(self.minecraftDirectory, "tags", "function")
        os.makedirs(tags_function_dir, exist_ok=True)

        # Write tick.mcfunction
        tick_path = os.path.join(self.namespaceDirectory, "function", "tick.mcfunction")
        with open(tick_path, "w") as tick:
            if self.blocks:
                tick.write(f"{self.header}execute as @e[type=item_display,tag={self.packAuthor}.custom_block] at @s run function {self.packNamespace}:blocks/as_blocks")
            else:
                tick.write(self.header)

        # Write load.mcfunction
        load_path = os.path.join(self.namespaceDirectory, "function", "load.mcfunction")
        with open(load_path, "w") as load:
            load.write(f'{self.header}tellraw @a {{"text":"[mDirt {APP_VERSION}] - Successfully loaded pack!","color":"red"}}')

        # Write tick/load JSON tags
        tick_json_path = os.path.join(tags_function_dir, "tick.json")
        load_json_path = os.path.join(tags_function_dir, "load.json")

        with open(tick_json_path, "w") as tick:
            json.dump({"values": [f"{self.packNamespace}:tick"]}, tick, indent=4)

        with open(load_json_path, "w") as load:
            json.dump({"values": [f"{self.packNamespace}:load"]}, load, indent=4)
        
        version = self.packVersion.replace(".", "_")

        if getattr(sys, 'frozen', False):
            internal = 'src.'
        else:
            internal = ''

        BlockGenerator = importlib.import_module(f"{internal}generation.v{version}.blocks").BlockGenerator
        ItemGenerator = importlib.import_module(f"{internal}generation.v{version}.items").ItemGenerator
        RecipeGenerator = importlib.import_module(f"{internal}generation.v{version}.recipes").RecipeGenerator
        if self.packVersion != "1.21.3":
            PaintingGenerator = importlib.import_module(f"{internal}generation.v{version}.paintings").PaintingGenerator

        #######################
        # CUSTOM BLOCKS       #
        #######################

        if self.blocks:
            blockGenerator = BlockGenerator(
                self.header,
                self.namespaceDirectory,
                self.packNamespace,
                self.packAuthor,
                self.blocks,
                self.items,
            )

            blockGenerator.generate()

        #######################
        # CUSTOM ITEMS        #
        #######################

        if self.items:
            itemGenerator = ItemGenerator(
                self.header, 
                self.namespaceDirectory, 
                self.items,
                self.packNamespace
            )

            itemGenerator.generate()

        #######################
        # CUSTOM RECIPES      #
        #######################

        if self.recipes:
            recipeGenerator = RecipeGenerator(
                self.namespaceDirectory,
                self.packNamespace,
                self.packAuthor,
                self.blocks,
                self.items,
                self.recipes,
            )

            recipeGenerator.generate()
        
        #######################
        # CUSTOM PAINTINGS    #
        #######################

        if self.paintings and self.packVersion != "1.21.3":
            paintingGenerator = PaintingGenerator(
                self.header,
                self.namespaceDirectory,
                self.packNamespace,
                self.packAuthor,
                self.paintings,
                self.minecraftDirectory,
            )

            paintingGenerator.generate()

        #######################
        # RESOURCE PACK       #
        #######################

        self.generateResourcePack()

        #######################
        # FINISH GENERATE     #
        #######################

        alert("Pack Generated!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.setStyle("Fusion")
    sys.exit(app.exec())