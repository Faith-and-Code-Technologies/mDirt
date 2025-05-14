from PySide6.QtWidgets import (
    QLineEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QLabel,
    QCheckBox,
    QTreeWidget,
)


class FieldResetter:
    def clear_line_edits(*fields: QLineEdit):
        for field in fields:
            field.setText("")

    def clear_text_edits(*fields: QTextEdit):
        for field in fields:
            field.clear()

    def reset_combo_boxes(*boxes: QComboBox, default_text=""):
        for box in boxes:
            box.setCurrentText(default_text)

    def reset_spin_boxes(*boxes: QSpinBox, default_value=0):
        for box in boxes:
            box.setValue(default_value)

    def clear_labels(*labels: QLabel):
        for label in labels:
            label.clear()

    def uncheck_boxes(*boxes: QCheckBox):
        for box in boxes:
            box.setChecked(False)

    def clear_tree_selection(*trees: QTreeWidget):
        for tree in trees:
            tree.clearSelection()
