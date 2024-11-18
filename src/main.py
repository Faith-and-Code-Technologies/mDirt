from ui import Ui_MainWindow
from select_item import Ui_Form
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QMessageBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import sys, os, json, datetime, re, shutil, ast

def alert(message):
    messageBox = QMessageBox()
    messageBox.setIcon(QMessageBox.Icon.Information)
    messageBox.setText(message)
    messageBox.setWindowTitle("Alert")
    messageBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    messageBox.exec()

def checkInputValid(input_, type_):
    return "empty" if not input_.text() else ("type" if type_ == "strict" and (not input_.text().islower() or any(
        char.isspace() or char.isdigit() for char in input_.text())) else ("valid" if type_ == "strict" else (
        "valid" if type_ == "string" and re.match(r'^[^<>:\"/\\|?*\x00-\x1F]+$',
                                                  input_.text()) and input_.text().strip() != "" else (
            "type" if type_ == "string" else (
                "valid" if type_ == "integer" and input_.text().isdigit() else "type")))))

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Make PyCharm stop yelling at me
        self.exists = None
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
        self.packCMDPrefix = None
        self.recipeProperties = None
        self.ui_form = None
        self.block_popup = None
        self.itemProperties = None
        self.blockProperties = None
        self.header = None
        self.recipe = None
        self.itemTexture = None
        self.blockTexture = None
        self.recipes = None
        self.items = None
        self.blocks = None
        self.data = None
        self.mainDirectory = None

        self.featureNum = 0

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup Needed Data
        self.setupData()

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

        # Import & Export
        self.ui.actionImport_mdrt.triggered.connect(self.importProject)
        self.ui.actionExport_mdrt.triggered.connect(self.exportProject)

        # Generate
        self.ui.packGenerate.clicked.connect(self.generateDataPack)

    def setupData(self):
        self.mainDirectory = f'{os.path.dirname(os.path.abspath(__file__))}\\..'
        self.data = json.load(open(f'{self.mainDirectory}\\lib\\data.json', 'r'))

        self.blocks = {}
        self.items = {}
        self.recipes = {}

        self.blockTexture = {}
        self.itemTexture = None
        self.recipe = {}

        self.header = """
        #####################################
        #   This File Was Created By mDirt  #
        #               v2.0.0              #
        #   Copyright 2024 by Jupiter Dev   #
        #####################################
        \n"""

    def parseCMD(self, num):
        if checkInputValid(self.ui.packCMDPrefix, "integer") == "empty": alert("Pack CMD Prefix is empty!"); return "error"
        if checkInputValid(self.ui.packCMDPrefix, "integer") == "type": alert("Pack CMD Prefix has unsupported characters!"); return "error"
        elif checkInputValid(self.ui.packCMDPrefix, "integer") == "valid": self.packCMDPrefix = self.ui.packCMDPrefix.text()

        strNum = str(num)
        numLen = len(strNum)
        zeros = 7 - len(self.packCMDPrefix) - numLen
        return f'{self.packCMDPrefix}{'0' * zeros}{strNum}'

    #######################
    # IMPORT & EXPORT     #
    #######################

    def exportProject(self, version="2.0.0"):
        data = {
            "file_type": "mDirtProjectData",
            "version": version,
            "metadata": {
                "exported_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z"
            },
            "content": {
                "pack_info": {
                    "packName": self.ui.packName.text(),
                    "packNamespace": self.ui.packNamespace.text(),
                    "author": self.ui.packAuthor.text(),
                    "cmdPrefix": self.ui.packCMDPrefix.text(),
                    "description": self.ui.packDescription.text(),
                    "version": self.ui.packVersion.currentText()
                },
                "elements": {
                    "blocks": self.blocks,
                    "items": self.items,
                    "recipes": self.recipes
                }
            }
        }
        file, _ = QFileDialog.getSaveFileName(self, "Save mDirt Project", "", "mDirt File (*.mdrt)")

        if file:
            with open(file, 'w') as f:
                json.dump(data, f, indent=4)

    def importProject(self, version="2.0.0"):
        file, _ = QFileDialog.getOpenFileName(self, "Open mDirt Project", "", "mDirt File (*.mdrt)")

        if file:
            with open(file, 'r') as f:
                data = json.load(f)
        else:
            alert("Please Select a Valid File!")
            return


        if data.get("file_type") != "mDirtProjectData":
            alert("Invalid File!")
            return

        if data.get("version") != version:
            alert(f"Incompatible version!")

        self.ui.packName.setText(data["content"]["pack_info"]["packName"])
        self.ui.packNamespace.setText(data["content"]["pack_info"]["packNamespace"])
        self.ui.packAuthor.setText(data["content"]["pack_info"]["author"])
        self.ui.packCMDPrefix.setText(data["content"]["pack_info"]["cmdPrefix"])
        self.ui.packDescription.setText(data["content"]["pack_info"]["description"])
        self.ui.packVersion.setCurrentText(data["content"]["pack_info"]["version"])
        self.blocks = data["content"]["elements"]["blocks"]
        self.items = data["content"]["elements"]["items"]
        self.recipes = data["content"]["elements"]["recipes"]

        for block in self.blocks: self.ui.blockList.addItem(self.blocks[block]["name"])
        for item in self.items: self.ui.itemList.addItem(self.items[item]["name"])
        for recipe in self.recipes: self.ui.recipeList.addItem(self.recipes[recipe]["name"])

    #######################
    # BLOCKS TAB          #
    #######################

    def getBlockModel(self):
        if self.ui.blockModel.currentText() == "Custom":
            fileDialog = QFileDialog()
            filePath, _ = fileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")

            if filePath: self.ui.blockModel.addItem(filePath); self.ui.blockModel.setCurrentText(filePath)

    def getBlockTexture(self, id_):
        textureId = id_
        self.blockTexture[textureId], _ = QFileDialog.getOpenFileName(self, "Open Texture File", "", "PNG Files (*.png)")
        if not self.blockTexture[textureId]: return
        image = QImage(self.blockTexture[textureId])
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        if textureId == 0: self.ui.blockTextureTop.setPixmap(pixmap)
        if textureId == 1: self.ui.blockTextureLeft.setPixmap(pixmap)
        if textureId == 2: self.ui.blockTextureBack.setPixmap(pixmap)
        if textureId == 3: self.ui.blockTextureRight.setPixmap(pixmap)
        if textureId == 4: self.ui.blockTextureFront.setPixmap(pixmap)
        if textureId == 5: self.ui.blockTextureBottom.setPixmap(pixmap)

    def addBlock(self):

        self.featureNum += 1

        self.blockProperties = {
            "name": self.ui.blockName.text(),
            "displayName": self.ui.blockDisplayName.text(),
            "baseBlock": self.ui.blockBaseBlock.text(),
            "textures": self.blockTexture,
            "placeSound": self.ui.blockPlaceSound.text(),
            "blockDrop": self.ui.blockDrop.text(),
            "directional": self.ui.blockDirectional.isChecked(),
            "model": self.ui.blockModel.currentText(),
            "cmd": self.parseCMD(self.featureNum)
        }

        self.blocks[self.blockProperties["name"]] = self.blockProperties

        self.ui.blockList.addItem(self.blockProperties["name"])

        self.clearBlockFields()

    def editBlock(self):
        if not self.ui.blockList.currentRow(): return
        curItem = self.ui.blockList.currentRow()
        curItem = self.ui.blockList.item(curItem).text()
        properties = self.blocks[curItem]

        self.ui.blockName.setText(properties["name"])
        self.ui.blockDisplayName.setText(properties["displayName"])
        self.ui.blockBaseBlock.setText(properties["baseBlock"])
        self.ui.blockDrop.setText(properties["blockDrop"])
        self.ui.blockPlaceSound.setText(properties["placeSound"])
        self.ui.blockDirectional.setChecked(properties["directional"])
        self.ui.blockModel.setCurrentText(properties["model"])
        self.blockTexture = properties["textures"]

        for textureId in self.blockTexture:
            image = QImage(self.blockTexture[textureId])
            pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

            if textureId == 0: self.ui.blockTextureTop.setPixmap(pixmap)
            if textureId == 1: self.ui.blockTextureLeft.setPixmap(pixmap)
            if textureId == 2: self.ui.blockTextureBack.setPixmap(pixmap)
            if textureId == 3: self.ui.blockTextureRight.setPixmap(pixmap)
            if textureId == 4: self.ui.blockTextureFront.setPixmap(pixmap)
            if textureId == 5: self.ui.blockTextureBottom.setPixmap(pixmap)

        self.removeBlock(self.ui.blockList.currentRow())

    def removeBlock(self, item=None):
        curItem = item
        if not item:
            curItem = self.ui.blockList.currentRow()
            if not self.ui.blockList.currentRow(): return

        self.blocks.pop(self.ui.blockList.item(curItem).text())
        self.ui.blockList.takeItem(curItem)

    def clearBlockFields(self):
        self.ui.blockName.setText("")
        self.ui.blockDisplayName.setText("")
        self.ui.blockBaseBlock.setText("")
        self.ui.blockDrop.setText("")
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

    def getItemModel(self):
        if self.ui.itemModel.currentText() == "Custom":
            fileDialog = QFileDialog()
            filePath, _ = fileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")

            if filePath: self.ui.itemModel.addItem(filePath); self.ui.itemModel.setCurrentText(filePath)

    def getItemTexture(self):
        self.itemTexture, _ = QFileDialog.getOpenFileName(self, "Open Texture File", "","PNG Files (*.png)")
        if not self.itemTexture: return
        image = QImage(self.itemTexture)
        pixmap = QPixmap.fromImage(image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        self.ui.itemTexture.setPixmap(pixmap)

    def addItem(self):

        self.featureNum += 1

        self.itemProperties = {
            "name": self.ui.itemName.text(),
            "displayName": self.ui.itemDisplayName.text(),
            "baseItem": self.ui.itemBaseItem.text(),
            "texture": self.itemTexture,
            "model": self.ui.itemModel.currentText().lower(),
            "cmd": self.parseCMD(self.featureNum)
        }

        self.items[self.itemProperties["name"]] = self.itemProperties
        self.ui.itemList.addItem(self.itemProperties["name"])
        self.clearItemFields()

    def editItem(self):
        if not self.ui.itemList.currentRow(): return
        curItem = self.ui.itemList.currentItem()
        curItem = self.ui.itemList.item(curItem).text()
        properties = self.items[curItem]

        self.ui.itemName.setText(properties["name"])
        self.ui.itemDisplayName.setText(properties["displayName"])
        self.ui.itemBaseItem.setText(properties["baseItem"])
        self.ui.itemModel.setCurrentText(properties["model"])

        self.itemTexture = properties["texture"]

        pixmap = QPixmap.fromImage(QImage(properties["texture"])).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.itemTexture.setPixmap(pixmap)

        self.removeItem(self.ui.itemList.currentRow())

    def removeItem(self, item=None):
        curItem = item
        if not item:
            curItem = self.ui.itemList.currentRow()
            if not self.ui.itemList.currentRow(): return

        self.items.pop(self.ui.itemList.item(curItem).text())
        self.ui.itemList.takeItem(curItem)

    def clearItemFields(self):
        self.ui.itemName.setText("")
        self.ui.itemDisplayName.setText("")
        self.ui.itemBaseItem.setText("")
        self.ui.itemModel.setCurrentText("Generated")

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

        if slotId == 9 or slotId == 11:
            for block in self.blocks:
                self.ui_form.itemsBox.addItem(f'{self.blocks[block]["name"]}')
            for item in self.items:
                self.ui_form.itemsBox.addItem(f'{self.items[item]["name"]}')

        for item in item_list:
            self.ui_form.itemsBox.addItem(item)

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

        self.block_popup.close()

    def addRecipe(self):
        self.recipeProperties = {
            "name": self.ui.recipeName.text(),
            "items": self.recipe,
            "outputCount": self.ui.slot9Count.value(),
            "exact": self.ui.exactlyRadio.isChecked(),
            "shapeless": self.ui.exactlyRadio.isChecked(),
            "type": self.ui.recipeSubTabs.tabText(self.ui.recipeSubTabs.currentIndex()).lower() # Should result as "crafting" or "smelting"
        }

        self.recipes[self.recipeProperties["name"]] = self.recipeProperties
        self.ui.recipeList.addItem(self.recipeProperties["name"])
        self.clearRecipeFields()

    def editRecipe(self):
        if not self.ui.recipeList.currentRow(): return
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
            curItem = self.ui.itemList.currentRow()
            if not self.ui.itemList.currentRow(): return

        self.recipes.pop(self.ui.recipeList.item(curItem).text())
        self.ui.recipeList.takeItem(curItem)

    def clearRecipeFields(self):
        self.recipe = None
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

    #######################
    # PACK GENERATION     #
    #######################

    def generateResourcePack(self):
        #######################
        # BASE STRUCTURE      #
        #######################

        self.resPackDirectory = os.path.join(self.outputDir, f'{self.packName} Resource Pack')
        os.mkdir(self.resPackDirectory)
        os.mkdir(f'{self.resPackDirectory}\\assets')
        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft')
        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft\\atlases')
        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft\\models')
        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft\\textures')
        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft\\textures\\item')
        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft\\models\\item')
        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft\\models\\{self.packNamespace}')

        # Create Atlas
        with open(f'{self.resPackDirectory}\\assets\\minecraft\\atlases\\blocks.json', 'w') as file:
            file.write(f'{{"sources":[{{"type": "directory", "source": "{self.packNamespace}", "prefix": "{self.packNamespace}/"}}]}}')

        # Pack.mcmeta
        with open(f'{self.resPackDirectory}\\pack.mcmeta', 'w') as pack:
            pack.write(f'{{\n    "pack": {{\n        "pack_format": 42,\n        "description": "{self.packDescription}"\n    }}\n}}\n')

        # Item Frame Model(s) For Blocks
        with open(f'{self.resPackDirectory}\\assets\\minecraft\\models\\item\\item_frame.json', 'a') as file:
            file.write('{"parent": "minecraft:item/generated","textures": {"layer0": "minecraft:item/item_frame"},"overrides":[')
            for block in self.blocks:
                file.write(f'{{ "predicate": {{ "custom_model_data": {self.blocks[block]["cmd"]}}}, "model": "{self.packNamespace}/{self.blocks[block]["name"]}"}}')
                if block != next(reversed(self.blocks.keys())):
                    file.write(',')
            file.write('}}')

        # Copy Block Textures To Pack
        for block in self.blocks:
            texturePath = f'{self.resPackDirectory}\\assets\\minecraft\\textures\\item\\'

            if '.json' not in self.blocks[block]["model"]:
                for path in self.blocks[block]["textures"].values():
                    if not os.path.exists(os.path.join(texturePath, os.path.splitext(os.path.basename(str(path)))[ -2] + ".png")):
                        shutil.copy(path, os.path.join(texturePath,os.path.splitext(os.path.basename(str(path)))[-2] + ".png"))
            else:
                path = self.blocks[block]["textures"][5]
                if not os.path.exists(os.path.join(texturePath, os.path.splitext(os.path.basename(str(path)))[-2] + ".png")):
                    shutil.copy(path, os.path.join(texturePath, os.path.splitext(os.path.basename(str(path)))[ -2] + ".png"))

        # Copy / Write Block Model To Pack
        for block in self.blocks:
            with open(f'{self.resPackDirectory}\\assets\\minecraft\\models\\{self.packNamespace}\\{self.blocks[block]["name"]}.json', 'w') as file:
                if '.json' not in self.blocks[block]["model"]:
                    file.write(f'{{"credit": "Made with mDirt 2","textures": {{"0": "item/{self.blocks[block]["textures"][0]}","1": "item/{self.blocks[block]["textures"][1]}","2": "item/{self.blocks[block]["textures"][2]}","3": "item/{self.blocks[block]["textures"][3]}","4": "item/{self.blocks[block]["textures"][4]}","5": "item/{self.blocks[block]["textures"][5]}","particle": "item/{self.blocks[block]["textures"][0]}"}},"elements": [{{"from": [0, 0, 0],"to": [16, 16, 16],"faces": {{"north": {{"uv": [0, 0, 16, 16], "texture": "#0"}},"east": {{"uv": [0, 0, 16, 16], "texture": "#1"}},"south": {{"uv": [0, 0, 16, 16], "texture": "#2"}},"west": {{"uv": [0, 0, 16, 16], "texture": "#3"}},"up": {{"uv": [0, 0, 16, 16], "texture": "#4"}},"down": {{"uv": [0, 0, 16, 16], "texture": "#5"}}}}}}],"display": {{"thirdperson_righthand": {{"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]}},"thirdperson_lefthand": {{"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]}},"firstperson_righthand": {{"rotation": [0, 45, 0],"scale": [0.4, 0.4, 0.4]}},"ground": {{"translation": [0, 3.25, 0],"scale": [0.4, 0.4, 0.4]}},"gui": {{"rotation": [28, 45, 0],"scale": [0.6, 0.6, 0.6]}}}}}}')
                else:
                    with open(self.blocks[block]["model"], 'r') as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][texture] = f'item/{model["textures"][texture]}'
                    file.write(str(model).replace("'", '"'))

        # Write Base Item Model To Pack
        for item in self.items:
            modelPath = f'{self.resPackDirectory}\\assets\\minecraft\\models\\item\\'
            if not os.path.exists(f'{modelPath}{self.items[item]["baseItem"].removeprefix("minecraft:")}.json'):
                self.exists[self.items[item]["baseItem"]] = False
            with open(f'{modelPath}{self.items[item]["baseItem"].removeprefix("minecraft:")}.json', 'a') as file:
                if not self.exists[self.items[item]["baseItem"]]:
                    self.exists[self.items[item]["baseItem"]] = True
                    modelType = self.data["models"][self.items[item]["baseItem"]]
                    file.write(f'{modelType}, "overrides": [')
                file.write(f'{{ "predicate": {{ "custom_model_data": {self.items[item]["cmd"]}}}, "model": "{self.packNamespace}/{self.items[item]["name"]}"}},')

        # Remove Trailing Comma At Each Model
        for file in os.listdir(f'{self.resPackDirectory}\\assets\\minecraft\\models\\item'):
            if file.endswith('.json'):
                with open(os.path.join(f'{self.resPackDirectory}\\assets\\minecraft\\models\\item\\', file), 'r+') as f:
                    content = f.read(); f.seek(0); f.write(content[:-1]);  f.truncate(); f.write(']}')

        # Copy / Write Item Model To Pack
        for item in self.items:
            currentPath = f'{self.resPackDirectory}\\assets\\minecraft\\models\\{self.packNamespace}'
            with open(f'{currentPath}\\{self.items[item]["name"]}.json', 'w') as file:
                if '.json' in self.items[item]["model"]:
                    with open(self.items[item]["model"], 'r') as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][texture] = f'{self.packNamespace}/{model["textures"][texture]}'
                    file.write(str(model).replace("'", '"'))
                else:
                    file.write(f'{{"parent":" {self.data["models"][self.items[item]["baseItem"]]["parent"]}", "textures": {{ "layer0": "minecraft:{self.packNamespace}/{os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]}"}}}}')

        os.mkdir(f'{self.resPackDirectory}\\assets\\minecraft\\textures\\{self.packNamespace}')

        # Copy Item Texture To Pack
        for item in self.items:
            currentPath = f'{self.resPackDirectory}\\assets\\minecraft\\textures\\{self.packNamespace}'
            shutil.copy(self.items[item]["texture"], os.path.normpath(f'{currentPath}\\{os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]}.png'))

    def generateDataPack(self):

        #######################
        # ERROR CHECKING      #
        #######################

        self.default_blocks = self.data["blocks"]
        self.default_items = self.data["items"]

        for block in self.blocks:
            if self.blocks[block]["baseBlock"] not in self.default_blocks.keys(): alert(f"Block '{self.blocks[block]["name"]}' has an unsupported Base Block!"); return

        for item in self.items:
            if self.items[item]["baseItem"] not in self.default_items.keys(): alert(f"Item '{self.items[item]["name"]}' has an unsupported Base Item!"); return

        if checkInputValid(self.ui.packName, "string") == "empty": alert("Pack Name is empty!"); return
        if checkInputValid(self.ui.packName, "string") == "type": alert("Pack Name has unsupported characters!"); return
        elif checkInputValid(self.ui.packName, "string") == "valid": self.packName = self.ui.packName.text()

        if checkInputValid(self.ui.packNamespace, "strict") == "empty": alert("Pack Namespace is empty!"); return
        if checkInputValid(self.ui.packNamespace, "strict") == "type": alert("Pack Namespace has unsupported characters!"); return
        elif checkInputValid(self.ui.packNamespace, "strict") == "valid": self.packNamespace = self.ui.packNamespace.text()

        if checkInputValid(self.ui.packDescription, "string") == "empty": alert("Pack Description is empty!"); return
        if checkInputValid(self.ui.packDescription, "string") == "type": alert("Pack Description has unsupported characters!"); return
        elif checkInputValid(self.ui.packDescription, "string") == "valid": self.packDescription = self.ui.packDescription.text()

        if checkInputValid(self.ui.packAuthor, "strict") == "empty": alert("Pack Author is empty!"); return
        if checkInputValid(self.ui.packAuthor, "strict") == "type": alert("Pack Author has unsupported characters!"); return
        elif checkInputValid(self.ui.packAuthor, "strict") == "valid": self.packAuthor = self.ui.packAuthor.text()

        if checkInputValid(self.ui.packCMDPrefix, "integer") == "empty": alert("Pack CMD Prefix is empty!"); return
        if checkInputValid(self.ui.packCMDPrefix, "integer") == "type": alert("Pack CMD Prefix has unsupported characters!"); return
        elif checkInputValid(self.ui.packCMDPrefix, "integer") == "valid": self.packCMDPrefix = self.ui.packCMDPrefix.text()

        self.outputDir = QFileDialog.getExistingDirectory(self, "Output Directory", "")
        if not self.outputDir: alert("Please select a valid output directory!"); return

        #######################
        # BASE STRUCTURE      #
        #######################

        self.packDirectory = os.path.join(self.outputDir, self.packName)
        os.mkdir(self.packDirectory)
        os.mkdir(f'{self.packDirectory}\\data')
        self.namespaceDirectory = os.path.join(self.packDirectory, 'data', self.packNamespace)
        self.minecraftDirectory = os.path.join(self.packDirectory, "data", "minecraft")
        os.mkdir(self.minecraftDirectory)
        os.mkdir(self.namespaceDirectory)

        with open(f'{self.packDirectory}\\pack.mcmeta', 'w') as pack:
            pack.write('{\n    "pack": {\n        "pack_format": 57,\n        "description": "' + self.packDescription + '"\n    }\n}\n')

        os.mkdir(f'{self.namespaceDirectory}\\function')
        if len(self.blocks) > 0:
            os.mkdir(f'{self.namespaceDirectory}\\loot_table')
            os.mkdir(f'{self.namespaceDirectory}\\advancement')
        if len(self.recipes) > 0:
            os.mkdir(f'{self.namespaceDirectory}\\recipe')

        os.mkdir(f'{self.minecraftDirectory}\\tags')
        os.mkdir(f'{self.minecraftDirectory}\\tags\\function')

        with open(f'{self.namespaceDirectory}\\function\\tick.mcfunction', 'w') as tick:
            if len(self.blocks) > 0:
                tick.write(f'{self.header}execute as @e[type=item_display,tag={self.packAuthor}.custom_block] at @s run function {self.packNamespace}:as_blocks')
            else: tick.write(self.header)
        with open(f'{self.namespaceDirectory}\\function\\load.mcfunction', 'w') as load:
            load.write(f'{self.header}tellraw @a {"text":"[mDirt 2] - Successfully loaded pack!","color":"red"}')
        with open(f'{self.minecraftDirectory}\\tags\\function\\tick.json', 'w') as tick:
            tick.write('{\n    "values":[\n        ' + f'"{self.packNamespace}' + ':tick"\n        ]\n    }')
        with open(f'{self.minecraftDirectory}\\tags\\function\\load.json', 'w') as load:
            load.write('{\n    "values":[\n        ' + f'"{self.packNamespace}' + ':load"\n        ]\n    }')

        #######################
        # CUSTOM BLOCKS       #
        #######################

        if len(self.blocks) > 0:
            self.generateBlocks()

        #######################
        # CUSTOM ITEMS        #
        #######################

        if len(self.items) > 0:
            self.generateItems()

        #######################
        # CUSTOM RECIPES      #
        #######################

        if len(self.recipes) > 0:
            self.generateRecipes()

        #######################
        # RESOURCE PACK       #
        #######################

        self.generateResourcePack()

    def generateBlocks(self):
        os.mkdir(f'{self.namespaceDirectory}\\function\\blocks')

        # Placed Item Frame Advancement
        with open(f'{self.namespaceDirectory}\\advancement\\placed_item_frame.json', 'w') as file:
            file.write(f'{{"criteria": {{"requirement": {{"trigger": "minecraft:item_used_on_block","conditions": {{"location": [{{"condition": "minecraft:match_tool","predicate": {{"items": ["minecraft:item_frame"]}}}}]}}}}}}, "rewards": {{"function": "{self.packNamespace}:placed_item_frame"}}}}')

        # Placed Item Frame Function
        with open(f'{self.namespaceDirectory}\\function\\blocks\\placed_item_frame.mcfunction', 'w') as file:
            file.write(f"{self.header}advancement revoke @s only {self.packNamespace}:placed_item_frame\n"
                       f"execute as @e[tag={self.packAuthor}.item_frame_block,distance=..10] at @s run function {self.packNamespace}:check_placed_item_frame")

        # Check Placed Item Frame, block/place Functions
        with open(f'{self.packNamespace}\\function\\blocks\\check_placed_item_frame', 'a') as file:
            for block in self.blocks:
                os.mkdir(f'{self.namespaceDirectory}\\function\\blocks\\{self.blocks[block]["name"]}')
                with open(f'{self.namespaceDirectory}\\function\\{self.blocks[block]["name"]}\\place.mcfunction', 'a') as file2:
                    file2.write(f'{self.header}setblock ~ ~ ~ {self.blocks[block]["baseBlock"]} keep\n')
                    if self.blocks[block]["placeSound"] != "": file2.write(f'playsound {self.blocks[block]["placeSound"]} block @e[type=player,distance=..5] ~ ~ ~ 10 1 1\n')
                    if self.blocks[block]["directional"]:
                        file2.write(f'execute at @p if entity @p[y_rotation=135..-135,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~-0.469 {{Rotation:[0F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n')
                        file2.write(f'execute at @p if entity @p[y_rotation=-135..-45,x_rotation=-45..45] at @s run summon item_display ~0.469 ~0.469 ~ {{Rotation:[90F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n')
                        file2.write(f'execute at @p if entity @p[y_rotation=-45..45,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~0.469 {{Rotation:[180F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n')
                        file2.write(f'execute at @p if entity @p[y_rotation=45..135,x_rotation=-45..45] at @s run summon item_display ~-0.469 ~0.469 ~ {{Rotation:[90F,-90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n')
                        file2.write(f'execute if entity @p[x_rotation=45..90] at @s run summon item_display ~ ~ ~ {{brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n')
                        file2.write(f'execute if entity @p[x_rotation=-90..-45] at @s run summon item_display ~ ~0.469 ~-0.47 {{Rotation:[0F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,-1f,1f,1f],right_rotation:[1.000f,0.5f,0.5f,0f],translation:[0f,0.47f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n')
                    else:
                        file2.write(f'summon item_display ~ ~ ~ {{brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n')
                file.write(f"{self.header}execute as @s[tag={self.packAuthor}.{self.blocks[block]['name']}] run function {self.packNamespace}:blocks/{self.blocks[block]['name']}/place\n")
            file.write('kill @s')

        # As Blocks, block/block, block/break Functions
        with open(f'{self.namespaceDirectory}\\function\\blocks\\as_blocks.mcfunction', 'a') as file:
            file.write(self.header)
            for block in self.blocks:
                with open(f'{self.namespaceDirectory}\\function\\blocks\\{block}\\{block}.mcfunction', 'w') as file2:
                    file2.write(f'{self.header}execute unless block ~ ~ ~ {self.blocks[block]["baseBlock"]} run function {self.packNamespace}:blocks/{self.blocks[block]["name"]}/break')
                with open(f'{self.namespaceDirectory}\\function\\blocks\\{block}\\break.mcfunction', 'a') as file2:
                    file2.write(f'{self.header}execute as @e[type=item,sort=nearest,limit=1,distance=..2,nbt={{OnGround:0b,Age:0s,Item:{{id:"{self.blocks[block]["baseBlock"]}"}}}}] run kill @s\n'
                                f'loot spawn ~ ~ ~ loot {self.packNamespace}:{self.blocks[block]["name"]}\n'
                                f'kill @s')

                file.write(f'execute as @s[tag={self.packAuthor}.{self.blocks[block]["name"]}] run function {self.packNamespace}:blocks/{self.blocks[block]["name"]}/{self.blocks[block]["name"]}\n')

        # Give Blocks Function
        with open(f'{self.namespaceDirectory}\\function\\give_blocks.mcfunction', 'a') as file:
            file.write(self.header)
            for block in self.blocks:
                file.write(f'give @s item_frame[item_name=\'{{"italic":false,"text":"{self.blocks[block]["displayName"]}}}\',custom_model_data={self.blocks[block]["cmd"]},entity_data={{id:"minecraft:item_frame",Fixed:1b,Invisible:1b,Silent:1b,Invulnerable:1b,Facing:1,Tags:["{self.packAuthor}.item_frame_block","{self.packAuthor}.{self.blocks[block]["name"]}"]}}] 1\n')

        # Loot Tables
        for block in self.blocks:
            with open(f'{self.namespaceDirectory}\\loot_table\\{self.blocks[block]["name"]}.json', 'w') as file:
                if self.blocks[block]["blockDrop"] == "":
                    file.write(f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "minecraft:item_frame"}}],"functions": [{{"function": "minecraft:set_components","components": {{"minecraft:custom_model_data": {self.blocks[block]["cmd"]},"minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{self.blocks[block]["displayName"]}\\"}}","minecraft:entity_data": {{"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{self.blocks[block]["name"]}"]}}}}}}]}}]}}')
                else:
                    file.write(f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "{self.blocks[block]["blockDrop"]}"}}]}}]}}')

    def generateItems(self):
        with open(f'{self.packNamespace}\\function\\give_items.mcfunction', 'a') as file:
            file.write(self.header)
            for item in self.items:
                file.write(f'give @s {self.items[item]["baseItem"]}[item_name=\'{{"italic":false,"text":"{self.items[item]["displayName"]}"}}\',custom_model_data={self.items[item]["cmd"]}] 1\n')

    def generateRecipes(self):
        for recipe in self.recipes:
            if self.recipes[recipe]["type"] == "crafting":
                if not self.recipes[recipe]["shapeless"]:
                    with open(f'{self.namespaceDirectory}\\recipe\\{self.recipes[recipe]["name"]}.json', 'a') as file:
                        letters = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I"}
                        recip = self.recipes[recipe]["items"]
                        file.write('{"type": "minecraft:crafting_shaped", "pattern": ["')
                        result = []

                        for key in range(9):
                            value = recip.get(key)
                            if value:
                                result.append(letters[key])
                            else:
                                result.append(" ")
                        for i in range(0, len(result), 2):
                            if i < len(result) - 2:
                                line = f'["{result[i]} {result[i + 1]}"],\n'
                            else:
                                line = f'["{result[i]} {result[i + 1]}"]\n'
                            file.write(line)

                        file.write('"],"key":{')
                        items = [(k, v) for k, v in recip.items() if v not in (None, '')][:-1]
                        for i, (key, value) in enumerate(items):
                            if value != "" and value:
                                file.write(f'"{letters[key]}":"minecraft:{value}"')
                                if i < len(items) - 1: file.write(',')
                        if not recip[9] in self.items and not recip[9] in self.blocks:
                            file.write(f'}},"result": {{ "id":"minecraft:{recip[9]}", "count":{self.recipes[recipe]["outputCount"]}}}}}')
                        elif recip[9] in self.items:
                            idx = self.items[recip[9]]
                            file.write(f'}},"result":{{ "id":"{idx["baseItem"]}", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_name":"{{\"italic\":false,\"text\":\"{idx["displayName"]}\"}}", "minecraft:custom_model_data": {idx["name"]} }} }} }}')
                        elif recip[9] in self.blocks:
                            idx = self.blocks[recip[9]]
                            file.write(f'}},"result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:custom_model_data": {idx["cmd"]}, "minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{idx["displayName"]}\\"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}')

                else:
                    with open(f'{self.namespaceDirectory}\\recipe\\{self.recipes[recipe]["name"]}.json', 'a') as file:
                        recip = self.recipes[recipe]["items"]
                        items = [(k, v) for k, v in recip.items() if v not in (None, '')][:-3]
                        for ingredient, (key, value) in enumerate(items):
                            if value:
                                file.write(f'"minecraft:{value}"')
                                if ingredient < len(items) - 1: file.write(',')
                        if not recip[9] in self.items and not recip[9] in self.blocks:
                            file.write(
                                f']],"result":{{"id": "minecraft:{recip[9]}", "count":{self.recipes[recipe]["outputCount"]}}}}}')
                        elif recip[9] in self.items:
                            idx = self.items[recip[9]]
                            file.write(
                                f'}},"result":{{ "id":"{idx["baseItem"]}", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_name":"{{\\"italic\\":false,\\"text\\":\\"{idx["displayName"]}\\"}}", "minecraft:custom_model_data": {idx["cmd"]}}} }} }}')
                        elif recip[9] in self.blocks:
                            idx = self.blocks[recip[9]]
                            file.write(
                                f'}},"result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:custom_model_data": {idx["cmd"]}, "minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{idx["displayName"]}\\"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}')

            elif self.recipes[recipe]["type"] == "smelting":
                with open(f'{self.namespaceDirectory}\\recipe\\{self.recipes[recipe]["name"]}.json', 'a') as file:
                    recip = self.recipes[recipe]["items"]
                    if not recip[11] in self.items and not recip[11] in self.blocks:
                        file.write(f'{{ "type": "minecraft:smelting", "ingredient": "minecraft:{recipe[10]}", "result": {{ "id": "minecraft:{recip[11]}"}} }}')
                    elif recip[11] in self.items:
                        idx = self.items[recip[11]]
                        file.write(
                            f'{{ "type": "minecraft:smelting", "ingredient": "minecraft:{recip[10]}", "result": {{ "id": "minecraft:{recip[11]}", "components": {{"minecraft:item_name":"{{\\"italic\\":false,\\"text\\":\\"{idx["displayName"]}\\"}}", "minecraft:custom_model_data": {idx["cmd"]} }}}}')
                    elif recip[11] in self.blocks:
                        idx = self.blocks[recip[11]]
                        file.write(
                            f'}},"result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["count"]}, "components": {{ "minecraft:custom_model_data": {idx["cmd"]}, "minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{idx["displayName"]}\\"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.setStyle("Fusion")
    sys.exit(app.exec())