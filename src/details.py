# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'detailsvIhPGD.ui'
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
#if QT_CONFIG(tooltip)
        self.packGenerate.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Sets the details!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packGenerate.setText(QCoreApplication.translate("Form", u"OK", None))
        self.packNameLabel.setText(QCoreApplication.translate("Form", u"Pack Name", None))
#if QT_CONFIG(tooltip)
        self.packName.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>The name of your Data &amp; Resource packs!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packName.setPlaceholderText(QCoreApplication.translate("Form", u"The Ruby Pack", None))
        self.packNamespaceLabel.setText(QCoreApplication.translate("Form", u"Namespace", None))
#if QT_CONFIG(tooltip)
        self.packNamespace.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>The namespace for your packs. This is what the game uses to recognize your packs.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packNamespace.setPlaceholderText(QCoreApplication.translate("Form", u"rubypack", None))
        self.packAuthorLabel.setText(QCoreApplication.translate("Form", u"Author", None))
#if QT_CONFIG(whatsthis)
        self.packAuthor.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p>You!</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.packAuthor.setPlaceholderText(QCoreApplication.translate("Form", u"jupiterdev", None))
        self.packDescriptionLabel.setText(QCoreApplication.translate("Form", u"Description", None))
#if QT_CONFIG(tooltip)
        self.packDescription.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>The description for your packs!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packDescription.setPlaceholderText(QCoreApplication.translate("Form", u"Adds Rubys, Ruby Blocks, etc.", None))
        self.packCMDPrefixLabel.setText(QCoreApplication.translate("Form", u"CMD Prefix", None))
#if QT_CONFIG(tooltip)
        self.packCMDPrefix.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:700;\">LEGACY! Only used in 1.21.3. </span><span style=\" font-style:italic;\">Note that you still must fill it in!</span><br/>A 3 digit number used to figure out the Custom Model Data for your custom blocks &amp; items.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.packCMDPrefix.setPlaceholderText(QCoreApplication.translate("Form", u"589", None))
        self.packVersionLabel.setText(QCoreApplication.translate("Form", u"Version", None))
#if QT_CONFIG(tooltip)
        self.packVersion.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>The version your packs will work for.<br/><span style=\" font-weight:700;\">1.21.4 highly recommended!</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.titleLabel.setText(QCoreApplication.translate("Form", u"mDirt - a tool made to help make Datapacks\n"
"Created By JupiterDev & JustJoshinDev 2025", None))
    # retranslateUi

