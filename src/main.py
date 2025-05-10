import datetime, json, os, re, sys, details, requests, importlib, shutil, pickle

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QWidget, QDialog

from select_item import Ui_Form
from ui import Ui_MainWindow

from updater import Updater, ModuleGrabber


def alert(message):
    messageBox = QMessageBox()
    messageBox.setIcon(QMessageBox.Icon.Information)
    messageBox.setText(message)
    messageBox.setWindowTitle("Alert")
    messageBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    messageBox.exec()

def checkInputValid(input_, type_):
    return (
        "empty"
        if not input_.text()
        else (
            "type"
            if type_ == "strict"
            and (
                not input_.text().islower()
                or any(char.isspace() or char.isdigit() for char in input_.text())
            )
            else (
                "valid"
                if type_ == "strict"
                else (
                    "valid"
                    if type_ == "string"
                    and re.match(r"^[^<>:\"//|?*\x00-\x1F]+$", input_.text())
                    and input_.text().strip() != ""
                    else (
                        "type"
                        if type_ == "string"
                        else (
                            "valid"
                            if type_ == "integer" and input_.text().isdigit()
                            else "type"
                        )
                    )
                )
            )
        )
    )

class App(QMainWindow):

    #######################
    # APP SETUP STUFF     #
    #######################
    
    def __init__(self):
        super().__init__()
        
        self.appVersion = "3.0.0"
        # self.checkUpdate()

        # Make PyCharm stop yelling at me
        self.exists = {}
        self.resPackDirectory = None
        self.minecraftDirectory = None
        self.namespaceDirectory = None
        self.packDirectory = None
        self.outputDir = None
        self.packAuthor = None
        self.packDescription = None
        self.packNamespace = None
        self.packName = None
        self.default_items = None
        self.default_blocks = None
        self.recipeProperties = None
        self.ui_form = None
        self.block_popup = None
        self.itemProperties = None
        self.blockProperties = None
        self.header = None
        self.recipe = None
        self.itemTexture = None
        self.blockTexture = {}
        self.recipes = None
        self.items = None
        self.blocks = None
        self.data = None
        self.mainDirectory = None

        self.featureNum = 0

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Grab supported versions
        self.populateVersions()

        # Launch Details Menu
        self.launchDetails()

        # Block Signals
        self.ui.blockAddButton.clicked.connect(self.addBlock)
        self.ui.blockEditButton.clicked.connect(self.editBlock)
        self.ui.blockRemoveButton.clicked.connect(self.removeBlock)

        self.ui.blockTextureButtonTop.clicked.connect(lambda: self.getBlockTexture(0))
        self.ui.blockTextureButtonLeft.clicked.connect(lambda: self.getBlockTexture(1))
        self.ui.blockTextureButtonBack.clicked.connect(lambda: self.getBlockTexture(2))
        self.ui.blockTextureButtonRight.clicked.connect(lambda: self.getBlockTexture(3))
        self.ui.blockTextureButtonFront.clicked.connect(lambda: self.getBlockTexture(4))
        self.ui.blockTextureButtonBottom.clicked.connect(lambda: self.getBlockTexture(5))

        self.ui.blockModel.activated.connect(self.getBlockModel)

        self.ui.mainTab.currentChanged.connect(self.loadBlockDropBox)

        # Item Signals
        self.ui.itemAddButton.clicked.connect(self.addItem)
        self.ui.itemEditButton.clicked.connect(self.editItem)
        self.ui.itemRemoveButton.clicked.connect(self.removeItem)

        self.ui.itemTextureButton.clicked.connect(self.getItemTexture)

        self.ui.itemModel.activated.connect(self.getItemModel)

        # Recipe Signals
        self.ui.recipeAddButton.clicked.connect(self.addRecipe)
        self.ui.recipeEditButton.clicked.connect(self.editRecipe)
        self.ui.recipeRemoveButton.clicked.connect(self.removeRecipe)

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

        # Painting Signals
        self.ui.paintingAddButton.clicked.connect(self.addPainting)
        self.ui.paintingEditButton.clicked.connect(self.editPainting)
        self.ui.paintingRemoveButton.clicked.connect(self.removePainting)

        self.ui.paintingTextureButton.clicked.connect(self.getPaintingTexture)

        # Enable / Disable Text Edit
        self.ui.itemRightClickCheck.checkStateChanged.connect(self.enableRightClickFunc)
        self.enableRightClickFunc()

        # Import & Export
        self.ui.actionImport_mdrt.triggered.connect(lambda: self.importProject(self.appVersion))
        self.ui.actionExport_mdrt.triggered.connect(lambda: self.exportProject(self.appVersion))

        # Generate
        self.ui.packGenerate.clicked.connect(self.generateDataPack)
    
    def launchDetails(self):
        self.details_popup = QWidget()
        self.detail_form = details.Ui_Form()
        self.detail_form.setupUi(self.details_popup)
        self.details_popup.show()

        for version in self.supportedVersions:
            if version != "1.21.3": self.detail_form.packVersion.addItem(version)

        self.detail_form.packGenerate.clicked.connect(lambda: self.closeDetailPopup(self.details_popup,
                                                                                    self.detail_form.packName.text(), 
                                                                                    self.detail_form.packNamespace.text(), 
                                                                                    self.detail_form.packAuthor.text(), 
                                                                                    self.detail_form.packDescription.text(), 
                                                                                    self.detail_form.packVersion.currentText())
                                                                                    )

    def closeDetailPopup(self, detail_popup,
                         packName,
                         packNamespace,
                         packAuthor,
                         packPrefix,
                         packDesc,
                         packVer):
        
        self.packName = packName
        self.packNamespace = packNamespace
        self.packAuthor = packAuthor
        self.packDescription = packDesc
        self.packVersion = packVer
        self.ui.packName.setText(packName)
        self.ui.packNamespace.setText(packNamespace)
        self.ui.packAuthor.setText(packAuthor)
        self.ui.packDescription.setText(packDesc)
        self.ui.packVersion.addItem(packVer)
        
        detail_popup.close()

        self.grabModule()

        self.setupData()
    
    def populateVersions(self):
        version_url = "https://raw.githubusercontent.com/Faith-and-Code-Technologies/mDirt-2/main/lib/version_list.json"
        try:
            response = requests.get(version_url)
            if response.status_code == 200:
                self.version_json = response.json()
                self.supportedVersions = self.version_json["versions"]
            else:
                alert(f"Failed to download Supported Version list. Status code: {response.status_code}. Relaunch mDirt and try again. If the problem persists, submit an issue here: https://github.com/Faith-and-Code-Technologies/mDirt-2/issues")
        except:
            alert(f"Failed to download Supported Version list. Relaunch mDirt and try again. If the problem persists, submit an issue here: https://github.com/Faith-and-Code-Technologies/mDirt-2/issues")

    def grabModule(self):
        self.moduleGrab = ModuleGrabber(
            base_url="https://github.com/Faith-and-Code-Technologies/mDirt-2/raw/main/"
        )
        #self.moduleGrab.update_module(version=self.packVersion)

    def setupData(self):
        self.mainDirectory = f"{os.path.dirname(os.path.abspath(__file__))}/.."
        self.data = json.load(open(os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), f"lib/{self.packVersion}_data.json"), "r"))

        dataformat = self.version_json["dataformat"]
        resourceformat = self.version_json["resourceformat"]

        self.dataFormat = dataformat[self.packVersion]
        self.resourceFormat = resourceformat[self.packVersion]

        self.blocks = {}
        self.items = {}
        self.recipes = {}
        self.paintings = {}

        self.blockTexture = {}
        self.itemTexture = None
        self.recipe = {}
        self.paintingTexture = None

        self.header = f"""
        #####################################
        #   This File Was Created By mDirt  #
        #               v{self.appVersion}              #
        #   Copyright 2025 by Jupiter Dev   #
        #####################################
        \n"""

    def checkUpdate(self):
        self.updater = Updater(
            repo_url="https://github.com/Faith-and-Code-Technologies/mDirt-2",
            current_version=self.appVersion
        )

        if self.updater.is_update_available():
            # self.update_popup = QDialog()
            # self.update_form = ui_updater.Ui_Dialog()
            # self.update_form.setupUi(self.update_popup)
            # self.update_popup.show()
            pass

    #######################
    # IMPORT & EXPORT     #
    #######################

    def exportProject(self, version):
        data = {
            "file_type": "mDirtProjectData",
            "version": version,
            "metadata": {
                "exported_at": datetime.datetime.now(datetime.UTC).isoformat()
            },
            "content": {
                "pack_info": {
                    "packName": self.ui.packName.text(),
                    "packNamespace": self.ui.packNamespace.text(),
                    "author": self.ui.packAuthor.text(),
                    "description": self.ui.packDescription.text(),
                    "version": self.ui.packVersion.currentText(),
                },
                "elements": {
                    "blocks": self.blocks,
                    "items": self.items,
                    "recipes": self.recipes,
                },
            },
        }

        file = QFileDialog.getExistingDirectory(self, "Save mDirt Project", "")

        if file:
            with open(f'{file}/mDirtProject.mdrt', "wb") as f:
                pickle.dump(data, f)

    def importProject(self, version):
        file, _ = QFileDialog.getOpenFileName(
            self, "Open mDirt Project", "", "mDirt File (*.mdrt)"
        )

        if file:
            with open(file, "rb") as f:
                data = pickle.load(f)
        else:
            alert("Please Select a Valid File!")
            return

        if data["file_type"] != "mDirtProjectData":
            alert("Invalid File!")
            return

        if data["version"] != version:
            alert(f"Incompatible version!")

        self.ui.packName.setText(data["content"]["pack_info"]["packName"])
        self.ui.packNamespace.setText(data["content"]["pack_info"]["packNamespace"])
        self.ui.packAuthor.setText(data["content"]["pack_info"]["author"])
        self.ui.packDescription.setText(data["content"]["pack_info"]["description"])
        self.ui.packVersion.setCurrentText(data["content"]["pack_info"]["version"])
        self.blocks = data["content"]["elements"]["blocks"]
        self.items = data["content"]["elements"]["items"]
        self.recipes = data["content"]["elements"]["recipes"]

        self.featureNum = 0

        for block in self.blocks:
            self.ui.blockList.addItem(self.blocks[block]["name"])
            self.featureNum += 1
        for item in self.items:
            self.ui.itemList.addItem(self.items[item]["name"])
            self.featureNum += 1
        for recipe in self.recipes:
            self.ui.recipeList.addItem(self.recipes[recipe]["name"])

    #######################
    # BLOCKS TAB          #
    #######################

    def loadBlockDropBox(self):
        self.ui.blockDropBox.clear()
        item_list = self.data["items"]
        self.ui.blockDropBox.addItem("self")
        for block in self.blocks:
            self.ui.blockDropBox.addItem(f'{self.blocks[block]["name"]}')
        for item in self.items:
            self.ui.blockDropBox.addItem(f'{self.items[item]["name"]}')
        for item in item_list:
            self.ui.blockDropBox.addItem(item)

    def getBlockModel(self):
        if self.ui.blockModel.currentText() == "Custom":
            fileDialog = QFileDialog()
            filePath, _ = fileDialog.getOpenFileName(
                self, "Open JSON File", "", "JSON Files (*.json)"
            )

            if filePath:
                self.ui.blockModel.addItem(filePath)
                self.ui.blockModel.setCurrentText(filePath)

    def getBlockTexture(self, id_):
        textureId = id_
        self.blockTexture[textureId], _ = QFileDialog.getOpenFileName(
            self, "Open Texture File", "", "PNG Files (*.png)"
        )
        if not self.blockTexture[textureId]:
            return
        image = QImage(self.blockTexture[textureId])
        pixmap = QPixmap.fromImage(image).scaled(
            50, 50, Qt.AspectRatioMode.KeepAspectRatio
        )

        if textureId == 0:
            self.ui.blockTextureTop.setPixmap(pixmap)
        if textureId == 1:
            self.ui.blockTextureLeft.setPixmap(pixmap)
        if textureId == 2:
            self.ui.blockTextureBack.setPixmap(pixmap)
        if textureId == 3:
            self.ui.blockTextureRight.setPixmap(pixmap)
        if textureId == 4:
            self.ui.blockTextureFront.setPixmap(pixmap)
        if textureId == 5:
            self.ui.blockTextureBottom.setPixmap(pixmap)

    def addBlock(self):

        self.featureNum += 1

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

        self.blocks[self.blockProperties["name"]] = self.blockProperties

        self.ui.blockList.addItem(self.blockProperties["name"])

        self.clearBlockFields()

    def editBlock(self):
        curItem = self.ui.blockList.currentRow()
        curItem = self.ui.blockList.item(curItem).text()
        properties = self.blocks[curItem]

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
                self.ui.blockTextureTop.setPixmap(pixmap)
            if textureId == 1:
                self.ui.blockTextureLeft.setPixmap(pixmap)
            if textureId == 2:
                self.ui.blockTextureBack.setPixmap(pixmap)
            if textureId == 3:
                self.ui.blockTextureRight.setPixmap(pixmap)
            if textureId == 4:
                self.ui.blockTextureFront.setPixmap(pixmap)
            if textureId == 5:
                self.ui.blockTextureBottom.setPixmap(pixmap)

        self.removeBlock(self.ui.blockList.currentRow())

    def removeBlock(self, item=None):
        curItem = item
        if not item:
            curItem = self.ui.blockList.currentRow()

        self.blocks.pop(self.ui.blockList.item(curItem).text())
        self.ui.blockList.takeItem(curItem)

    def clearBlockFields(self):
        self.ui.blockName.setText("")
        self.ui.blockDisplayName.setText("")
        self.ui.blockBaseBlock.setText("")
        self.ui.blockDropBox.setCurrentText("")
        self.ui.blockPlaceSound.setText("")
        self.ui.blockDirectional.setChecked(False)
        self.ui.blockModel.setCurrentText("")

        self.ui.blockTextureTop.clear()
        self.ui.blockTextureLeft.clear()
        self.ui.blockTextureBack.clear()
        self.ui.blockTextureRight.clear()
        self.ui.blockTextureFront.clear()
        self.ui.blockTextureBottom.clear()

        self.blockTexture = {}

    #######################
    # ITEMS TAB           #
    #######################
    
    def enableRightClickFunc(self):
        if self.ui.itemRightClickCheck.isChecked():
            self.ui.itemRightClickFunc.setEnabled(True)
            self.ui.itemRightClickMode.setEnabled(True)
        else:
            self.ui.itemRightClickFunc.setEnabled(False)
            self.ui.itemRightClickMode.setEnabled(False)

    def getItemModel(self):
        if self.ui.itemModel.currentText() == "Custom":
            fileDialog = QFileDialog()
            filePath, _ = fileDialog.getOpenFileName(
                self, "Open JSON File", "", "JSON Files (*.json)"
            )

            if filePath:
                self.ui.itemModel.addItem(filePath)
                self.ui.itemModel.setCurrentText(filePath)

    def getItemTexture(self):
        self.itemTexture, _ = QFileDialog.getOpenFileName(
            self, "Open Texture File", "", "PNG Files (*.png)"
        )
        if not self.itemTexture:
            return
        image = QImage(self.itemTexture)
        pixmap = QPixmap.fromImage(image).scaled(
            50, 50, Qt.AspectRatioMode.KeepAspectRatio
        )

        self.ui.itemTexture.setPixmap(pixmap)

    def addItem(self):

        self.featureNum += 1

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

        self.items[self.itemProperties["name"]] = self.itemProperties
        self.ui.itemList.addItem(self.itemProperties["name"])
        self.clearItemFields()

    def editItem(self):
        curItem = self.ui.itemList.currentRow()
        curItem = self.ui.itemList.item(curItem).text()
        properties = self.items[curItem]

        self.ui.itemName.setText(properties["name"])
        self.ui.itemDisplayName.setText(properties["displayName"])
        self.ui.itemBaseItem.setText(properties["baseItem"])
        self.ui.itemModel.setCurrentText(properties["model"])
        self.ui.itemStackSize.setValue(properties["stackSize"])
        self.ui.itemRightClickFunc.setPlainText(properties["rightClick"]["function"])
        self.ui.itemRightClickMode.setCurrentText(properties["rightClick"]["mode"])
        self.ui.itemRightClickCheck.setChecked(properties["rightClick"]["enabled"])

        self.itemTexture = properties["texture"]

        pixmap = QPixmap.fromImage(QImage(properties["texture"])).scaled(
            50, 50, Qt.AspectRatioMode.KeepAspectRatio
        )
        self.ui.itemTexture.setPixmap(pixmap)

        self.removeItem(self.ui.itemList.currentRow())

    def removeItem(self, item=None):
        curItem = item
        if not item:
            curItem = self.ui.itemList.currentRow()

        self.items.pop(self.ui.itemList.item(curItem).text())
        self.ui.itemList.takeItem(curItem)

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

    #######################
    # RECIPES TAB         #
    #######################

    def getRecipeItem(self, id_):
        slotId = id_
        self.block_popup = QWidget()
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self.block_popup)

        item_list = self.data["items"]

        if slotId in (9, 11, 13):
            for block in self.blocks:
                self.ui_form.itemsBox.addItem(f'{self.blocks[block]["name"]}')
            for item in self.items:
                self.ui_form.itemsBox.addItem(f'{self.items[item]["name"]}')

        for item in item_list:
            self.ui_form.itemsBox.addItem(item)

        self.ui_form.pushButton.clicked.connect(
            lambda: self.recipeCloseForm(slotId, self.ui_form.itemsBox.currentText())
        )

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

    def addRecipe(self):

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

        self.recipes[self.recipeProperties["name"]] = self.recipeProperties
        self.ui.recipeList.addItem(self.recipeProperties["name"])
        self.clearRecipeFields()

    def editRecipe(self):
        curItem = self.ui.recipeList.currentRow()
        curItem = self.ui.recipeList.item(curItem).text()
        properties = self.recipes[curItem]

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

        self.removeRecipe(self.ui.recipeList.currentRow())

    def removeRecipe(self, item=None):
        curItem = item
        if not item:
            curItem = self.ui.recipeList.currentRow()

        self.recipes.pop(self.ui.recipeList.item(curItem).text())
        self.ui.recipeList.takeItem(curItem)

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

    #######################
    # PAINTINGS TAB       #
    #######################

    def getPaintingTexture(self):
        self.paintingTexture, _ = QFileDialog.getOpenFileName(
            self, "Open Texture File", "", "PNG Files (*.png)"
        )

        if not self.paintingTexture:
            return
        
        image = QImage(self.paintingTexture)
        pixmap = QPixmap.fromImage(image).scaled(
            50, 50, Qt.AspectRatioMode.KeepAspectRatio
        )

        self.ui.paintingTexture.setPixmap(pixmap)

    def addPainting(self):
        self.paintingProperties = {
            "name": self.ui.paintingName.text(),
            "displayName": self.ui.paintingDisplayName.text(),
            "width": self.ui.paintingWidth.value(),
            "height": self.ui.paintingHeight.value(),
            "placeable": self.ui.paintingPlaceable.isChecked(),
            "texture": self.paintingTexture
        }

        self.paintings[self.paintingProperties["name"]] = self.paintingProperties
        self.ui.paintingList.addItem(self.paintingProperties["name"])
        self.clearPaintingFields()

    def editPainting(self):
        curItem = self.ui.paintingList.currentRow()
        curItem = self.ui.paintingList.item(curItem).text()
        properties = self.paintings[curItem]

        self.ui.paintingDisplayName.setText(properties["displayName"])
        self.ui.paintingName.setText(properties["name"])
        self.ui.paintingWidth.setValue(properties["width"])
        self.ui.paintingHeight.setValue(properties["height"])
        self.ui.paintingPlaceable.setChecked(properties["placeable"])

        self.removePainting(self.ui.paintingList.currentRow())

    def removePainting(self, item=None):
        curItem = item
        if not item:
            curItem = self.ui.paintingList.currentRow()
        
        self.paintings.pop(self.ui.paintingList.item(curItem).text())
        self.ui.paintingList.takeItem(curItem)

    def clearPaintingFields(self):
        self.paintingTexture = None
        self.ui.paintingDisplayName.setText("")
        self.ui.paintingName.setText("")
        self.ui.paintingWidth.setValue(1)
        self.ui.paintingHeight.setValue(1)
        self.ui.paintingPlaceable.setChecked(False)
        self.ui.paintingTexture.clear()

    #######################
    # ERROR CHECKING      #
    #######################

    def checkInputs(self):
        self.default_blocks = self.data["blocks"]
        self.default_items = self.data["items"]

        for block in self.blocks:
            if self.blocks[block]["baseBlock"] not in self.default_blocks:
                block_name = self.blocks[block]["name"]
                alert(
                    f"Block '{block_name}' has an unsupported Base Block!"
                )
                return

        for item in self.items:
            if self.items[item]["baseItem"] not in self.default_items:
                item_name = self.items[item]["name"]
                alert(
                    f"Item '{item_name}' has an unsupported Base Item!"
                )
                return

        if checkInputValid(self.ui.packName, "string") == "empty":
            alert("Pack Name is empty!")
            return
        if checkInputValid(self.ui.packName, "string") == "type":
            alert("Pack Name has unsupported characters!")
            return
        elif checkInputValid(self.ui.packName, "string") == "valid":
            self.packName = self.ui.packName.text()

        if checkInputValid(self.ui.packNamespace, "strict") == "empty":
            alert("Pack Namespace is empty!")
            return
        if checkInputValid(self.ui.packNamespace, "strict") == "type":
            alert("Pack Namespace has unsupported characters!")
            return
        elif checkInputValid(self.ui.packNamespace, "strict") == "valid":
            self.packNamespace = self.ui.packNamespace.text()

        if checkInputValid(self.ui.packDescription, "string") == "empty":
            alert("Pack Description is empty!")
            return
        if checkInputValid(self.ui.packDescription, "string") == "type":
            alert("Pack Description has unsupported characters!")
            return
        elif checkInputValid(self.ui.packDescription, "string") == "valid":
            self.packDescription = self.ui.packDescription.text()

        if checkInputValid(self.ui.packAuthor, "strict") == "empty":
            alert("Pack Author is empty!")
            return
        if checkInputValid(self.ui.packAuthor, "strict") == "type":
            alert("Pack Author has unsupported characters!")
            return
        elif checkInputValid(self.ui.packAuthor, "strict") == "valid":
            self.packAuthor = self.ui.packAuthor.text()

        self.outputDir = QFileDialog.getExistingDirectory(self, "Output Directory", "")
        if not self.outputDir:
            alert("Please select a valid output directory!")
            return

    #######################
    # PACK GENERATION     #
    #######################

    def generateResourcePack(self):
        #######################
        # BASE STRUCTURE      #
        #######################

        self.resPackDirectory = os.path.join(
                self.outputDir, f"{self.packName} Resource Pack"
            )
        os.mkdir(self.resPackDirectory)
        os.mkdir(f"{self.resPackDirectory}/assets")

        if self.packVersion == "1.21.3":
            os.mkdir(f"{self.resPackDirectory}/assets/minecraft")
            os.mkdir(f"{self.resPackDirectory}/assets/minecraft/atlases")
            os.mkdir(f"{self.resPackDirectory}/assets/minecraft/models")
            os.mkdir(f"{self.resPackDirectory}/assets/minecraft/textures")
            os.mkdir(f"{self.resPackDirectory}/assets/minecraft/textures/item")
            os.mkdir(f"{self.resPackDirectory}/assets/minecraft/models/item")
            os.mkdir(
                f"{self.resPackDirectory}/assets/minecraft/models/{self.packNamespace}"
            )

            # Create Atlas
            with open(
                f"{self.resPackDirectory}/assets/minecraft/atlases/blocks.json", "w"
            ) as file:
                file.write(
                    f'{{"sources":[{{"type": "directory", "source": "{self.packNamespace}", "prefix": "{self.packNamespace}/"}}]}}'
                )
        
        else:
            os.mkdir(f"{self.resPackDirectory}/assets/{self.packNamespace}")
            os.mkdir(f"{self.resPackDirectory}/assets/{self.packNamespace}/items")
            os.mkdir(f"{self.resPackDirectory}/assets/{self.packNamespace}/models")
            os.mkdir(f"{self.resPackDirectory}/assets/{self.packNamespace}/models/item")
            os.mkdir(f"{self.resPackDirectory}/assets/{self.packNamespace}/textures")
            os.mkdir(f"{self.resPackDirectory}/assets/{self.packNamespace}/textures/item")
            os.mkdir(f"{self.resPackDirectory}/assets/{self.packNamespace}/textures/painting")

        # Pack.mcmeta
        with open(f"{self.resPackDirectory}/pack.mcmeta", "w") as pack:
            pack.write(
                f'{{\n    "pack": {{\n        "pack_format": {self.resourceFormat},\n        "description": "{self.packDescription}"\n    }}\n}}\n'
            )

        version = self.packVersion.replace(".", "_")

        if getattr(sys, 'frozen', False):
            internal = 'src.'
        else:
            internal = ''
        BlockResourcer = importlib.import_module(f"{internal}generation.v{version}.blocks").BlockResourcer
        ItemResourcer = importlib.import_module(f"{internal}generation.v{version}.items").ItemResourcer
        if self.packVersion != "1.21.3":
            PaintingResourcer = importlib.import_module(f"{internal}generation.v{version}.paintings").PaintingResourcer

        if len(self.blocks) > 0:
            blockResourcer = BlockResourcer(
                self.resPackDirectory, self.packNamespace, self.blocks
            )

            blockResourcer.generate()

        if len(self.items) > 0:
            itemResourcer = ItemResourcer(
                self.resPackDirectory,
                self.packNamespace,
                self.exists,
                self.data,
                self.items,
            )

            itemResourcer.generate()
        
        if len(self.paintings) > 0 and self.packVersion != "1.21.3":
            paintingResourcer = PaintingResourcer(
                self.resPackDirectory,
                self.packNamespace,
                self.paintings
            )

            paintingResourcer.generate()

    def generateDataPack(self):

        self.checkInputs()

        #######################
        # BASE STRUCTURE      #
        #######################

        self.packDirectory = os.path.join(self.outputDir, self.packName)
        os.mkdir(self.packDirectory)
        os.mkdir(f"{self.packDirectory}/data")
        self.namespaceDirectory = os.path.join(
            self.packDirectory, "data", self.packNamespace
        )
        self.minecraftDirectory = os.path.join(self.packDirectory, "data", "minecraft")
        os.mkdir(self.minecraftDirectory)
        os.mkdir(self.namespaceDirectory)

        with open(f"{self.packDirectory}/pack.mcmeta", "w") as pack:
            pack.write(
                f'{{\n    "pack": {{\n        "pack_format": {self.dataFormat},\n        "description": "'
                + self.packDescription
                + '"\n    }\n}\n'
            )

        os.mkdir(f"{self.namespaceDirectory}/function")
        if len(self.blocks) > 0 or len(self.items) > 0:
            os.mkdir(f"{self.namespaceDirectory}/advancement")
        if len(self.blocks) > 0:
            os.mkdir(f"{self.namespaceDirectory}/loot_table")
        if len(self.recipes) > 0:
            os.mkdir(f"{self.namespaceDirectory}/recipe")

        os.mkdir(f"{self.minecraftDirectory}/tags")
        os.mkdir(f"{self.minecraftDirectory}/tags/function")

        with open(f"{self.namespaceDirectory}/function/tick.mcfunction", "w") as tick:
            if len(self.blocks) > 0:
                tick.write(
                    f"{self.header}execute as @e[type=item_display,tag={self.packAuthor}.custom_block] at @s run function {self.packNamespace}:blocks/as_blocks"
                )
            else:
                tick.write(self.header)
        with open(f"{self.namespaceDirectory}/function/load.mcfunction", "w") as load:
            load.write(
                f'{self.header}tellraw @a {{"text":"[mDirt {self.appVersion}] - Successfully loaded pack!","color":"red"}}'
            )
        with open(f"{self.minecraftDirectory}/tags/function/tick.json", "w") as tick:
            tick.write(
                '{\n    "values":[\n        '
                + f'"{self.packNamespace}'
                + ':tick"\n        ]\n    }'
            )
        with open(f"{self.minecraftDirectory}/tags/function/load.json", "w") as load:
            load.write(
                '{\n    "values":[\n        '
                + f'"{self.packNamespace}'
                + ':load"\n        ]\n    }'
            )
        
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

        if len(self.blocks) > 0:
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

        if len(self.items) > 0:
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

        if len(self.recipes) > 0:
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

        if len(self.paintings) > 0 and self.packVersion != "1.21.3":
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
