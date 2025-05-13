from PySide6.QtWidgets import QLineEdit, QMessageBox

class FieldValidator:
    def validate_text_field(field: QLineEdit, allowed_chars: str, field_name: str) -> bool:
        text = field.text()

        if not text:
            field.setStyleSheet("QLineEdit { border: 1px solid red; }")
            FieldValidator._alert(f"Please fill in all fields! ({field_name})")
            return False

        if any(c not in allowed_chars for c in text):
            field.setStyleSheet("QLineEdit { border: 1px solid red; }")
            FieldValidator._alert(f"{field_name} contains illegal characters!")
            return False

        field.setStyleSheet("")
        return True

    def validate_dropdown_selection(field: QLineEdit, options: list[str], field_name: str) -> bool:
        value = field.text()
        if value not in options:
            field.setStyleSheet("QLineEdit { border: 1px solid red; }")
            FieldValidator._alert(f"{field_name} must be one of the allowed values.")
            return False

        field.setStyleSheet("")
        return True

    def validate_non_null(value, field_name: str) -> bool:
        if value is None or value == "":
            FieldValidator._alert(f"Please select a valid value for {field_name}!")
            return False
        return True

    def _alert(message: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Validation Error")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
