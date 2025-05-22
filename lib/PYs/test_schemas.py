import sys
import json
from PySide6.QtWidgets import QApplication, QPushButton, QLayout
from jsontoqt import JsonForm, load_json_schema

if __name__ == "__main__":
    app = QApplication(sys.argv)

    schema = load_json_schema("src/generation/v1_21_4/schemas/enchantment.json")

    with open('lib/1.21.4_data.json', 'r') as f:
        data = json.load(f)

    builder = JsonForm(schema, data)
    form = builder.build_form()
    form.show()

    def on_submit():
        print(json.dumps(builder.get_form_data(), indent=2))

    submit_btn = QPushButton("Submit")
    submit_btn.clicked.connect(on_submit)
    form.layout().addWidget(submit_btn)

    sys.exit(app.exec())
