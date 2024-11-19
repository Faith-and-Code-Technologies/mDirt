import json.tool, os, sys, shutil, json, ast
from ui import Ui_MainWindow
from item_select import Ui_Form
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class app:
    def __init__(self):
        super(app, self).__init__()
        
        self.blocks = {}
        self.items = {}
        self.recipes = {}

        self.generated_cmds = {
            "items": {}, 
            "blocks": {}
            }

        self.recipe = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": ""}
        self.texture = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}
        self.blockNum = 0

        self.header = '#####################################\n#   This File Was Created By mDirt  #\n#              v1.10.0              #\n#   Copyright 2024 by Jupiter Dev   #\n#####################################\n'

        self.app = QApplication(sys.argv)
        self.mainwindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainwindow)
        self.mainwindow.setStyleSheet(open("themes/dark.qss", "r").read())
        self.mainwindow.show()

        self.ui.actionImport_from_mrdt.triggered.connect(self.imported)
        self.ui.actionExport_to_mrdt_2.triggered.connect(self.export)

        self.ui.itemModel.activated.connect(self.getItemModel)
        self.ui.blockModel.activated.connect(self.getBlockModel)

        self.checkBlockAdd()
        self.checkBlockRemove()
        self.checkBlockEdit()
        self.checkItemAdd()
        self.checkItemRemove()
        self.checkItemEdit()
        self.checkRecipeAdd()
        self.checkRecipeRemove()
        self.checkRecipeEdit()
        self.checkGenerate()
        self.checkBlockTextures()
        self.checkItemTexture()
        self.checkRecipeButtons()
        self.checkThemeActions()

        self.app.exec()
    
    def checkThemeActions(self):
        self.ui.actionBlue.triggered.connect(lambda: self.switchTheme("blue"))
        self.ui.actionRed.triggered.connect(lambda: self.switchTheme("red"))
        self.ui.actionGreen.triggered.connect(lambda: self.switchTheme("green"))
        self.ui.actionPurple.triggered.connect(lambda: self.switchTheme("purple"))
        self.ui.actionDark_default.triggered.connect(lambda: self.switchTheme("dark"))
        self.ui.actionLight.triggered.connect(lambda: self.switchTheme("light"))
    
    def switchTheme(self, theme):
        self.mainwindow.setStyleSheet(open(f"themes/{theme}.qss", "r").read())
    
    def checkRecipeButtons(self):
        self.ui.slot0.clicked.connect(lambda: self.recipeSlot(0))
        self.ui.slot1.clicked.connect(lambda: self.recipeSlot(1))
        self.ui.slot2.clicked.connect(lambda: self.recipeSlot(2))
        self.ui.slot3.clicked.connect(lambda: self.recipeSlot(3))
        self.ui.slot4.clicked.connect(lambda: self.recipeSlot(4))
        self.ui.slot5.clicked.connect(lambda: self.recipeSlot(5))
        self.ui.slot6.clicked.connect(lambda: self.recipeSlot(6))
        self.ui.slot7.clicked.connect(lambda: self.recipeSlot(7))
        self.ui.slot8.clicked.connect(lambda: self.recipeSlot(8))
        self.ui.slot9.clicked.connect(lambda: self.recipeSlot(9))
                                                                                                          
        self.ui.input.clicked.connect(lambda: self.recipeSlot(10))
        self.ui.output.clicked.connect(lambda: self.recipeSlot(11))
    
    def recipeSlot(self, id):
        self.block_popup = QWidget()
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self.block_popup)

        with open(f'{os.path.dirname(os.path.abspath(__file__)) + '\\data.json'}', 'r') as f:
            item_list = json.load(f)["items"]

        if id == 9 or id == 11:
            for block in self.blocks:
                self.ui_form.comboBox.addItem(f'{self.blocks[block]["name"]}')
            for item in self.items:
                self.ui_form.comboBox.addItem(f'{self.items[item]["name"]}')
        
        for item in item_list:
            self.ui_form.comboBox.addItem(item)

        self.block_popup.show()

        self.ui_form.pushButton.clicked.connect(lambda: self.itemFormClosed(id, self.ui_form.comboBox.currentText()))
        
    def itemFormClosed(self, id, item):
        self.recipe[str(id)] = item
        if id == 0:
            self.ui.slot0Label.setText(item)
        elif id == 1:
            self.ui.slot1Label.setText(item)
        elif id == 2:
            self.ui.slot2Label.setText(item)
        elif id == 3:
            self.ui.slot3Label.setText(item)
        elif id == 4:
            self.ui.slot4Label.setText(item)
        elif id == 5:
            self.ui.slot5Label.setText(item)
        elif id == 6:
            self.ui.slot6Label.setText(item)
        elif id == 7:
            self.ui.slot7Label.setText(item)
        elif id == 8:
            self.ui.slot8Label.setText(item)
        elif id == 9:
            self.ui.slot9Label.setText(item)
        elif id == 10:
            self.ui.inputLabel.setText(item)
        elif id == 11:
            self.ui.outputLabel.setText(item)
        self.block_popup.close()

    def getBlockModel(self):
        if self.ui.blockModel.currentText() == "Custom":
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self.mainwindow, "Open JSON File", "", "JSON Files (*.json)")

            if file_path:
                self.ui.blockModel.addItem(file_path)
                self.ui.blockModel.setCurrentText(file_path)

    def getItemModel(self):
        if self.ui.itemModel.currentText() == "Custom":
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self.mainwindow, "Open JSON File", "", "JSON Files (*.json)")

            if file_path:
                self.ui.itemModel.addItem(file_path)
                self.ui.itemModel.setCurrentText(file_path)

    def imported(self):
        self.iFile = QFileDialog.getOpenFileName(self.mainwindow, "Open mDirt File", "", "mDirt File (*.mdrt)")
        
        if self.iFile[0] != "":
            with open(self.iFile[0], 'r') as file:
                self.packProperties = json.load(file)
                self.ui.packName.setText(self.packProperties["packName"])
                self.ui.packNamespace.setText(self.packProperties["packNamespace"])
                self.ui.packDescription.setText(self.packProperties["packDescription"])
                self.ui.packVersion.setCurrentText(self.packProperties["packVersion"])
                self.ui.author.setText(self.packProperties["packAuthor"])
                self.blocks = self.packProperties["blcks"]
                self.items = self.packProperties["itms"]
                self.recipes = self.packProperties["recip"]
                for block in self.blocks:
                    self.ui.blockList.addItem(self.blocks[block]["name"])
                for item in self.items:
                    self.ui.itemList.addItem(self.items[item]["name"])
                for recipe in self.recipes:
                    self.ui.recipeList.addItem(self.recipes[recipe]["name"])
        else:
            self.setStatus("Please select a valid mDirt file!")

    def export(self):
        self.eFile = QFileDialog.getSaveFileName(self.mainwindow, "Save mDirt File", "", "mDirt File (*.mdrt)")
        
        if self.eFile[0] != "":
            self.packProperties = {
                "packName": self.ui.packName.text(),
                "packNamespace": self.ui.packNamespace.text(),
                "packDescription": self.ui.packDescription.text(),
                "packVersion": self.ui.packVersion.currentText(),
                "packAuthor": self.ui.author.text(),
                "blcks": self.blocks,
                "itms": self.items,
                "recip": self.recipes
            }
            with open(self.eFile[0], 'w') as eFile:
                eFile[0].write(str(self.packProperties).replace("'", '"'))
            eFile[0]
        else:
            self.setStatus("Please save to a proper location!")

    def setStatus(self, stat):
        self.stat = stat
        self.ui.status.setEnabled(True)
        self.ui.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.status.setText(self.stat)

    def checkItemTexture(self):
        self.ui.itemTextureButton.clicked.connect(self.getItemTexture)

    def checkBlockTextures(self):
        self.ui.topFaceBtn.clicked.connect(lambda: self.getBlockTexture("4"))
        self.ui.bottomFaceBtn.clicked.connect(lambda: self.getBlockTexture("5"))
        self.ui.rightFaceBtn.clicked.connect(lambda: self.getBlockTexture("1"))
        self.ui.leftFaceBtn.clicked.connect(lambda: self.getBlockTexture("3"))
        self.ui.frontFaceBtn.clicked.connect(lambda: self.getBlockTexture("2"))
        self.ui.backFaceBtn.clicked.connect(lambda: self.getBlockTexture("0"))

    def getItemTexture(self):
        self.itemTexture = QFileDialog.getOpenFileName(self.mainwindow, "Open Texture File", "", "PNG Files (*.png)")[0]
        self.image = QImage(self.itemTexture)
        self.pixmap = QPixmap.fromImage(self.image).scaled(41, 41, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.itemTextureLabel.setPixmap(self.pixmap)

    def getBlockTexture(self, id):
        self.id = id
        self.texture[self.id] = QFileDialog.getOpenFileName(self.mainwindow, "Open Texture File", "", "PNG Files (*.png)")[0]
        self.image = QImage(self.texture[self.id])

        if self.texture[self.id] != "":
            self.pixmap = QPixmap.fromImage(self.image).scaled(41, 41, Qt.AspectRatioMode.KeepAspectRatio)
            if self.id == "0":
                self.ui.backFace.setPixmap(self.pixmap)
            elif self.id == "1":
                self.ui.rightFace.setPixmap(self.pixmap)
            elif self.id == "2":
                self.ui.frontFace.setPixmap(self.pixmap)
            elif self.id == "3":
                self.ui.leftFace.setPixmap(self.pixmap)
            elif self.id == "4":
                self.ui.topFace.setPixmap(self.pixmap)
            elif self.id == "5":
                self.ui.bottomFace.setPixmap(self.pixmap)
        else:
            self.setStatus("Please select a valid Texture!")

    def checkBlockAdd(self):
        self.ui.buttonAddBlock.clicked.connect(self.addBlock)

    def checkBlockEdit(self):
        self.ui.buttonEditBlock.clicked.connect(self.editBlock)

    def checkBlockRemove(self):
        self.ui.buttonRemoveBlock.clicked.connect(self.removeBlock)

    def checkItemAdd(self):
        self.ui.itemAddButton.clicked.connect(self.addItem)

    def checkItemEdit(self):
        self.ui.buttonEditItem.clicked.connect(self.editItem)

    def checkItemRemove(self):
        self.ui.buttonRemoveItem.clicked.connect(self.removeItem)
    
    def checkRecipeAdd(self):
        self.ui.buttonAddRecipe.clicked.connect(self.addRecipe)
        self.ui.buttonAddRecipe_2.clicked.connect(self.addSmelting)
    
    def checkRecipeRemove(self):
        self.ui.buttonRemoveRecipe.clicked.connect(self.removeRecipe)
    
    def checkRecipeEdit(self):
        self.ui.buttonEditRecipe.clicked.connect(self.editRecipe)

    def checkGenerate(self):
        self.ui.buttonGeneratePack.clicked.connect(self.generate)
    
    def addSmelting(self):
        self.recipeProperties = {
            "name": self.ui.lineEdit.text(),
            "items": self.recipe,
            "mode": "smelting"
        }
    
        self.recipes[self.recipeProperties["name"]] = self.recipeProperties
        self.ui.recipeList.addItem(self.recipeProperties["name"])
        self.clearRecipeFields()

    def addRecipe(self):
        self.recipeProperties = {
            "name": self.ui.lineEdit.text(),
            "shapeless": self.ui.shapeless.isChecked(),
            "exact": self.ui.exact.isChecked(),
            "items": self.recipe,
            "count": str(self.ui.slot9Count.value()),
            "mode": "recipe"
        }

        self.recipes[self.recipeProperties["name"]] = self.recipeProperties
        self.ui.recipeList.addItem(self.recipeProperties["name"])
        self.clearRecipeFields()

    def addItem(self):
        self.itemProperties = {
            "name": self.ui.itemName.text(),
            "displayName": self.ui.itemDisplayName.text(),
            "baseItem": self.ui.itemBase.text(),
            "texture": self.itemTexture,
            "model": self.ui.itemModel.currentText().lower()
        }

        self.items[self.itemProperties["name"]] = self.itemProperties
        self.ui.itemList.addItem(self.itemProperties["name"])
        self.clearItemFields()

    def addBlock(self):
        self.textureNames = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}
        for text in self.texture.keys():
            self.val = self.texture[text]
            self.textureNames[text] = os.path.splitext(os.path.basename(str(self.val)))[0]
        
        if self.ui.blockName.text() == "":
            self.setStatus("Please fill in each field!")
            return
        if self.ui.blockDisplayName.text() == "":
            self.setStatus("Please fill in each field!")
            return
        if self.ui.blockBase.text() == "":
            self.setStatus("Please fill in each field!")
            return
        if '.json' not in self.ui.blockModel.currentText():
            if self.texture["0"] == "":
                self.setStatus("Please fill in each field!")
                return
            if self.texture["1"] == "":
                self.setStatus("Please fill in each field!")
                return
            if self.texture["2"] == "":
                self.setStatus("Please fill in each field!")
                return
            if self.texture["3"] == "":
                self.setStatus("Please fill in each field!")
                return
            if self.texture["4"] == "":
                self.setStatus("Please fill in each field!")
                return
        if self.texture["5"] == "":
            self.setStatus("Please fill in each field!")
            return
        
        self.blockProperties = {
            "name": self.ui.blockName.text(),
            "displayName": self.ui.blockDisplayName.text(),
            "baseBlock": self.ui.blockBase.text(),
            "blockDrop": self.ui.blockDrop.text(),
            "texturePaths": self.texture,
            "textures": self.textureNames,
            "placeSound": self.ui.placeSound.text(),
            "directional": self.ui.directionalCheck.isChecked(),
            "model": self.ui.blockModel.currentText()
        }

        self.blocks[self.blockProperties["name"]] = self.blockProperties

        self.blockNum += 1

        self.ui.blockList.addItem(self.blockProperties["name"])
        self.clearBlockFields()
    
    def clearRecipeFields(self):
        self.recipe = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": ""}
        self.ui.lineEdit.setText("")
        self.ui.shapeless.setChecked(False)
        self.ui.exact.setChecked(False)
        self.ui.slot0Label.setText("")
        self.ui.slot1Label.setText("")
        self.ui.slot2Label.setText("")
        self.ui.slot3Label.setText("")
        self.ui.slot4Label.setText("")
        self.ui.slot5Label.setText("")
        self.ui.slot6Label.setText("")
        self.ui.slot7Label.setText("")
        self.ui.slot8Label.setText("")
        self.ui.slot9Label.setText("")
        self.ui.outputLabel.setText("")
        self.ui.inputLabel.setText("")

    def clearItemFields(self):
        self.itemTexture = None
        self.ui.itemDisplayName.setText("")
        self.ui.itemName.setText("")
        self.ui.itemBase.setText("")
        self.ui.itemTextureLabel.clear()

    def clearBlockFields(self):
        self.texture = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}
        self.ui.blockDisplayName.setText("")
        self.ui.blockName.setText("")
        self.ui.blockBase.setText("")
        self.ui.blockDrop.setText("")
        self.ui.placeSound.setText("")
        self.ui.directionalCheck.setChecked(False)
        self.ui.topFace.clear()
        self.ui.bottomFace.clear()
        self.ui.rightFace.clear()
        self.ui.leftFace.clear()
        self.ui.frontFace.clear()
        self.ui.backFace.clear() 
    
    def editRecipe(self):
        self.curItem = self.ui.recipeList.currentRow()
        self.curItem = self.ui.recipeList.item(self.curItem).text()
        properties = self.recipes[self.recipe]

        self.ui.lineEdit.setText(properties["name"])
        self.ui.shapeless.setChecked(properties["shapeless"])
        self.ui.exact.setChecked(properties["exact"])
        self.ui.slot9Count.setValue(properties["count"])

        self.recipe = properties["items"]

        self.ui.slot0Label.setText(self.recipe["0"])
        self.ui.slot1Label.setText(self.recipe["1"])
        self.ui.slot2Label.setText(self.recipe["2"])
        self.ui.slot3Label.setText(self.recipe["3"])
        self.ui.slot4Label.setText(self.recipe["4"])
        self.ui.slot5Label.setText(self.recipe["5"])
        self.ui.slot6Label.setText(self.recipe["6"])
        self.ui.slot7Label.setText(self.recipe["7"])
        self.ui.slot8Label.setText(self.recipe["8"])
        self.ui.slot9Label.setText(self.recipe["9"])

    def editItem(self):
        self.curItem = self.ui.itemList.currentRow()
        self.curItem = self.ui.itemList.item(self.curItem).text()
        properties = self.items[self.curItem]

        self.ui.itemName.setText(properties["name"])
        self.ui.itemDisplayName.setText(properties["displayName"])
        self.ui.itemBase.setText(properties["baseItem"])
        self.ui.itemModel.setCurrentText(properties["model"])

        self.itemTexture = properties["texture"]

        self.ui.itemTextureLabel.setPixmap(QPixmap.fromImage(QImage(properties["texture"])).scaled(41, 41, Qt.KeepAspectRatio))

    def editBlock(self):
        self.curItem = self.ui.blockList.currentRow()
        self.curItem = self.ui.blockList.item(self.curItem).text()
        properties = self.blocks[self.curItem]

        self.ui.blockName.setText(properties["name"])
        self.ui.blockDisplayName.setText(properties["displayName"])
        self.ui.blockBase.setText(properties["baseBlock"])
        self.ui.blockDrop.setText(properties["blockDrop"])
        self.ui.placeSound.setText(properties["placeSound"])
        self.ui.directionalCheck.setChecked(properties["directional"])
        
        self.ui.frontFace.setPixmap(QPixmap.fromImage(QImage(properties["texturePaths"]["2"])).scaled(41, 41, Qt.KeepAspectRatio))
        self.ui.backFace.setPixmap(QPixmap.fromImage(QImage(properties["texturePaths"]["0"])).scaled(41, 41, Qt.KeepAspectRatio))
        self.ui.rightFace.setPixmap(QPixmap.fromImage(QImage(properties["texturePaths"]["1"])).scaled(41, 41, Qt.KeepAspectRatio))
        self.ui.leftFace.setPixmap(QPixmap.fromImage(QImage(properties["texturePaths"]["3"])).scaled(41, 41, Qt.KeepAspectRatio))
        self.ui.topFace.setPixmap(QPixmap.fromImage(QImage(properties["texturePaths"]["4"])).scaled(41, 41, Qt.KeepAspectRatio))
        self.ui.bottomFace.setPixmap(QPixmap.fromImage(QImage(properties["texturePaths"]["5"])).scaled(41, 41, Qt.KeepAspectRatio))

        self.texture = {
            "0": properties["texturePaths"]["0"],
            "1": properties["texturePaths"]["1"],
            "2": properties["texturePaths"]["2"],
            "3": properties["texturePaths"]["3"],
            "4": properties["texturePaths"]["4"],
            "5": properties["texturePaths"]["5"]
        }

    def removeRecipe(self):
        self.curItem = self.ui.recipeList.currentRow()
        self.recipes.pop(self.ui.recipeList.item(self.curItem).text())
        self.ui.recipeList.takeItem(self.curItem)

    def removeItem(self):
        self.curItem = self.ui.itemList.currentRow()
        self.items.pop(self.ui.itemList.item(self.curItem).text())
        self.ui.itemList.takeItem(self.curItem)  

    def removeBlock(self):
        self.curItem = self.ui.blockList.currentRow()
        self.blocks.pop(self.ui.blockList.item(self.curItem).text())
        self.ui.blockList.takeItem(self.curItem)  

    def parse(self, cmdPrefix, blockNumLoop):
        self.strBlockNumLoop = str(blockNumLoop)
        self.blockNumLoopLen = len(self.strBlockNumLoop)
        self.zeros = 7 - len(cmdPrefix) - self.blockNumLoopLen
        return f'{cmdPrefix}{'0' * self.zeros}{self.strBlockNumLoop}' 
    
    def appendCMD(self, type_, name, cmd):
        self.generated_cmds[type_][name] = cmd

    def generateResourcePack(self, itemModelFile):
        self.outputDir = QFileDialog.getExistingDirectory(self.mainwindow, "Output Directory", "")

        if self.outputDir == "":
            self.setStatus("Please select an output directory!")
            return

        self.packDir = os.path.join(self.outputDir, self.packName + " Resource Pack")
        os.mkdir(self.packDir)
        os.mkdir(self.packDir + "\\assets")
        os.mkdir(self.packDir + "\\assets\\minecraft")
        os.mkdir(self.packDir + "\\assets\\minecraft\\atlases")
        os.mkdir(self.packDir + "\\assets\\minecraft\\models")
        os.mkdir(self.packDir + "\\assets\\minecraft\\textures")
        os.mkdir(self.packDir + "\\assets\\minecraft\\textures\\item")
        os.mkdir(self.packDir + "\\assets\\minecraft\\models\\item")
        os.mkdir(self.packDir + "\\assets\\minecraft\\models\\" + self.nameSpace)

        with open(f'{self.packDir}\\assets\\minecraft\\atlases\\blocks.json', 'w') as f:
            f.write('{"sources":[{"type": "directory","source": "' + self.nameSpace + '","prefix": "' + self.nameSpace + '/"}]}')

        with open(f'{self.packDir}\\pack.mcmeta', 'w') as pack:
            pack.write('{\n    "pack": {\n        "pack_format": 42,\n        "description": "' + self.packDescription + '"\n    }\n}\n')
        with open(f'{self.packDir}\\assets\\minecraft\\models\\item\\item_frame.json', 'a') as file:
            file.write('{"parent": "minecraft:item/generated","textures": {"layer0": "minecraft:item/item_frame"},"overrides":[')
            self.blockNumLoop = 0
            for block in self.blocks:
                self.blockNumLoop += 1
                self.personalCMD = self.parse(self.customModelDataPrefix, self.blockNumLoop)
                file.write('{ "predicate": { "custom_model_data": ' + self.personalCMD + '}, "model": "' + self.nameSpace + '/' + self.blocks[block]["name"] + '"}')
                self.appendCMD("blocks", self.blocks[block]["name"], self.personalCMD)
                if block != next(reversed(self.blocks.keys())):
                    file.write(',')
            file.write('}')
            file.close()
        for self.block in self.blocks:
            self.texturePath = self.packDir + "\\assets\\minecraft\\textures\\item\\"
            if '.json' not in self.blocks[self.block]["model"]:
                for self.path in self.blocks[self.block]["texturePaths"].values():
                    if not os.path.exists(os.path.join(self.texturePath, os.path.splitext(os.path.basename(str(self.path)))[-2] + ".png")):
                        shutil.copy(self.path, os.path.join(self.texturePath, os.path.splitext(os.path.basename(str(self.path)))[-2] + ".png"))
            else:
                self.path = self.blocks[self.block]["texturePaths"]["5"]
                if not os.path.exists(os.path.join(self.texturePath, os.path.splitext(os.path.basename(str(self.path)))[-2] + ".png")):
                        shutil.copy(self.path, os.path.join(self.texturePath, os.path.splitext(os.path.basename(str(self.path)))[-2] + ".png"))
            
        for self.block in self.blocks:
            with open(f'{self.packDir}\\assets\\minecraft\\models\\'+ self.nameSpace + '\\' + self.blocks[self.block]["name"] + '.json', 'w') as file:
                if ".json" not in self.blocks[self.block]["model"]:
                    file.write('{"credit": "Made with mDirt","textures": {"0": "item/' + self.blocks[self.block]["textures"]["0"] + '","1": "item/' + self.blocks[self.block]["textures"]["1"] + '","2": "item/' + self.blocks[self.block]["textures"]["2"] + '","3": "item/' + self.blocks[self.block]["textures"]["3"] + '","4": "item/' + self.blocks[self.block]["textures"]["4"] + '","5": "item/' + self.blocks[self.block]["textures"]["5"] + '","particle": "item/' + self.blocks[self.block]["textures"]["0"] + '"},"elements": [{"from": [0, 0, 0],"to": [16, 16, 16],"faces": {"north": {"uv": [0, 0, 16, 16], "texture": "#0"},"east": {"uv": [0, 0, 16, 16], "texture": "#1"},"south": {"uv": [0, 0, 16, 16], "texture": "#2"},"west": {"uv": [0, 0, 16, 16], "texture": "#3"},"up": {"uv": [0, 0, 16, 16], "texture": "#4"},"down": {"uv": [0, 0, 16, 16], "texture": "#5"}}}],"display": {"thirdperson_righthand": {"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]},"thirdperson_lefthand": {"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]},"firstperson_righthand": {"rotation": [0, 45, 0],"scale": [0.4, 0.4, 0.4]},"ground": {"translation": [0, 3.25, 0],"scale": [0.4, 0.4, 0.4]},"gui": {"rotation": [28, 45, 0],"scale": [0.6, 0.6, 0.6]}}}')
                else:
                    with open(self.blocks[self.block]["model"], 'r') as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][texture] = 'item/' + model["textures"][texture]
                    file.write(str(model).replace("'", '"'))

        for self.item in self.items:
            self.blockNumLoop += 1
            self.modelPath = self.packDir + "\\assets\\minecraft\\models\\item\\"
            self.personalCMD = self.parse(self.customModelDataPrefix, self.blockNumLoop)
            self.appendCMD("items", self.items[self.item]["name"], self.personalCMD)
            if not os.path.exists(f'{self.modelPath}{self.items[self.item]["baseItem"].removeprefix("minecraft:")}.json'): 
                self.exists = 0
            with open(f'{self.modelPath}{self.items[self.item]["baseItem"].removeprefix("minecraft:")}.json', 'a') as file:
                if self.exists == 0:
                    self.exists = 1
                    if ".json" in self.items[self.item]["model"]:
                        self.modelType = itemModelFile[self.items[self.item]["baseItem"]]
                        file.write('{"parent": "' + self.modelType + '", "textures":{"layer0": "minecraft:item/' + self.items[self.item]["baseItem"].removeprefix("minecraft:") + '"},"overrides":[')
                    else:
                        file.write('{"parent": "minecraft:item/' + self.items[self.item]["model"] + '", "textures":{"layer0": "minecraft:item/' + self.items[self.item]["baseItem"].removeprefix("minecraft:") + '"},"overrides":[')
                file.write('{ "predicate": { "custom_model_data": ' + self.personalCMD + '}, "model": "' + self.nameSpace + '/' + self.items[self.item]["name"] + '"},')
        
        for file in os.listdir(self.packDir + "\\assets\\minecraft\\models\\item"):
            if file.endswith('.json'):
                with open(os.path.join(self.packDir + "\\assets\\minecraft\\models\\item\\", file), 'r+') as f:
                    content = f.read()
                    f.seek(0)
                    f.write(content[:-1])
                    f.truncate()
                    f.write(']}')
        
        for self.item in self.items:
            self.currentPath = f'{self.packDir}\\assets\\minecraft\\models\\{self.nameSpace}'
            with open(f'{self.currentPath}\\{self.items[self.item]["name"]}.json', 'w') as file:
                if ".json" in self.items[self.item]["model"]:
                    with open(self.items[self.item]["model"], 'r') as f:
                        model = ast.literal_eval(f.read())
                        f.close()
                    for texture in model["textures"]:
                        model["textures"][texture] = self.nameSpace + '/' + model["textures"][texture]
                    file.write(str(model).replace("'", '"'))
                else:
                    file.write('{"parent":"minecraft:item/' + self.items[self.item]["model"] + '", "textures": { "layer0": "minecraft:' + self.nameSpace + '/' + os.path.splitext(os.path.basename(str(self.items[self.item]["texture"])))[-2] + '"}}')
        
        os.mkdir(f'{self.packDir}\\assets\\minecraft\\textures\\{self.nameSpace}')

        for self.item in self.items:
            self.currentPath = f'{self.packDir}\\assets\\minecraft\\textures\\{self.nameSpace}'
            shutil.copy(self.items[self.item]["texture"], os.path.normpath(f'{self.currentPath}\\{os.path.splitext(os.path.basename(str(self.items[self.item]["texture"])))[-2]}.png'))  

    def generate(self):
        
        self.setStatus("Generating...")

        with open(f'{os.path.dirname(os.path.abspath(__file__)) + '\\data.json'}', 'r') as f:
            self.item_models = json.load(f)["models"]
        
        for self.itm in self.items:
            if self.items[self.itm]["baseItem"] not in self.item_models.keys():
                self.setStatus(f"The item '{self.items[self.itm]["name"]}' has an unsupported Base Item!")
                return

        self.nameSpace = self.ui.packNamespace.text()
        if self.nameSpace == "":
            self.setStatus("Input a proper Namespace!")
            return
        
        self.packName = self.ui.packName.text()

        if self.packName == "":
            self.setStatus("Input a proper Pack Name!")
            return
        
        self.packDescription = self.ui.packDescription.text()
        
        if self.packDescription == "":
            self.setStatus("Input a proper Pack Description!")
            return

        self.packAuthor = self.ui.author.text()
        if self.packAuthor == "":
            self.setStatus("Input a proper Author name!")
            return
        
        self.customModelDataPrefix = self.ui.vmdPrefix.text()
        if self.customModelDataPrefix == "":
            self.setStatus("Input a proper CMD Prefix!")
            return

        self.generateResourcePack(self.item_models)

        self.outputDir = QFileDialog.getExistingDirectory(self.mainwindow, "Output Directory", "")
        if self.outputDir == "":
            self.setStatus("Please select an output directory!")
            return

        self.packDir = os.path.join(self.outputDir, self.packName)
        os.mkdir(self.packDir)
        os.mkdir(self.packDir + "\\data")
        self.packNamespace = os.path.join(self.packDir, "data", self.nameSpace)
        self.minecraft = os.path.join(self.packDir, "data", "minecraft")
        os.mkdir(self.minecraft)
        os.mkdir(self.packNamespace)

        with open(f'{self.packDir}\\pack.mcmeta', 'w') as pack:
            pack.write('{\n    "pack": {\n        "pack_format": 57,\n        "description": "' + self.ui.packDescription.text() + '"\n    }\n}\n')
            pack.close()
        
        os.mkdir(self.packNamespace + "\\function")
        os.mkdir(self.packNamespace + "\\loot_table")
        os.mkdir(self.packNamespace + "\\advancement")
        os.mkdir(self.packNamespace + "\\recipe")

        os.mkdir(self.minecraft + "\\tags")
        os.mkdir(self.minecraft + "\\tags" + "\\function")

        with open(f'{self.packNamespace}\\function\\tick.mcfunction', 'w') as tick:
            tick.write(self.header + 'execute as @e[type=item_display,tag=' + self.packAuthor + ".custom_block] at @s run function " + self.nameSpace + ":as_blocks")
            tick.close()
        with open(f'{self.packNamespace}\\function\\load.mcfunction', 'w') as load:
            load.write(self.header + 'tellraw @a {"text":"[mDirt] - Successfully loaded pack!","color":"red"}')
            load.close()
        with open(f'{self.minecraft}\\tags\\function\\tick.json', 'w') as tickJS:
            tickJS.write('{\n    "values":[\n        ' + f'"{self.nameSpace}' + ':tick"\n        ]\n    }')
            tickJS.close()
        with open(f'{self.minecraft}\\tags\\function\\load.json', 'w') as loadJS:
            loadJS.write('{\n    "values":[\n        ' + f'"{self.nameSpace}' + ':load"\n        ]\n    }')
            loadJS.close()
        
        # Placed Item Frame Advancement

        with open(f'{self.packNamespace}\\advancement\\placed_item_frame.json', 'w') as file:
            file.write('{"criteria": {"requirement": {"trigger": "minecraft:item_used_on_block","conditions": {"location": [{"condition": "minecraft:match_tool","predicate": {"items": ["minecraft:item_frame"]}}]}}},"rewards": {"function": "' + self.nameSpace + ':placed_item_frame"}}')
            file.close()
        
        # Placed Item Frame Function

        with open(f'{self.packNamespace}\\function\\placed_item_frame.mcfunction', 'w') as file:
            file.write(self.header + 'advancement revoke @s only ' + self.nameSpace + ':placed_item_frame\nexecute as @e[tag=' + self.packAuthor + '.item_frame_block,distance=..10] at @s run function ' + self.nameSpace + ':check_placed_item_frame')
            file.close()

        # Check Placed Item Frame, block/place Functions

        with open(f'{self.packNamespace}\\function\\check_placed_item_frame.mcfunction', 'a') as file:
            self.blockNumLoop = 0
            for self.blck in self.blocks.keys():
                self.blockNumLoop += 1
                self.personalCMD = self.parse(self.customModelDataPrefix, self.blockNumLoop)
                os.mkdir(self.packNamespace + "\\function" + f"\\{self.blck}")
                with open(f'{self.packNamespace}\\function\\{self.blck}\\place.mcfunction', 'a') as file2:
                    file2.write(self.header + "setblock ~ ~ ~ " + self.blocks[self.blck]["baseBlock"] + ' keep\n')
                    if self.blocks[self.block]["placeSound"] != "":
                        file2.write("playsound " + self.blocks[self.block]["placeSound"] + " block @e[type=player,distance=..5] ~ ~ ~ 10 1 1\n")
                    if self.blocks[self.block]["directional"]:
                        file2.write('execute at @p if entity @p[y_rotation=135..-135,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~-0.469 {Rotation:[0F,90F],brightness:{sky:15,block:0},Tags:["' + self.packAuthor + f'.{self.blocks[self.blck]["name"]}","' + self.packAuthor + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.personalCMD + '}}}\n')
                        file2.write('execute at @p if entity @p[y_rotation=-135..-45,x_rotation=-45..45] at @s run summon item_display ~0.469 ~0.469 ~ {Rotation:[90F,90F],brightness:{sky:15,block:0},Tags:["' + self.packAuthor + f'.{self.blocks[self.blck]["name"]}","' + self.packAuthor + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.personalCMD + '}}}\n')
                        file2.write('execute at @p if entity @p[y_rotation=-45..45,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~0.469 {Rotation:[180F,90F],brightness:{sky:15,block:0},Tags:["' + self.packAuthor + f'.{self.blocks[self.blck]["name"]}","' + self.packAuthor + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.personalCMD + '}}}\n')
                        file2.write('execute at @p if entity @p[y_rotation=45..135,x_rotation=-45..45] at @s run summon item_display ~-0.469 ~0.469 ~ {Rotation:[90F,-90F],brightness:{sky:15,block:0},Tags:["' + self.packAuthor + f'.{self.blocks[self.blck]["name"]}","' + self.packAuthor + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.personalCMD + '}}}\n')
                        file2.write('execute if entity @p[x_rotation=45..90] at @s run summon item_display ~ ~ ~ {brightness:{sky:15,block:0},Tags:["' + self.packAuthor + f'.{self.blocks[self.blck]["name"]}","' + self.packAuthor + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.personalCMD + '}}}\n')
                        file2.write('execute if entity @p[x_rotation=-90..-45] at @s run summon item_display ~ ~0.469 ~-0.47 {Rotation:[0F,90F],brightness:{sky:15,block:0},Tags:["' + self.packAuthor + f'.{self.blocks[self.blck]["name"]}","' + self.packAuthor + '.custom_block"],transformation:{left_rotation:[0f,-1f,1f,1f],right_rotation:[1.000f,0.5f,0.5f,0f],translation:[0f,0.47f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.personalCMD + '}}}\n')
                    else:
                        file2.write('summon item_display ~ ~ ~ {brightness:{sky:15,block:0},Tags:["' + self.packAuthor + f'.{self.blocks[self.blck]["name"]}","' + self.packAuthor + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.personalCMD + '}}}\n')
                    file2.close()
                file.write(self.header + 'execute as @s[tag=' + self.packAuthor + '.' + self.blocks[self.blck]["name"] + '] run function ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '/place\n')
            
            file.write('\nkill @s')
            file.close()
        
        # As Blocks block/block, block/break Functions

        with open(f'{self.packNamespace}\\function\\as_blocks.mcfunction', 'a') as file:
            for self.blck in self.blocks.keys():
                with open(f'{self.packNamespace}\\function\\{self.blck}\\{self.blck}.mcfunction', 'w') as file2:
                    file2.write(self.header + 'execute unless block ~ ~ ~ ' + self.blocks[self.blck]["baseBlock"] + ' run function ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '/break')
                    file2.close()
                with open(f'{self.packNamespace}\\function\\{self.blck}\\break.mcfunction', 'a') as file3:
                    file3.write(self.header + 'execute as @e[type=item,sort=nearest,limit=1,distance=..2,nbt={OnGround:0b,Age:0s,Item:{id:"' + self.blocks[self.blck]["baseBlock"] + '"}}] run kill @s\n')
                    file3.write('loot spawn ~ ~ ~ loot ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '\n')
                    file3.write('kill @s')
                    file3.close()
                
                file.write(self.header + 'execute as @s[tag=' + self.packAuthor + '.' + self.blocks[self.blck]["name"] + '] run function ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '/' + self.blocks[self.blck]["name"] + '\n')
            file.close()
        
        # Give Items Function

        with open(f'{self.packNamespace}\\function\\give_items.mcfunction', 'a') as file:
            self.blockNumLoop = 0
            for self.blck in self.blocks.keys():
                self.blockNumLoop += 1
                self.personalCMD = self.parse(self.customModelDataPrefix, self.blockNumLoop)
                file.write(self.header + 'give @s item_frame[item_name=\'{"italic":false,"text":"' + self.blocks[self.blck]["displayName"] + '"}\',custom_model_data=' + self.personalCMD + ',entity_data={id:"minecraft:item_frame",Fixed:1b,Invisible:1b,Silent:1b,Invulnerable:1b,Facing:1,Tags:["' + self.packAuthor + '.item_frame_block","' + self.packAuthor + '.' + self.blocks[self.blck]["name"] + '"]}] 1\n')
            for self.itm in self.items.keys():
                self.blockNumLoop += 1
                self.personalCMD = self.parse(self.customModelDataPrefix, self.blockNumLoop)
                file.write('give @s ' + self.items[self.itm]["baseItem"] + '[item_name=\'{"italic":false,"text":"' + self.items[self.itm]["displayName"] + '"}\',custom_model_data=' + self.personalCMD + '] 1\n')
            file.close()
        
        
        # Loot Tables

        self.blockNumLoop = 0
        for self.blck in self.blocks.keys():
            self.blockNumLoop += 1
            self.personalCMD = self.parse(self.customModelDataPrefix, self.blockNumLoop)
            with open(f'{self.packNamespace}\\loot_table\\{self.blocks[self.blck]["name"]}.json', 'w') as file:
                if self.blocks[self.blck]["blockDrop"] == "":
                    file.write('{"pools": [{"rolls": 1,"entries": [{"type": "minecraft:item","name": "minecraft:item_frame"}],"functions": [{"function": "minecraft:set_components","components": {"minecraft:custom_model_data": ' + self.personalCMD + ',"minecraft:custom_name": "{\\"italic\\":false,\\"text\\":\\"' + self.blocks[self.blck]["displayName"] + '\\"}","minecraft:entity_data": {"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["' + self.packAuthor + '.item_frame_block","' + self.packAuthor + '.' + self.blocks[self.blck]["name"] + '"]}}}]}]}')
                else:
                    file.write('{"pools": [{"rolls": 1,"entries": [{"type": "minecraft:item","name": "' + self.blocks[self.blck]["blockDrop"] + '"}]}]}')
                
                file.close()
        
        # Recipes

        for recipe in self.recipes:
            if self.recipes[recipe]["mode"] == "recipe":
                if not self.recipes[recipe]["shapeless"]:
                    with open(f'{self.packNamespace}\\recipe\\{self.recipes[recipe]["name"]}.json', 'a') as file:
                        file.truncate(0)
                        file.seek(0)
                        letters = {"0": "A", "1": "D", "2": "G", "3": "B", "4": "E", "5": "H", "6": "C", "7": "F", "8": "I"}
                        recip = self.recipes[recipe]["items"]
                        file.write('{"type": "minecraft:crafting_shaped", "pattern": ["')
                        if recip["0"] != "":
                            file.write("A")
                        else:
                            file.write(" ")
                        if recip["3"] != "":
                            file.write("B")
                        else:
                            file.write(" ")
                        if recip["6"] != "":
                            file.write("C")
                        else:
                            file.write(" ")
                        
                        file.write('","')

                        if recip["1"] != "":
                            file.write("D")
                        else:
                            file.write(" ")
                        if recip["4"] != "":
                            file.write("E")
                        else:
                            file.write(" ")
                        if recip["7"] != "":
                            file.write("F")
                        else:
                            file.write(" ")
                        
                        file.write('","')

                        if recip["2"] != "":
                            file.write("G")
                        else:
                            file.write(" ")
                        if recip["5"] != "":
                            file.write("H")
                        else:
                            file.write(" ")
                        if recip["8"] != "":
                            file.write("I")
                        else:
                            file.write(" ")

                        file.write('"],"key":{')
                        items = [(k, v) for k, v in recip.items() if v not in (None, '')][:-1]
                        for i, (key, value) in enumerate(items):
                            if value != "" and value != None:
                                file.write('"' + letters[str(key).replace("'", '"')] + '":"minecraft:' + value + '"')
                                if i < len(items) -1: file.write(',')
                        if not recip["9"] in self.items and not recip["9"] in self.blocks:
                            file.write('},"result": { "id":"minecraft:' + recip[str(9)] + '", "count":' + self.recipes[recipe]["count"] + '}}')
                        elif recip["9"] in self.items:
                            idx = self.items[recip["9"]]
                            file.write('},"result":{ "id":"' + idx["baseItem"] + '", "count":' + self.recipes[recipe]["count"] + ', "components": {"minecraft:item_name":"{\"italic\":false,\"text\":\"' + idx["displayName"] + '\"}", "minecraft:custom_model_data": ' + self.generated_cmds["items"][idx["name"]] + '}}}')
                        elif recip["9"] in self.blocks:
                            idx = self.blocks[recip["9"]]
                            file.write('},"result":{ "id":"' + 'minecraft:item_frame' + '", "count":' + self.recipes[recipe]["count"] + ', "components": {"minecraft:custom_model_data": ' + self.generated_cmds["blocks"][idx["name"]] + ',"minecraft:custom_name": "{\\"italic\\":false,\\"text\\":\\"' + idx["displayName"] + '\\"}","minecraft:entity_data": {"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["' + self.packAuthor + '.item_frame_block","' + self.packAuthor + '.' + idx["name"] + '"]}}}}')
                            
                else:
                    with open(f'{self.packNamespace}\\recipe\\{self.recipes[recipe]["name"]}.json', 'a') as file:
                        recip = self.recipes[recipe]["items"]
                        file.write('{"type": "minecraft:crafting_shapeless", "ingredients": [')
                        items = [(k, v) for k, v in recip.items() if v not in (None, '')][:-3]
                        for ingredient, (key, value) in enumerate(items):
                            if str(value) != "":
                                file.write('"minecraft:' + str(value) + '"')
                                if ingredient < len(items) - 1: file.write(',')
                        if not recip["9"] in self.items and not recip["9"] in self.blocks:
                            file.write('],"result":{"id": "minecraft:' + recip[str(9)] + '", "count":' + self.recipes[recipe]["count"] + '}}')
                        elif recip["9"] in self.items:
                            idx = self.items[recip["9"]]
                            file.write('},"result":{ "id":"' + idx["baseItem"] + '", "count":' + self.recipes[recipe]["count"] + ', "components": {"minecraft:item_name":"{\"italic\":false,\"text\":\"' + idx["displayName"] + '\"}", "minecraft:custom_model_data": ' + self.generated_cmds["items"][idx["name"]] + '}}}')
                        elif recip["9"] in self.blocks:
                            idx = self.blocks[recip["9"]]
                            file.write('},"result":{ "id":"' + 'minecraft:item_frame' + '", "count":' + self.recipes[recipe]["count"] + ', "components": {"minecraft:custom_model_data": ' + self.generated_cmds["blocks"][idx["name"]] + ',"minecraft:custom_name": "{\\"italic\\":false,\\"text\\":\\"' + idx["displayName"] + '\\"}","minecraft:entity_data": {"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["' + self.packAuthor + '.item_frame_block","' + self.packAuthor + '.' + idx["name"] + '"]}}}}')
            
            elif self.recipes[recipe]["mode"] == "smelting":
                with open(f'{self.packNamespace}\\recipe\\{self.recipes[recipe]["name"]}.json', 'a') as file:
                    recip = self.recipes[recipe]["items"]
                    if not recip["11"] in self.items and not recip["11"] in self.blocks:
                        file.write('{ "type": "minecraft:smelting", "ingredient": "minecraft:' + recip["10"] + '", "result": { "id": "minecraft:' + recip["11"] + '"}}')
                    elif recip["11"] in self.items:
                        idx = self.items[recip["11"]]
                        file.write('{ "type": "minecraft:smelting", "ingredient": "minecraft:' + recip["10"] + '", "result": { "id": "minecraft:' + recip["11"] + '", "components": {"minecraft:item_name":"{\"italic\":false,\"text\":\"' + idx["displayName"] + '\"}", "minecraft:custom_model_data": ' + self.generated_cmds["items"][idx["name"]] + '}}}')
                    elif recip["11"] in self.blocks:
                        idx = self.blocks[recip["11"]]
                        file.write('},"result":{ "id":"' + 'minecraft:item_frame' + '", "count":' + self.recipes[recipe]["count"] + ', "components": {"minecraft:custom_model_data": ' + self.generated_cmds["blocks"][idx["name"]] + ',"minecraft:custom_name": "{\\"italic\\":false,\\"text\\":\\"' + idx["displayName"] + '\\"}","minecraft:entity_data": {"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["' + self.packAuthor + '.item_frame_block","' + self.packAuthor + '.' + idx["name"] + '"]}}}}')

        self.setStatus("Generated!")     

if __name__ == '__main__':
    app()