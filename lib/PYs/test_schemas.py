import sys
import json
from PySide6.QtWidgets import QApplication, QPushButton, QLayout
from koreui import load_schema, JsonSchemaForm

if __name__ == "__main__":
    app = QApplication(sys.argv)

    schema = load_schema("src/generation/v1_21_4/schemas/enchantment.json")

    with open('lib/1.21.4_data.json', 'r') as f:
        data = json.load(f)

    form = JsonSchemaForm(schema, "Enchantment")
    form.show()

    sys.exit(app.exec())
