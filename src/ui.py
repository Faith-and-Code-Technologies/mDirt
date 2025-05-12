# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uiSTaFBF.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QFormLayout, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpinBox, QStackedWidget, QStatusBar, QTabWidget,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1003, 737)
        MainWindow.setStyleSheet(u"/*mDirt Dev Theme - Dark Earthy */\n"
"\n"
"* {\n"
"    font-family: \"JetBrains Mono\", \"Consolas\", monospace;\n"
"    font-size: 13px;\n"
"    color: #e9e9e9;\n"
"}\n"
"\n"
"QWidget {\n"
"    background-color: #1c1a16;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #3b553c;\n"
"    color: #ffffff;\n"
"    border: 1px solid #5e7e5f;\n"
"    border-radius: 5px;\n"
"    padding: 6px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4d6e4f;\n"
"    border-color: #89b089;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #36503a;\n"
"}\n"
"\n"
"QLineEdit, QTextEdit {\n"
"    background-color: #2b2a26;\n"
"    border: 1px solid #464642;\n"
"    border-radius: 4px;\n"
"    padding: 4px 6px;\n"
"    color: #eaeaea;\n"
"}\n"
"\n"
"QLineEdit:focus, QTextEdit:focus {\n"
"    border: 1px solid #7da87d;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #ccc9b5;\n"
"}\n"
"\n"
"QComboBox {\n"
"    background-color: #2b2a26;\n"
"    border: 1px solid #464642;\n"
"    border-radius: 4px;\n"
"   "
                        " padding: 4px;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border-color: #7da87d;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #5a5a50;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: #3b3731;\n"
"    color: #b5b5a5;\n"
"    padding: 6px 12px;\n"
"    border-top-left-radius: 6px;\n"
"    border-top-right-radius: 6px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: #4e4a40;\n"
"    color: #d7f7d4;\n"
"}\n"
"\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
"    background: #1c1a16;\n"
"    border: none;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
"    background: #575342;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:hover {\n"
"    background: #7da87d;\n"
"}\n"
"\n"
"QToolTip {\n"
"    background-color: #3b553c;\n"
"    color: #f4f4f4;\n"
"    border: 1px solid #7da87d;\n"
"    padding: 4px;\n"
"    border-radius: 4px;\n"
"}")
        self.actionBlock = QAction(MainWindow)
        self.actionBlock.setObjectName(u"actionBlock")
        self.actionRecipie = QAction(MainWindow)
        self.actionRecipie.setObjectName(u"actionRecipie")
        self.actionPaintings = QAction(MainWindow)
        self.actionPaintings.setObjectName(u"actionPaintings")
        self.actionItems = QAction(MainWindow)
        self.actionItems.setObjectName(u"actionItems")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionExport_Pack = QAction(MainWindow)
        self.actionExport_Pack.setObjectName(u"actionExport_Pack")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayout_2 = QFormLayout(self.centralwidget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.elementVeiwer = QTreeWidget(self.centralwidget)
        font = QFont()
        font.setBold(True)
        font.setUnderline(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(0, font);
        self.elementVeiwer.setHeaderItem(__qtreewidgetitem)
        self.elementVeiwer.setObjectName(u"elementVeiwer")
        self.elementVeiwer.setMinimumSize(QSize(211, 0))

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.elementVeiwer)

        self.elementEditor = QStackedWidget(self.centralwidget)
        self.elementEditor.setObjectName(u"elementEditor")
        self.welcomeScreen = QWidget()
        self.welcomeScreen.setObjectName(u"welcomeScreen")
        self.gridLayout_4 = QGridLayout(self.welcomeScreen)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.textEdit = QTextEdit(self.welcomeScreen)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.gridLayout_4.addWidget(self.textEdit, 0, 0, 1, 1)

        self.elementEditor.addWidget(self.welcomeScreen)
        self.blockEditor = QWidget()
        self.blockEditor.setObjectName(u"blockEditor")
        self.blockTextureButtonBottom = QPushButton(self.blockEditor)
        self.blockTextureButtonBottom.setObjectName(u"blockTextureButtonBottom")
        self.blockTextureButtonBottom.setGeometry(QRect(330, 150, 50, 50))
        self.blockTextureButtonBottom.setFlat(True)
        self.blockTextureButtonTop = QPushButton(self.blockEditor)
        self.blockTextureButtonTop.setObjectName(u"blockTextureButtonTop")
        self.blockTextureButtonTop.setGeometry(QRect(330, 30, 50, 50))
        self.blockTextureButtonTop.setFlat(True)
        self.blockTextureButtonLeft = QPushButton(self.blockEditor)
        self.blockTextureButtonLeft.setObjectName(u"blockTextureButtonLeft")
        self.blockTextureButtonLeft.setGeometry(QRect(270, 90, 50, 50))
        self.blockTextureButtonLeft.setFlat(True)
        self.blockTextureButtonBack = QPushButton(self.blockEditor)
        self.blockTextureButtonBack.setObjectName(u"blockTextureButtonBack")
        self.blockTextureButtonBack.setGeometry(QRect(330, 90, 50, 50))
        self.blockTextureButtonBack.setFlat(True)
        self.blockTextureButtonFront = QPushButton(self.blockEditor)
        self.blockTextureButtonFront.setObjectName(u"blockTextureButtonFront")
        self.blockTextureButtonFront.setGeometry(QRect(450, 90, 50, 50))
        self.blockTextureButtonFront.setFlat(True)
        self.blockTextureButtonRight = QPushButton(self.blockEditor)
        self.blockTextureButtonRight.setObjectName(u"blockTextureButtonRight")
        self.blockTextureButtonRight.setGeometry(QRect(390, 90, 50, 50))
        self.blockTextureButtonRight.setFlat(True)
        self.blockTextureLabel = QLabel(self.blockEditor)
        self.blockTextureLabel.setObjectName(u"blockTextureLabel")
        self.blockTextureLabel.setGeometry(QRect(260, 10, 49, 16))
        self.layoutWidget = QWidget(self.blockEditor)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 241, 251))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.blockDirectional = QCheckBox(self.layoutWidget)
        self.blockDirectional.setObjectName(u"blockDirectional")

        self.gridLayout.addWidget(self.blockDirectional, 5, 1, 1, 1)

        self.blockModel = QComboBox(self.layoutWidget)
        self.blockModel.addItem("")
        self.blockModel.addItem("")
        self.blockModel.setObjectName(u"blockModel")

        self.gridLayout.addWidget(self.blockModel, 6, 1, 1, 1)

        self.blockPlaceSoundLabel = QLabel(self.layoutWidget)
        self.blockPlaceSoundLabel.setObjectName(u"blockPlaceSoundLabel")

        self.gridLayout.addWidget(self.blockPlaceSoundLabel, 4, 0, 1, 1)

        self.blockDropLabel = QLabel(self.layoutWidget)
        self.blockDropLabel.setObjectName(u"blockDropLabel")

        self.gridLayout.addWidget(self.blockDropLabel, 3, 0, 1, 1)

        self.blockBaseBlock = QLineEdit(self.layoutWidget)
        self.blockBaseBlock.setObjectName(u"blockBaseBlock")

        self.gridLayout.addWidget(self.blockBaseBlock, 2, 1, 1, 1)

        self.blockDisplayName = QLineEdit(self.layoutWidget)
        self.blockDisplayName.setObjectName(u"blockDisplayName")

        self.gridLayout.addWidget(self.blockDisplayName, 0, 1, 1, 1)

        self.blockDirectionalLabel = QLabel(self.layoutWidget)
        self.blockDirectionalLabel.setObjectName(u"blockDirectionalLabel")

        self.gridLayout.addWidget(self.blockDirectionalLabel, 5, 0, 1, 1)

        self.blockPlaceSound = QLineEdit(self.layoutWidget)
        self.blockPlaceSound.setObjectName(u"blockPlaceSound")

        self.gridLayout.addWidget(self.blockPlaceSound, 4, 1, 1, 1)

        self.blockDropBox = QComboBox(self.layoutWidget)
        self.blockDropBox.setObjectName(u"blockDropBox")
        self.blockDropBox.setEditable(True)

        self.gridLayout.addWidget(self.blockDropBox, 3, 1, 1, 1)

        self.blockModelLabel = QLabel(self.layoutWidget)
        self.blockModelLabel.setObjectName(u"blockModelLabel")

        self.gridLayout.addWidget(self.blockModelLabel, 6, 0, 1, 1)

        self.blockNameLabel = QLabel(self.layoutWidget)
        self.blockNameLabel.setObjectName(u"blockNameLabel")

        self.gridLayout.addWidget(self.blockNameLabel, 1, 0, 1, 1)

        self.blockDisplayNameLabel = QLabel(self.layoutWidget)
        self.blockDisplayNameLabel.setObjectName(u"blockDisplayNameLabel")

        self.gridLayout.addWidget(self.blockDisplayNameLabel, 0, 0, 1, 1)

        self.blockName = QLineEdit(self.layoutWidget)
        self.blockName.setObjectName(u"blockName")

        self.gridLayout.addWidget(self.blockName, 1, 1, 1, 1)

        self.blockBaseBlockName = QLabel(self.layoutWidget)
        self.blockBaseBlockName.setObjectName(u"blockBaseBlockName")

        self.gridLayout.addWidget(self.blockBaseBlockName, 2, 0, 1, 1)

        self.blockConfirmButton = QPushButton(self.layoutWidget)
        self.blockConfirmButton.setObjectName(u"blockConfirmButton")

        self.gridLayout.addWidget(self.blockConfirmButton, 7, 0, 1, 2)

        self.blockTextureLabelLeft = QLabel(self.blockEditor)
        self.blockTextureLabelLeft.setObjectName(u"blockTextureLabelLeft")
        self.blockTextureLabelLeft.setGeometry(QRect(270, 90, 50, 50))
        self.blockTextureLabelBottom = QLabel(self.blockEditor)
        self.blockTextureLabelBottom.setObjectName(u"blockTextureLabelBottom")
        self.blockTextureLabelBottom.setGeometry(QRect(330, 150, 50, 50))
        self.blockTextureLabelBack = QLabel(self.blockEditor)
        self.blockTextureLabelBack.setObjectName(u"blockTextureLabelBack")
        self.blockTextureLabelBack.setGeometry(QRect(330, 90, 50, 50))
        self.blockTextureLabelTop = QLabel(self.blockEditor)
        self.blockTextureLabelTop.setObjectName(u"blockTextureLabelTop")
        self.blockTextureLabelTop.setGeometry(QRect(330, 30, 50, 50))
        self.blockTextureLabelRight = QLabel(self.blockEditor)
        self.blockTextureLabelRight.setObjectName(u"blockTextureLabelRight")
        self.blockTextureLabelRight.setGeometry(QRect(390, 90, 50, 50))
        self.blockTextureLabelFront = QLabel(self.blockEditor)
        self.blockTextureLabelFront.setObjectName(u"blockTextureLabelFront")
        self.blockTextureLabelFront.setGeometry(QRect(450, 90, 50, 50))
        self.elementEditor.addWidget(self.blockEditor)
        self.blockTextureLabelFront.raise_()
        self.blockTextureLabelRight.raise_()
        self.blockTextureLabelTop.raise_()
        self.blockTextureLabelBack.raise_()
        self.blockTextureLabelBottom.raise_()
        self.blockTextureLabelLeft.raise_()
        self.blockTextureButtonBottom.raise_()
        self.blockTextureButtonTop.raise_()
        self.blockTextureButtonLeft.raise_()
        self.blockTextureButtonBack.raise_()
        self.blockTextureButtonFront.raise_()
        self.blockTextureButtonRight.raise_()
        self.blockTextureLabel.raise_()
        self.layoutWidget.raise_()
        self.recipeEditor = QWidget()
        self.recipeEditor.setObjectName(u"recipeEditor")
        self.formLayout = QFormLayout(self.recipeEditor)
        self.formLayout.setObjectName(u"formLayout")
        self.recipeNameLabel = QLabel(self.recipeEditor)
        self.recipeNameLabel.setObjectName(u"recipeNameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.recipeNameLabel)

        self.recipeName = QLineEdit(self.recipeEditor)
        self.recipeName.setObjectName(u"recipeName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.recipeName)

        self.recipeSubTabs = QTabWidget(self.recipeEditor)
        self.recipeSubTabs.setObjectName(u"recipeSubTabs")
        self.craftingTab = QWidget()
        self.craftingTab.setObjectName(u"craftingTab")
        self.slot0Button = QPushButton(self.craftingTab)
        self.slot0Button.setObjectName(u"slot0Button")
        self.slot0Button.setGeometry(QRect(40, 40, 50, 50))
        self.slot0Button.setFlat(True)
        self.slot1Button = QPushButton(self.craftingTab)
        self.slot1Button.setObjectName(u"slot1Button")
        self.slot1Button.setGeometry(QRect(90, 40, 50, 50))
        self.slot1Button.setFlat(True)
        self.slot2Button = QPushButton(self.craftingTab)
        self.slot2Button.setObjectName(u"slot2Button")
        self.slot2Button.setGeometry(QRect(140, 40, 50, 50))
        self.slot2Button.setFlat(True)
        self.slot3Button = QPushButton(self.craftingTab)
        self.slot3Button.setObjectName(u"slot3Button")
        self.slot3Button.setGeometry(QRect(40, 90, 50, 50))
        self.slot3Button.setFlat(True)
        self.slot4Button = QPushButton(self.craftingTab)
        self.slot4Button.setObjectName(u"slot4Button")
        self.slot4Button.setGeometry(QRect(90, 90, 50, 50))
        self.slot4Button.setFlat(True)
        self.slot5Button = QPushButton(self.craftingTab)
        self.slot5Button.setObjectName(u"slot5Button")
        self.slot5Button.setGeometry(QRect(140, 90, 50, 50))
        self.slot5Button.setFlat(True)
        self.slot6Button = QPushButton(self.craftingTab)
        self.slot6Button.setObjectName(u"slot6Button")
        self.slot6Button.setGeometry(QRect(40, 140, 50, 50))
        self.slot6Button.setFlat(True)
        self.slot7Button = QPushButton(self.craftingTab)
        self.slot7Button.setObjectName(u"slot7Button")
        self.slot7Button.setGeometry(QRect(90, 140, 50, 50))
        self.slot7Button.setFlat(True)
        self.slot8Button = QPushButton(self.craftingTab)
        self.slot8Button.setObjectName(u"slot8Button")
        self.slot8Button.setGeometry(QRect(140, 140, 50, 50))
        self.slot8Button.setFlat(True)
        self.slot9Button = QPushButton(self.craftingTab)
        self.slot9Button.setObjectName(u"slot9Button")
        self.slot9Button.setGeometry(QRect(250, 90, 50, 50))
        self.slot9Button.setFlat(True)
        self.slot9Count = QSpinBox(self.craftingTab)
        self.slot9Count.setObjectName(u"slot9Count")
        self.slot9Count.setGeometry(QRect(250, 140, 88, 24))
        self.slot9Count.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.slot9Count.setMinimum(1)
        self.slot9Count.setMaximum(64)
        self.shapelessRadio = QRadioButton(self.craftingTab)
        self.shapelessRadio.setObjectName(u"shapelessRadio")
        self.shapelessRadio.setGeometry(QRect(50, 200, 92, 20))
        self.shapelessRadio.setAutoRepeat(False)
        self.shapelessRadio.setAutoExclusive(True)
        self.exactlyRadio = QRadioButton(self.craftingTab)
        self.exactlyRadio.setObjectName(u"exactlyRadio")
        self.exactlyRadio.setGeometry(QRect(50, 230, 161, 20))
        self.exactlyRadio.setChecked(True)
        self.exactlyRadio.setAutoRepeat(False)
        self.exactlyRadio.setAutoExclusive(True)
        self.slot0 = QLabel(self.craftingTab)
        self.slot0.setObjectName(u"slot0")
        self.slot0.setGeometry(QRect(40, 40, 50, 50))
        self.slot1 = QLabel(self.craftingTab)
        self.slot1.setObjectName(u"slot1")
        self.slot1.setGeometry(QRect(90, 40, 50, 50))
        self.slot2 = QLabel(self.craftingTab)
        self.slot2.setObjectName(u"slot2")
        self.slot2.setGeometry(QRect(140, 40, 50, 50))
        self.slot3 = QLabel(self.craftingTab)
        self.slot3.setObjectName(u"slot3")
        self.slot3.setGeometry(QRect(40, 90, 50, 50))
        self.slot4 = QLabel(self.craftingTab)
        self.slot4.setObjectName(u"slot4")
        self.slot4.setGeometry(QRect(90, 90, 50, 50))
        self.slot5 = QLabel(self.craftingTab)
        self.slot5.setObjectName(u"slot5")
        self.slot5.setGeometry(QRect(140, 90, 50, 50))
        self.slot6 = QLabel(self.craftingTab)
        self.slot6.setObjectName(u"slot6")
        self.slot6.setGeometry(QRect(40, 140, 50, 50))
        self.slot7 = QLabel(self.craftingTab)
        self.slot7.setObjectName(u"slot7")
        self.slot7.setGeometry(QRect(90, 140, 50, 50))
        self.slot8 = QLabel(self.craftingTab)
        self.slot8.setObjectName(u"slot8")
        self.slot8.setGeometry(QRect(140, 140, 50, 50))
        self.slot9 = QLabel(self.craftingTab)
        self.slot9.setObjectName(u"slot9")
        self.slot9.setGeometry(QRect(250, 90, 50, 50))
        self.recipeSubTabs.addTab(self.craftingTab, "")
        self.slot9Count.raise_()
        self.shapelessRadio.raise_()
        self.exactlyRadio.raise_()
        self.slot0.raise_()
        self.slot1.raise_()
        self.slot2.raise_()
        self.slot3.raise_()
        self.slot4.raise_()
        self.slot5.raise_()
        self.slot6.raise_()
        self.slot7.raise_()
        self.slot8.raise_()
        self.slot9.raise_()
        self.slot6Button.raise_()
        self.slot1Button.raise_()
        self.slot2Button.raise_()
        self.slot7Button.raise_()
        self.slot0Button.raise_()
        self.slot4Button.raise_()
        self.slot3Button.raise_()
        self.slot8Button.raise_()
        self.slot9Button.raise_()
        self.slot5Button.raise_()
        self.smeltingTab = QWidget()
        self.smeltingTab.setObjectName(u"smeltingTab")
        self.smeltingInputButton = QPushButton(self.smeltingTab)
        self.smeltingInputButton.setObjectName(u"smeltingInputButton")
        self.smeltingInputButton.setGeometry(QRect(140, 90, 50, 50))
        self.smeltingInputButton.setFlat(True)
        self.smeltingOutputButton = QPushButton(self.smeltingTab)
        self.smeltingOutputButton.setObjectName(u"smeltingOutputButton")
        self.smeltingOutputButton.setGeometry(QRect(250, 90, 50, 50))
        self.smeltingOutputButton.setFlat(True)
        self.smeltingInput = QLabel(self.smeltingTab)
        self.smeltingInput.setObjectName(u"smeltingInput")
        self.smeltingInput.setGeometry(QRect(140, 90, 50, 50))
        self.smeltingOutput = QLabel(self.smeltingTab)
        self.smeltingOutput.setObjectName(u"smeltingOutput")
        self.smeltingOutput.setGeometry(QRect(250, 90, 50, 50))
        self.label = QLabel(self.smeltingTab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 160, 49, 16))
        self.smeltingModeBox = QComboBox(self.smeltingTab)
        self.smeltingModeBox.addItem("")
        self.smeltingModeBox.addItem("")
        self.smeltingModeBox.addItem("")
        self.smeltingModeBox.addItem("")
        self.smeltingModeBox.setObjectName(u"smeltingModeBox")
        self.smeltingModeBox.setGeometry(QRect(180, 160, 121, 22))
        self.recipeSubTabs.addTab(self.smeltingTab, "")
        self.smeltingInput.raise_()
        self.smeltingOutput.raise_()
        self.smeltingOutputButton.raise_()
        self.smeltingInputButton.raise_()
        self.label.raise_()
        self.smeltingModeBox.raise_()
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.stoneCuttingInputButton = QPushButton(self.tab_4)
        self.stoneCuttingInputButton.setObjectName(u"stoneCuttingInputButton")
        self.stoneCuttingInputButton.setGeometry(QRect(140, 90, 50, 50))
        self.stoneCuttingInputButton.setFlat(True)
        self.stoneCuttingInput = QLabel(self.tab_4)
        self.stoneCuttingInput.setObjectName(u"stoneCuttingInput")
        self.stoneCuttingInput.setGeometry(QRect(140, 90, 50, 50))
        self.stoneCuttingOutputButton = QPushButton(self.tab_4)
        self.stoneCuttingOutputButton.setObjectName(u"stoneCuttingOutputButton")
        self.stoneCuttingOutputButton.setGeometry(QRect(250, 90, 50, 50))
        self.stoneCuttingOutputButton.setFlat(True)
        self.stoneCuttingOutput = QLabel(self.tab_4)
        self.stoneCuttingOutput.setObjectName(u"stoneCuttingOutput")
        self.stoneCuttingOutput.setGeometry(QRect(250, 90, 50, 50))
        self.stoneCuttingCount = QSpinBox(self.tab_4)
        self.stoneCuttingCount.setObjectName(u"stoneCuttingCount")
        self.stoneCuttingCount.setGeometry(QRect(250, 140, 88, 24))
        self.stoneCuttingCount.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.stoneCuttingCount.setMinimum(1)
        self.stoneCuttingCount.setMaximum(64)
        self.recipeSubTabs.addTab(self.tab_4, "")
        self.stoneCuttingInput.raise_()
        self.stoneCuttingCount.raise_()
        self.stoneCuttingOutput.raise_()
        self.stoneCuttingOutputButton.raise_()
        self.stoneCuttingInputButton.raise_()

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.recipeSubTabs)

        self.recipeConfirmButton = QPushButton(self.recipeEditor)
        self.recipeConfirmButton.setObjectName(u"recipeConfirmButton")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.recipeConfirmButton)

        self.elementEditor.addWidget(self.recipeEditor)
        self.itemEditor = QWidget()
        self.itemEditor.setObjectName(u"itemEditor")
        self.itemModel = QComboBox(self.itemEditor)
        self.itemModel.addItem("")
        self.itemModel.addItem("")
        self.itemModel.addItem("")
        self.itemModel.setObjectName(u"itemModel")
        self.itemModel.setGeometry(QRect(420, 10, 121, 22))
        self.itemModelLabel = QLabel(self.itemEditor)
        self.itemModelLabel.setObjectName(u"itemModelLabel")
        self.itemModelLabel.setGeometry(QRect(370, 10, 49, 16))
        self.itemTextureLabel = QLabel(self.itemEditor)
        self.itemTextureLabel.setObjectName(u"itemTextureLabel")
        self.itemTextureLabel.setGeometry(QRect(370, 60, 49, 16))
        self.itemTextureButton = QPushButton(self.itemEditor)
        self.itemTextureButton.setObjectName(u"itemTextureButton")
        self.itemTextureButton.setGeometry(QRect(430, 40, 50, 50))
        self.itemTextureButton.setFlat(True)
        self.layoutWidget1 = QWidget(self.itemEditor)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 0, 311, 382))
        self.gridLayout_2 = QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)

        self.itemBaseItemLabel = QLabel(self.layoutWidget1)
        self.itemBaseItemLabel.setObjectName(u"itemBaseItemLabel")

        self.gridLayout_2.addWidget(self.itemBaseItemLabel, 2, 0, 1, 1)

        self.itemRightClickFunc = QPlainTextEdit(self.layoutWidget1)
        self.itemRightClickFunc.setObjectName(u"itemRightClickFunc")

        self.gridLayout_2.addWidget(self.itemRightClickFunc, 7, 0, 1, 2)

        self.itemRightClickCheck = QCheckBox(self.layoutWidget1)
        self.itemRightClickCheck.setObjectName(u"itemRightClickCheck")

        self.gridLayout_2.addWidget(self.itemRightClickCheck, 4, 1, 1, 1)

        self.itemDisplayName = QLineEdit(self.layoutWidget1)
        self.itemDisplayName.setObjectName(u"itemDisplayName")

        self.gridLayout_2.addWidget(self.itemDisplayName, 0, 1, 1, 1)

        self.label_5 = QLabel(self.layoutWidget1)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)

        self.itemBaseItem = QLineEdit(self.layoutWidget1)
        self.itemBaseItem.setObjectName(u"itemBaseItem")

        self.gridLayout_2.addWidget(self.itemBaseItem, 2, 1, 1, 1)

        self.itemName = QLineEdit(self.layoutWidget1)
        self.itemName.setObjectName(u"itemName")

        self.gridLayout_2.addWidget(self.itemName, 1, 1, 1, 1)

        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)

        self.itemStackSize = QSpinBox(self.layoutWidget1)
        self.itemStackSize.setObjectName(u"itemStackSize")
        self.itemStackSize.setMinimum(1)

        self.gridLayout_2.addWidget(self.itemStackSize, 3, 1, 1, 1)

        self.itemNameLabel = QLabel(self.layoutWidget1)
        self.itemNameLabel.setObjectName(u"itemNameLabel")

        self.gridLayout_2.addWidget(self.itemNameLabel, 1, 0, 1, 1)

        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)

        self.itemRightClickMode = QComboBox(self.layoutWidget1)
        self.itemRightClickMode.addItem("")
        self.itemRightClickMode.addItem("")
        self.itemRightClickMode.setObjectName(u"itemRightClickMode")

        self.gridLayout_2.addWidget(self.itemRightClickMode, 5, 1, 1, 1)

        self.itemDisplayNameLabel = QLabel(self.layoutWidget1)
        self.itemDisplayNameLabel.setObjectName(u"itemDisplayNameLabel")

        self.gridLayout_2.addWidget(self.itemDisplayNameLabel, 0, 0, 1, 1)

        self.itemConfirmButton = QPushButton(self.layoutWidget1)
        self.itemConfirmButton.setObjectName(u"itemConfirmButton")

        self.gridLayout_2.addWidget(self.itemConfirmButton, 8, 0, 1, 2)

        self.itemTexture = QLabel(self.itemEditor)
        self.itemTexture.setObjectName(u"itemTexture")
        self.itemTexture.setGeometry(QRect(430, 40, 50, 50))
        self.elementEditor.addWidget(self.itemEditor)
        self.itemTexture.raise_()
        self.itemModel.raise_()
        self.itemModelLabel.raise_()
        self.itemTextureLabel.raise_()
        self.itemTextureButton.raise_()
        self.layoutWidget1.raise_()
        self.paintingEditor = QWidget()
        self.paintingEditor.setObjectName(u"paintingEditor")
        self.paintingTextureButton = QPushButton(self.paintingEditor)
        self.paintingTextureButton.setObjectName(u"paintingTextureButton")
        self.paintingTextureButton.setGeometry(QRect(470, 10, 50, 50))
        self.paintingTextureButton.setFlat(True)
        self.paintingTextureLabel = QLabel(self.paintingEditor)
        self.paintingTextureLabel.setObjectName(u"paintingTextureLabel")
        self.paintingTextureLabel.setGeometry(QRect(410, 30, 58, 15))
        self.layoutWidget2 = QWidget(self.paintingEditor)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 0, 359, 190))
        self.gridLayout_3 = QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.paintingHeightLabel = QLabel(self.layoutWidget2)
        self.paintingHeightLabel.setObjectName(u"paintingHeightLabel")

        self.gridLayout_3.addWidget(self.paintingHeightLabel, 4, 0, 1, 1)

        self.paintingPlaceableLabel = QLabel(self.layoutWidget2)
        self.paintingPlaceableLabel.setObjectName(u"paintingPlaceableLabel")

        self.gridLayout_3.addWidget(self.paintingPlaceableLabel, 5, 0, 1, 1)

        self.paintingNameLabel = QLabel(self.layoutWidget2)
        self.paintingNameLabel.setObjectName(u"paintingNameLabel")

        self.gridLayout_3.addWidget(self.paintingNameLabel, 2, 0, 1, 1)

        self.paintingDisplayName = QLineEdit(self.layoutWidget2)
        self.paintingDisplayName.setObjectName(u"paintingDisplayName")

        self.gridLayout_3.addWidget(self.paintingDisplayName, 1, 1, 1, 1)

        self.paintingWidthLabel = QLabel(self.layoutWidget2)
        self.paintingWidthLabel.setObjectName(u"paintingWidthLabel")

        self.gridLayout_3.addWidget(self.paintingWidthLabel, 3, 0, 1, 1)

        self.paintingPlaceable = QCheckBox(self.layoutWidget2)
        self.paintingPlaceable.setObjectName(u"paintingPlaceable")
        self.paintingPlaceable.setChecked(True)

        self.gridLayout_3.addWidget(self.paintingPlaceable, 5, 1, 1, 1)

        self.paintingHeight = QSpinBox(self.layoutWidget2)
        self.paintingHeight.setObjectName(u"paintingHeight")
        self.paintingHeight.setMinimum(1)
        self.paintingHeight.setMaximum(16)

        self.gridLayout_3.addWidget(self.paintingHeight, 4, 1, 1, 1)

        self.paintingName = QLineEdit(self.layoutWidget2)
        self.paintingName.setObjectName(u"paintingName")

        self.gridLayout_3.addWidget(self.paintingName, 2, 1, 1, 1)

        self.label_8 = QLabel(self.layoutWidget2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 2)

        self.paintingDisplayNameLabel = QLabel(self.layoutWidget2)
        self.paintingDisplayNameLabel.setObjectName(u"paintingDisplayNameLabel")

        self.gridLayout_3.addWidget(self.paintingDisplayNameLabel, 1, 0, 1, 1)

        self.paintingWidth = QSpinBox(self.layoutWidget2)
        self.paintingWidth.setObjectName(u"paintingWidth")
        self.paintingWidth.setMinimum(1)
        self.paintingWidth.setMaximum(16)

        self.gridLayout_3.addWidget(self.paintingWidth, 3, 1, 1, 1)

        self.paintingConfirmButton = QPushButton(self.layoutWidget2)
        self.paintingConfirmButton.setObjectName(u"paintingConfirmButton")

        self.gridLayout_3.addWidget(self.paintingConfirmButton, 6, 0, 1, 2)

        self.paintingTexture = QLabel(self.paintingEditor)
        self.paintingTexture.setObjectName(u"paintingTexture")
        self.paintingTexture.setGeometry(QRect(470, 10, 50, 50))
        self.elementEditor.addWidget(self.paintingEditor)
        self.paintingTexture.raise_()
        self.paintingTextureButton.raise_()
        self.paintingTextureLabel.raise_()
        self.layoutWidget2.raise_()
        self.details = QWidget()
        self.details.setObjectName(u"details")
        self.formLayoutWidget = QWidget(self.details)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 0, 361, 281))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.packName = QLineEdit(self.formLayoutWidget)
        self.packName.setObjectName(u"packName")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.packName)

        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.packNamespace = QLineEdit(self.formLayoutWidget)
        self.packNamespace.setObjectName(u"packNamespace")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.packNamespace)

        self.label_9 = QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.label_9)

        self.packVersion = QComboBox(self.formLayoutWidget)
        self.packVersion.setObjectName(u"packVersion")

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.packVersion)

        self.label_10 = QLabel(self.formLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_10)

        self.label_11 = QLabel(self.formLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_11)

        self.packDescription = QLineEdit(self.formLayoutWidget)
        self.packDescription.setObjectName(u"packDescription")

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.packDescription)

        self.packAuthor = QLineEdit(self.formLayoutWidget)
        self.packAuthor.setObjectName(u"packAuthor")

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.packAuthor)

        self.packGenerate = QPushButton(self.formLayoutWidget)
        self.packGenerate.setObjectName(u"packGenerate")

        self.formLayout_3.setWidget(6, QFormLayout.SpanningRole, self.packGenerate)

        self.label_12 = QLabel(self.formLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        font1 = QFont()
        font1.setFamilies([u"JetBrains Mono"])
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(True)
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_3.setWidget(0, QFormLayout.SpanningRole, self.label_12)

        self.elementEditor.addWidget(self.details)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.elementEditor)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1003, 33))
        self.menuNew_Element = QMenu(self.menuBar)
        self.menuNew_Element.setObjectName(u"menuNew_Element")
        self.menuSave = QMenu(self.menuBar)
        self.menuSave.setObjectName(u"menuSave")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuSave.menuAction())
        self.menuBar.addAction(self.menuNew_Element.menuAction())
        self.menuNew_Element.addSeparator()
        self.menuNew_Element.addAction(self.actionBlock)
        self.menuNew_Element.addAction(self.actionItems)
        self.menuNew_Element.addAction(self.actionRecipie)
        self.menuNew_Element.addAction(self.actionPaintings)
        self.menuSave.addAction(self.actionSave)
        self.menuSave.addAction(self.actionLoad)
        self.menuSave.addAction(self.actionExport_Pack)

        self.retranslateUi(MainWindow)

        self.elementEditor.setCurrentIndex(0)
        self.recipeSubTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"mDirt - v3.0.0", None))
        self.actionBlock.setText(QCoreApplication.translate("MainWindow", u"Block", None))
        self.actionRecipie.setText(QCoreApplication.translate("MainWindow", u"Recipe", None))
        self.actionPaintings.setText(QCoreApplication.translate("MainWindow", u"Paintings", None))
        self.actionItems.setText(QCoreApplication.translate("MainWindow", u"Items", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionExport_Pack.setText(QCoreApplication.translate("MainWindow", u"Export Pack", None))
        ___qtreewidgetitem = self.elementVeiwer.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Element Viewer", None));
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><title>Welcome to mDirt</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'JetBrains Mono','Consolas','monospace'; font-size:13px; font-weight:400; font-style:normal;\" bgcolor=\"#1e1e1e\">\n"
"<h1 style=\" margin-top:18px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:xx-large; font-weight:700; color:#00e676;\">mDirt - A Minecraft Datapack Generator</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:xx-large; font-weight:700; color:#f0f0f0;\"> </span></h1>\n"
"<p style=\" margin-top:12px;"
                        " margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic; color:#aaaaaa;\">Making Datapacks is really tedious... but not anymore.</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Creating custom Minecraft datapacks can be time-consuming and complex. </span><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0;\">mDirt</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> simplifies this process by providing an easy-to-use tool for generating datapacks with custom features like blocks, items, recipes, and more. </span></p>\n"
"<h2 style=\" margin-top:0px; margin-bottom:12px; margin-left:0p"
                        "x; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#00e676;\">Supported Versions</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#f0f0f0;\"> </span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0;\">Minecraft Versions Supported:</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> 1.21.3, 1.21.4, 1.21.5 </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0;\">Full compatibility</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> "
                        "for </span><span style=\" font-family:'Courier New'; color:#ffeb3b; background-color:#2c2c2c;\">1.21.5</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> has been added. </span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:large; font-weight:700; color:#00e676;\">Using the Interface</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:large; font-weight:700; color:#f0f0f0;\"> </span></h3>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-weight:700;\">Tooltips:</span> Hover over any field for help. </li>\n"
"<li style=\" "
                        "font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\">Fill in details like block names, item properties, recipes, etc. </li>\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\">To get started, create a new element!</li></ul>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:large; font-weight:700; color:#00e676;\">Generate Your Datapack</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:large; font-weight:700; color:#f0f0f0;\"> </span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-"
                        "indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Click </span><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0;\">&quot;Generate Pack&quot;</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> once you're done. Your datapack will be ready to export! </span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:large; font-weight:700; color:#00e676;\">Deploying in Minecraft</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:large; font-weight:700; color:#f0f0f0;\"> </span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Place the datapack in </span><span style=\" f"
                        "ont-family:'Courier New'; color:#ffeb3b; background-color:#2c2c2c;\">datapacks</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> folder and the resourcepack in </span><span style=\" font-family:'Courier New'; color:#ffeb3b; background-color:#2c2c2c;\">resourcepacks</span><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Use the following commands to get your features: </span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\">Blocks: <span style=\" font-family:'Courier New'"
                        "; color:#ffeb3b; background-color:#2c2c2c;\">/function YOURNAMESPACE:give_blocks</span> </li>\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\">Items: <span style=\" font-family:'Courier New'; color:#ffeb3b; background-color:#2c2c2c;\">/function YOURNAMESPACE:give_items</span> </li>\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\">Paintings: <span style=\" font-family:'Courier New'; color:#ffeb3b; background-color:#2c2c2c;\">/function YOURNAMESPACE:give_paintings</span> </li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-wei"
                        "ght:700; color:#00e676;\">Feature Support by Version</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#f0f0f0;\"> </span></h2>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; border-collapse:collapse;\" cellspacing=\"2\" cellpadding=\"0\"><thead>\n"
"<tr>\n"
"<td bgcolor=\"#333333\" style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%; background-color:#333333;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0; backg"
                        "round-color:#333333;\">Feature</span></p></td>\n"
"<td bgcolor=\"#333333\" style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%; background-color:#333333;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0; background-color:#333333;\">1.21.3</span></p></td>\n"
"<td bgcolor=\"#333333\" style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-c"
                        "olor:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%; background-color:#333333;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0; background-color:#333333;\">1.21.4</span></p></td>\n"
"<td bgcolor=\"#333333\" style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%; background-color:#333333;\"><span style"
                        "=\" font-family:'Segoe UI','sans-serif'; font-weight:700; color:#f0f0f0; background-color:#333333;\">1.21.5</span></p></td></tr></thead>\n"
"<tr>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Blocks</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#4444"
                        "44; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td>\n"
"<td style=\" padding-left:0; p"
                        "adding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td></tr>\n"
"<tr>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; mar"
                        "gin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Items</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 80%</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444"
                        "444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 80%</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705"
                        " 80%</span></p></td></tr>\n"
"<tr>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Recipes</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
""
                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left"
                        ":1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td></tr>\n"
"<tr>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span"
                        " style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Paintings</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#e53935;\">\u274c</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; bo"
                        "rder-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#00e676;\">\u2705 100%</span></p></td></tr>\n"
"<tr>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bot"
                        "tom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Enchantments</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-"
                        "block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#e53935;\">\u274c</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#444444; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#e53935;\">\u274c</span></p></td>\n"
"<td style=\" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0; border-top:1px; border-right:1px; border-bottom:1px; border-left:1px; border-top-color:#444444; border-right-color:#444444; border-bottom-color:#444444; border-left-color:#44444"
                        "4; border-top-style:solid; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#e53935;\">\u274c</span></p></td></tr></table>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<h2 style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#00e676;\">Coming Soon</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#f0f0f0;\"> </span></h2>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-inden"
                        "t: 1;\">\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\">Custom Components for Items and Blocks </li>\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\">Support for Custom Enchantments </li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#00e676;\">Tips and Best Practices</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#f0f0f0;\"> </span></h2>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
""
                        "<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-weight:700;\">Namespaces:</span> Avoid clashes with other datapacks. </li>\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-weight:700;\">Testing:</span> Try it in a separate world first. </li>\n"
"<li style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-weight:700;\">Backups:</span> Always back up before applying new packs. </li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-inden"
                        "t:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#00e676;\">Credits</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#f0f0f0;\"> </span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Created by </span><a href=\"https://github.com/TheJupiterDev\"><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline; color:#4fc3f7;\">@TheJupiterDev</span></a><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> and </span><a href=\"https://github.com/JustJoshinDev\"><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline; color:#4fc3f7;\">@JustJoshinDev</span></a><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> </span></p>\n"
"<p style=\" margin-top:12px"
                        "; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">Special thanks to Admin for the custom block generation method. </span></p>\n"
"<h2 style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#00e676;\">Get Involved</span><span style=\" font-family:'Segoe UI','sans-serif'; font-size:x-large; font-weight:700; color:#f0f0f0;\"> </span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\">We welcome contributions and suggestions! <br />Found a bug? Have an idea? <br />Visit the </span><a href=\"https://github.com/JustJoshinDev/mDirt\"><span style=\" "
                        "font-family:'Segoe UI','sans-serif'; text-decoration: underline; color:#4fc3f7;\">GitHub Repository</span></a><span style=\" font-family:'Segoe UI','sans-serif'; color:#f0f0f0;\"> to file issues or open pull requests. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:160%;\"><span style=\" font-family:'Segoe UI','sans-serif'; color:#aaaaaa;\">\u00a9 2025 mDirt Project. Minecraft is a trademark of Mojang Studios. </span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.blockTextureButtonBottom.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The bottom texture of your block. <span style=\" font-weight:700;\">If you are using a Custom model, only use this texture!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockTextureButtonBottom.setText("")
#if QT_CONFIG(tooltip)
        self.blockTextureButtonTop.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The top texture of your block. <span style=\" font-weight:700;\">If you are using a Custom model, only use the bottom texture!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockTextureButtonTop.setText("")
#if QT_CONFIG(tooltip)
        self.blockTextureButtonLeft.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The left texture of your block. <span style=\" font-weight:700;\">If you are using a Custom model, only use the bottom texture!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockTextureButtonLeft.setText("")
#if QT_CONFIG(tooltip)
        self.blockTextureButtonBack.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The back texture of your block. <span style=\" font-weight:700;\">If you are using a Custom model, only use the bottom texture!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockTextureButtonBack.setText("")
#if QT_CONFIG(tooltip)
        self.blockTextureButtonFront.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The front texture of your block. <span style=\" font-weight:700;\">If you are using a Custom model, only use the bottom texture!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockTextureButtonFront.setText("")
#if QT_CONFIG(tooltip)
        self.blockTextureButtonRight.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The right texture of your block. <span style=\" font-weight:700;\">If you are using a Custom model, only use the bottom texture!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockTextureButtonRight.setText("")
        self.blockTextureLabel.setText(QCoreApplication.translate("MainWindow", u"Texture:", None))
#if QT_CONFIG(tooltip)
        self.blockDirectional.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>When this is checked, it'll place like an oak log, directionally.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockDirectional.setText("")
        self.blockModel.setItemText(0, QCoreApplication.translate("MainWindow", u"Block", None))
        self.blockModel.setItemText(1, QCoreApplication.translate("MainWindow", u"Custom", None))

#if QT_CONFIG(tooltip)
        self.blockModel.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The model of your block.</p><p>Block: A normal block.</p><p>Custom: A model you created in <span style=\" font-weight:700;\">BlockBench</span>.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockPlaceSoundLabel.setText(QCoreApplication.translate("MainWindow", u"Place Sound", None))
        self.blockDropLabel.setText(QCoreApplication.translate("MainWindow", u"Drop", None))
#if QT_CONFIG(tooltip)
        self.blockBaseBlock.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The block that your custom block hides inside of. This determines most of the sounds (other than the place sound), mining speed, etc. <span style=\" font-weight:700;\">Do not use minecraft: in front of the block!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockBaseBlock.setPlaceholderText(QCoreApplication.translate("MainWindow", u"stone", None))
#if QT_CONFIG(tooltip)
        self.blockDisplayName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The name you'll see for your block in your inventory!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockDisplayName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ruby Ore", None))
        self.blockDirectionalLabel.setText(QCoreApplication.translate("MainWindow", u"Directional", None))
#if QT_CONFIG(tooltip)
        self.blockPlaceSound.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>When this is checked, it'll place like an oak log, directionally.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockPlaceSound.setPlaceholderText(QCoreApplication.translate("MainWindow", u"block.stone.place", None))
#if QT_CONFIG(tooltip)
        self.blockDropBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The item or block that this block drops when it is broken. Self will drop itself, or you can choose any of your blocks or items, or you can choose any Minecraft block or item.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockModelLabel.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.blockNameLabel.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.blockDisplayNameLabel.setText(QCoreApplication.translate("MainWindow", u"Display Name", None))
#if QT_CONFIG(tooltip)
        self.blockName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>How the game refers to the block.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.blockName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ruby_ore", None))
        self.blockBaseBlockName.setText(QCoreApplication.translate("MainWindow", u"Base Block", None))
        self.blockConfirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm Block", None))
        self.blockTextureLabelLeft.setText("")
        self.blockTextureLabelBottom.setText("")
        self.blockTextureLabelBack.setText("")
        self.blockTextureLabelTop.setText("")
        self.blockTextureLabelRight.setText("")
        self.blockTextureLabelFront.setText("")
        self.recipeNameLabel.setText(QCoreApplication.translate("MainWindow", u"Recipe Name", None))
#if QT_CONFIG(tooltip)
        self.recipeName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The name the game uses to recognize your recipe.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slot0Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot0Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot1Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot1Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot2Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot2Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot3Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot3Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot4Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot4Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot5Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot5Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot6Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot6Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot7Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot7Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot8Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A slot representing a crafting table slot!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot8Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot9Button.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The output of the crafting recipe. Can have any Minecraft block or item, as well as any custom blocks or items.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.slot9Button.setText("")
#if QT_CONFIG(tooltip)
        self.slot9Count.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The amount of your output. If this is higher than the max stack size of your output item, your datapack will crash!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.shapelessRadio.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Makes the recipe shapeless.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.shapelessRadio.setText(QCoreApplication.translate("MainWindow", u"Shapeless", None))
#if QT_CONFIG(tooltip)
        self.exactlyRadio.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Makes the recipe normal.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.exactlyRadio.setText(QCoreApplication.translate("MainWindow", u"Exactly Where Placed", None))
        self.slot0.setText("")
        self.slot1.setText("")
        self.slot2.setText("")
        self.slot3.setText("")
        self.slot4.setText("")
        self.slot5.setText("")
        self.slot6.setText("")
        self.slot7.setText("")
        self.slot8.setText("")
        self.slot9.setText("")
        self.recipeSubTabs.setTabText(self.recipeSubTabs.indexOf(self.craftingTab), QCoreApplication.translate("MainWindow", u"Crafting", None))
#if QT_CONFIG(tooltip)
        self.smeltingInputButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The input for the smelting recipe.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.smeltingInputButton.setText("")
#if QT_CONFIG(tooltip)
        self.smeltingOutputButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The output for the smelting recipe.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.smeltingOutputButton.setText("")
        self.smeltingInput.setText("")
        self.smeltingOutput.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.smeltingModeBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Smelting", None))
        self.smeltingModeBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Smoking", None))
        self.smeltingModeBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Blasting", None))
        self.smeltingModeBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Campfire_Cooking", None))

#if QT_CONFIG(tooltip)
        self.smeltingModeBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The block that this recipe is assigned to. For example, Campfire_Cooking will make it so this recipe is for a campfire.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.recipeSubTabs.setTabText(self.recipeSubTabs.indexOf(self.smeltingTab), QCoreApplication.translate("MainWindow", u"Smelting", None))
        self.stoneCuttingInputButton.setText("")
#if QT_CONFIG(tooltip)
        self.stoneCuttingInput.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Input for a stonecutting recipe.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.stoneCuttingInput.setText("")
        self.stoneCuttingOutputButton.setText("")
#if QT_CONFIG(tooltip)
        self.stoneCuttingOutput.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Output for the stonecutting recipe.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.stoneCuttingOutput.setText("")
#if QT_CONFIG(tooltip)
        self.stoneCuttingCount.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The amount of your stonecutting output. If this is higher than the max stack size of your output item, your datapack will crash!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.recipeSubTabs.setTabText(self.recipeSubTabs.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Stonecutting", None))
        self.recipeConfirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm Recipe", None))
        self.itemModel.setItemText(0, QCoreApplication.translate("MainWindow", u"Generated", None))
        self.itemModel.setItemText(1, QCoreApplication.translate("MainWindow", u"Handheld", None))
        self.itemModel.setItemText(2, QCoreApplication.translate("MainWindow", u"Custom", None))

#if QT_CONFIG(tooltip)
        self.itemModel.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The model your custom item will use.</p><p>Generated: Normal items.</p><p>Handheld: For thigns such as tools, swords, etc.</p><p>Custom: If you want to select a custom model you made in <span style=\" font-weight:700;\">BlockBench</span>.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemModelLabel.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.itemTextureLabel.setText(QCoreApplication.translate("MainWindow", u"Texture", None))
#if QT_CONFIG(tooltip)
        self.itemTextureButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The texture of your item!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemTextureButton.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Right-Click Mode", None))
        self.itemBaseItemLabel.setText(QCoreApplication.translate("MainWindow", u"Base Item", None))
#if QT_CONFIG(tooltip)
        self.itemRightClickFunc.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>A list of commands that will be run whenever you rightclick. <span style=\" font-weight:700;\">The program does not check if this will work or not! Any problems made here are the fault of the user.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.itemRightClickCheck.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Whether or not you want to have a set of special commands run whenever you rightclick your item.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemRightClickCheck.setText("")
#if QT_CONFIG(tooltip)
        self.itemDisplayName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The name of your custom item! This'll be what you see in your inventory.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemDisplayName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ruby", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Right-Click Function", None))
#if QT_CONFIG(tooltip)
        self.itemBaseItem.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The Minecraft item your custom item is wrapped around. <span style=\" font-weight:700;\">Do not add a minecraft: prefix to this item!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemBaseItem.setPlaceholderText(QCoreApplication.translate("MainWindow", u"flint", None))
#if QT_CONFIG(tooltip)
        self.itemName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The name of your item that the game recognizes it as.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ruby", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Max Stack Size", None))
#if QT_CONFIG(tooltip)
        self.itemStackSize.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The stack size of your item! Can be anything from 1 to 99, and can be used for any base item!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemNameLabel.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Right-Click Function?", None))
        self.itemRightClickMode.setItemText(0, QCoreApplication.translate("MainWindow", u"Tick", None))
        self.itemRightClickMode.setItemText(1, QCoreApplication.translate("MainWindow", u"Impulse", None))

#if QT_CONFIG(tooltip)
        self.itemRightClickMode.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The mode of the right-click method.</p><p>Tick: The function runs 20 times per second as long as you are holding rightclick.<br/>Impulse: Runs once whenever you rightclick your item.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.itemDisplayNameLabel.setText(QCoreApplication.translate("MainWindow", u"Display Name", None))
        self.itemConfirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm Item", None))
        self.itemTexture.setText("")
#if QT_CONFIG(tooltip)
        self.paintingTextureButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The texture of your painting!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.paintingTextureButton.setText("")
        self.paintingTextureLabel.setText(QCoreApplication.translate("MainWindow", u"Texture", None))
        self.paintingHeightLabel.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.paintingPlaceableLabel.setText(QCoreApplication.translate("MainWindow", u"Accessible in Survival?", None))
        self.paintingNameLabel.setText(QCoreApplication.translate("MainWindow", u"Name", None))
#if QT_CONFIG(tooltip)
        self.paintingDisplayName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The name of the painting your game recognizes.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.paintingDisplayName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Shrek Painting", None))
        self.paintingWidthLabel.setText(QCoreApplication.translate("MainWindow", u"Width", None))
#if QT_CONFIG(tooltip)
        self.paintingPlaceable.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Whether or not you can use the painting in Survival mode. Should almost always be True.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.paintingPlaceable.setText("")
#if QT_CONFIG(tooltip)
        self.paintingHeight.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The height in blocks your painting will be.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.paintingName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The name of the painting your game recognizes.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.paintingName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"shrek_painting", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"WARNING: Minecraft marks Paintings as EXPERIMENTAL!", None))
        self.paintingDisplayNameLabel.setText(QCoreApplication.translate("MainWindow", u"Display Name", None))
#if QT_CONFIG(tooltip)
        self.paintingWidth.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The width in blocks your painting will be.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.paintingConfirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm Painting", None))
        self.paintingTexture.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
#if QT_CONFIG(tooltip)
        self.packName.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The name of your data and resource pack!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"The Ruby Pack", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Namespace:", None))
#if QT_CONFIG(tooltip)
        self.packNamespace.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The namespace of your pack.</p><p><span style=\" font-weight:700;\">Only lowercase and underscores. NO spaces.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packNamespace.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ruby_pack", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Version:", None))
#if QT_CONFIG(tooltip)
        self.packVersion.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The version of Minecraft your pack will be made for.</p><p><span style=\" font-weight:700;\">If you select 1.21.3, paintings will be skipped and NOT generated!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packVersion.setPlaceholderText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Description:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Author:", None))
#if QT_CONFIG(tooltip)
        self.packDescription.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The description of your pack that displays when enabling the resource/data packs.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packDescription.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Adds Rubies, Ruby Blocks, and more!", None))
#if QT_CONFIG(tooltip)
        self.packAuthor.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>You're name, or you're <span style=\" font-style:italic;\">online</span> name.</p><p><span style=\" font-weight:700;\">Only lowercase and underscores. NO spaces.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packAuthor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"jupiterdev", None))
#if QT_CONFIG(tooltip)
        self.packGenerate.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Click once you have filled in the other details, and it will generate the packs!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Pack Details", None))
        self.menuNew_Element.setTitle(QCoreApplication.translate("MainWindow", u"New Element", None))
        self.menuSave.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

