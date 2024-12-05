# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'detailsNezKbS.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(337, 346)
        self.packGenerate = QPushButton(Form)
        self.packGenerate.setObjectName(u"packGenerate")
        self.packGenerate.setGeometry(QRect(40, 250, 271, 31))
        self.formLayoutWidget = QWidget(Form)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(40, 70, 271, 171))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.packNameLabel = QLabel(self.formLayoutWidget)
        self.packNameLabel.setObjectName(u"packNameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.packNameLabel)

        self.packName = QLineEdit(self.formLayoutWidget)
        self.packName.setObjectName(u"packName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.packName)

        self.packNamespaceLabel = QLabel(self.formLayoutWidget)
        self.packNamespaceLabel.setObjectName(u"packNamespaceLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.packNamespaceLabel)

        self.packNamespace = QLineEdit(self.formLayoutWidget)
        self.packNamespace.setObjectName(u"packNamespace")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.packNamespace)

        self.packAuthorLabel = QLabel(self.formLayoutWidget)
        self.packAuthorLabel.setObjectName(u"packAuthorLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.packAuthorLabel)

        self.packAuthor = QLineEdit(self.formLayoutWidget)
        self.packAuthor.setObjectName(u"packAuthor")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.packAuthor)

        self.packDescriptionLabel = QLabel(self.formLayoutWidget)
        self.packDescriptionLabel.setObjectName(u"packDescriptionLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.packDescriptionLabel)

        self.packDescription = QLineEdit(self.formLayoutWidget)
        self.packDescription.setObjectName(u"packDescription")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.packDescription)

        self.packCMDPrefixLabel = QLabel(self.formLayoutWidget)
        self.packCMDPrefixLabel.setObjectName(u"packCMDPrefixLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.packCMDPrefixLabel)

        self.packCMDPrefix = QLineEdit(self.formLayoutWidget)
        self.packCMDPrefix.setObjectName(u"packCMDPrefix")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.packCMDPrefix)

        self.packVersionLabel = QLabel(self.formLayoutWidget)
        self.packVersionLabel.setObjectName(u"packVersionLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.packVersionLabel)

        self.packVersion = QComboBox(self.formLayoutWidget)
        self.packVersion.addItem("")
        self.packVersion.addItem("")
        self.packVersion.setObjectName(u"packVersion")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.packVersion)

        self.titleLabel = QLabel(Form)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setGeometry(QRect(40, 10, 271, 51))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Datapack Details", None))
        self.packGenerate.setText(QCoreApplication.translate("Form", u"OK", None))
        self.packNameLabel.setText(QCoreApplication.translate("Form", u"Pack Name", None))
        self.packName.setPlaceholderText(QCoreApplication.translate("Form", u"The Ruby Pack", None))
        self.packNamespaceLabel.setText(QCoreApplication.translate("Form", u"Namespace", None))
        self.packNamespace.setPlaceholderText(QCoreApplication.translate("Form", u"rubypack", None))
        self.packAuthorLabel.setText(QCoreApplication.translate("Form", u"Author", None))
        self.packAuthor.setPlaceholderText(QCoreApplication.translate("Form", u"jupiterdev", None))
        self.packDescriptionLabel.setText(QCoreApplication.translate("Form", u"Description", None))
        self.packDescription.setPlaceholderText(QCoreApplication.translate("Form", u"Adds Rubys, Ruby Blocks, etc.", None))
        self.packCMDPrefixLabel.setText(QCoreApplication.translate("Form", u"CMD Prefix", None))
        self.packCMDPrefix.setPlaceholderText(QCoreApplication.translate("Form", u"589", None))
        self.packVersionLabel.setText(QCoreApplication.translate("Form", u"Version", None))
        self.packVersion.setItemText(0, QCoreApplication.translate("Form", u"1.21.3", None))
        self.packVersion.setItemText(1, QCoreApplication.translate("Form", u"1.21.4", None))

        self.titleLabel.setText(QCoreApplication.translate("Form", u"mDirt - a tool made to help make Datapacks\n"
"Created By JupiterDev & JustJoshinDev 2024", None))
    # retranslateUi

