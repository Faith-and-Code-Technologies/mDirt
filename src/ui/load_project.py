# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_projectRJAgvl.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QTextBrowser,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(493, 510)
        Form.setStyleSheet(
            "/*mDirt Dev Theme - Dark Earthy */\n"
            "\n"
            "* {\n"
            '    font-family: "JetBrains Mono", "Consolas", monospace;\n'
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
            "}"
        )
        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setGeometry(QRect(120, 20, 261, 51))
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setGeometry(QRect(120, 80, 261, 331))
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QRect(110, 420, 271, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.textBrowser.setHtml(
            QCoreApplication.translate(
                "Form",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "hr { height: 1px; border-width: 0; }\n"
                'li.unchecked::marker { content: "\\2610"; }\n'
                'li.checked::marker { content: "\\2612"; }\n'
                "</style></head><body style=\" font-family:'JetBrains Mono','Consolas','monospace'; font-size:13px; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:18pt; font-weight:700;">Load mDirt Project</span></p></body></html>',
                None,
            )
        )
        self.pushButton.setText(
            QCoreApplication.translate("Form", "Load Project", None)
        )

    # retranslateUi
