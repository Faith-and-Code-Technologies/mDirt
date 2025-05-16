from PySide6.QtWidgets import QMessageBox

def alert(message, type_='information'):
    messageBox = QMessageBox()
    if type_ == 'information':
        messageBox.setIcon(QMessageBox.Icon.Information)
    elif type_ == 'warning':
        messageBox.setIcon(QMessageBox.Icon.Warning)
    elif type_ == 'critical':
        messageBox.setIcon(QMessageBox.Icon.Critical)
    messageBox.setText(message)
    messageBox.setWindowTitle("mDirt Alert")
    messageBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    messageBox.exec()
