import sys
import json
from PySide6.QtWidgets import QApplication
from koreui import load_schema, JsonSchemaForm

if __name__ == "__main__":
    app = QApplication(sys.argv)

    schema = load_schema("src/generation/v1_21_4/schemas/data_component.json")

    with open('lib/1.21.4_data.json', 'r') as f:
        datas = json.load(f)

    form = JsonSchemaForm(schema, data=datas, title="Enchantment", toolbar=True)
    form.show()

    sys.exit(app.exec())
