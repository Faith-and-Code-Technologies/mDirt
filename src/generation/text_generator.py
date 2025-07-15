import json
from PySide6.QtGui import QTextCharFormat, QTextCursor, QFont, QColor
from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton, QColorDialog, QApplication


class TextGenerator:
    def __init__(self, ui, obfuscate_property, minecraft_colors):
        self.ui = ui
        self.OBFUSCATE_PROPERTY = obfuscate_property
        self.MINECRAFT_COLORS = minecraft_colors

    def tg_MergeFormat(self, fmt: QTextCharFormat):
        cursor = self.ui.textGeneratorTextBox.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.ui.textGeneratorTextBox.mergeCurrentCharFormat(fmt)

    def tg_ToggleBold(self):
        fmt = QTextCharFormat()
        current = self.ui.textGeneratorTextBox.currentCharFormat().fontWeight()
        fmt.setFontWeight(QFont.Normal if current > QFont.Normal else QFont.Bold)
        self.tg_MergeFormat(fmt)

    def tg_ToggleItalic(self):
        fmt = QTextCharFormat()
        current = self.ui.textGeneratorTextBox.currentCharFormat().fontItalic()
        fmt.setFontItalic(not current)
        self.tg_MergeFormat(fmt)

    def tg_ToggleUnderline(self):
        fmt = QTextCharFormat()
        current = self.ui.textGeneratorTextBox.currentCharFormat().fontUnderline()
        fmt.setFontUnderline(not current)
        self.tg_MergeFormat(fmt)

    def tg_ToggleStrikethrough(self):
        fmt = QTextCharFormat()
        current = self.ui.textGeneratorTextBox.currentCharFormat().fontStrikeOut()
        fmt.setFontStrikeOut(not current)
        self.tg_MergeFormat(fmt)

    def tg_ToggleObfuscate(self):
        cursor = self.ui.textGeneratorTextBox.textCursor()
        if not cursor.hasSelection():
            return

        start_pos = cursor.selectionStart()
        end_pos = cursor.selectionEnd()
        
        cursor.setPosition(start_pos)
        cursor.setPosition(start_pos + 1, QTextCursor.KeepAnchor)
        
        is_obfuscated = False
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            is_obfuscated = bool(fmt.property(self.OBFUSCATE_PROPERTY))
        
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        
        if is_obfuscated:
            doc = self.ui.textGeneratorTextBox.document()
            fragments_to_restore = []
            
            pos = start_pos
            while pos < end_pos:
                cursor.setPosition(pos)
                cursor.setPosition(pos + 1, QTextCursor.KeepAnchor)
                if cursor.hasSelection():
                    fmt = cursor.charFormat()
                    if fmt.property(self.OBFUSCATE_PROPERTY):
                        stored_text = fmt.property(self.OBFUSCATE_PROPERTY + 1)
                        if stored_text:
                            fragments_to_restore.append((pos, pos + 1, stored_text))
                    pos += 1
                else:
                    break
            
            for start, end, original_text in reversed(fragments_to_restore):
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.KeepAnchor)
                
                new_fmt = QTextCharFormat(cursor.charFormat())
                new_fmt.setProperty(self.OBFUSCATE_PROPERTY, False)
                new_fmt.setProperty(self.OBFUSCATE_PROPERTY + 1, None)
                
                cursor.insertText(original_text, new_fmt)
        else:
            selected_text = cursor.selectedText()
            cursor.removeSelectedText()
            
            for i, char in enumerate(selected_text):
                display_char = '█' if not char.isspace() else char
                
                fmt = QTextCharFormat(cursor.charFormat())
                fmt.setProperty(self.OBFUSCATE_PROPERTY, True)
                fmt.setProperty(self.OBFUSCATE_PROPERTY + 1, char)
                
                cursor.insertText(display_char, fmt)

    def tg_Color(self, checked=False, parent_widget=None):
        dialog = QDialog(parent_widget)
        dialog.setWindowTitle("Pick a Color")
        layout = QGridLayout(dialog)

        for i, (name, hexcode) in enumerate(self.MINECRAFT_COLORS):
            btn = QPushButton(name)
            btn.setStyleSheet(f"background-color: {hexcode}; color: black;")
            btn.clicked.connect(lambda _, color=hexcode: self.tg_ApplyColor(color, dialog))
            layout.addWidget(btn, i // 4, i % 4)

        custom_btn = QPushButton("Custom Color...")
        custom_btn.clicked.connect(lambda: self.tg_OpenColorPicker(dialog))
        layout.addWidget(custom_btn, len(self.MINECRAFT_COLORS) // 4 + 1, 0, 1, 4)

        dialog.setLayout(layout)
        dialog.exec()

    def tg_ApplyColor(self, hexcode, dialog=None):
        cursor = self.ui.textGeneratorTextBox.textCursor()
        if cursor.hasSelection():
            color = QColor(hexcode)
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            cursor.mergeCharFormat(fmt)

        if dialog:
            dialog.accept()

    def tg_OpenColorPicker(self, dialog=None):
        color = QColorDialog.getColor()
        if color.isValid():
            self.tg_ApplyColor(color.name(), dialog)

    def tg_UpdateTextComponentOutput(self):
        doc = self.ui.textGeneratorTextBox.document()
        output = [""]

        block = doc.begin()
        default_colors = {"#000000", "#ffffff"}

        while block.isValid():
            it = block.begin()
            while not it.atEnd():
                frag = it.fragment()
                if frag.isValid():
                    fmt = frag.charFormat()
                    
                    text = frag.text()
                    if fmt.property(self.OBFUSCATE_PROPERTY):
                        original_text = fmt.property(self.OBFUSCATE_PROPERTY + 1)
                        if original_text:
                            text = original_text

                    if text == "":
                        it += 1
                        continue

                    component = {"text": text}

                    if fmt.fontWeight() > QFont.Normal:
                        component["bold"] = True
                        
                    if fmt.fontItalic():
                        component["italic"] = True
                        
                    if fmt.fontUnderline():
                        component["underlined"] = True
                        
                    if fmt.fontStrikeOut():
                        component["strikethrough"] = True
                        
                    if bool(fmt.property(self.OBFUSCATE_PROPERTY)):
                        component["obfuscated"] = True

                    color = fmt.foreground().color()
                    if color.isValid():
                        hex_color = color.name()
                        if hex_color not in default_colors:
                            component["color"] = hex_color

                    output.append(component)
                it += 1

            if block.next().isValid():
                output.append({"text": "\n"})
            block = block.next()

        json_str = json.dumps(output, separators=(",", ":"))

        if self.ui.textGeneratorType.currentText() == "Raw JSON":
            output_string = json_str
        elif self.ui.textGeneratorType.currentText() == "Tellraw Command":
            output_string = "/tellraw @a " + json_str
        elif self.ui.textGeneratorType.currentText() == "Title":
            output_string = "/title @a title " + json_str
        elif self.ui.textGeneratorType.currentText() == "Subtitle":
            output_string = "/title @a subtitle " + json_str
        elif self.ui.textGeneratorType.currentText() == "Actionbar":
            output_string = "/title @a actionbar " + json_str
        elif self.ui.textGeneratorType.currentText() == "MOTD":
            output_string = self.tg_ConvertToMOTD()
        else:
            output_string = json_str

        self.ui.textGeneratorOutput.setText(output_string)

    def tg_ConvertToMOTD(self):
        doc = self.ui.textGeneratorTextBox.document()
        motd_text = ""
        
        color_codes = {
            "#000000": "&0",  # Black
            "#0000aa": "&1",  # Dark Blue
            "#00aa00": "&2",  # Dark Green
            "#00aaaa": "&3",  # Dark Aqua
            "#aa0000": "&4",  # Dark Red
            "#aa00aa": "&5",  # Dark Purple
            "#ffaa00": "&6",  # Gold
            "#aaaaaa": "&7",  # Gray
            "#555555": "&8",  # Dark Gray
            "#5555ff": "&9",  # Blue
            "#55ff55": "&a",  # Green
            "#55ffff": "&b",  # Aqua
            "#ff5555": "&c",  # Red
            "#ff55ff": "&d",  # Light Purple
            "#ffff55": "&e",  # Yellow
            "#ffffff": "&f",  # White
        }
        
        block = doc.begin()
        current_color = None
        current_bold = False
        current_italic = False
        current_underline = False
        current_strikethrough = False
        current_obfuscated = False
        
        while block.isValid():
            it = block.begin()
            while not it.atEnd():
                frag = it.fragment()
                if frag.isValid():
                    fmt = frag.charFormat()
                    
                    text = frag.text()
                    if fmt.property(self.OBFUSCATE_PROPERTY):
                        original_text = fmt.property(self.OBFUSCATE_PROPERTY + 1)
                        if original_text:
                            text = original_text
                    
                    if text == "":
                        it += 1
                        continue
                    
                    color = fmt.foreground().color()
                    hex_color = color.name().lower() if color.isValid() else None
                    bold = fmt.fontWeight() > QFont.Normal
                    italic = fmt.fontItalic()
                    underline = fmt.fontUnderline()
                    strikethrough = fmt.fontStrikeOut()
                    obfuscated = bool(fmt.property(self.OBFUSCATE_PROPERTY))
                    
                    if hex_color != current_color:
                        if hex_color in color_codes:
                            motd_text += color_codes[hex_color]
                        current_color = hex_color
                        current_bold = False
                        current_italic = False
                        current_underline = False
                        current_strikethrough = False
                        current_obfuscated = False
                    
                    if bold and not current_bold:
                        motd_text += "&l"
                        current_bold = True
                    if italic and not current_italic:
                        motd_text += "&o"
                        current_italic = True
                    if underline and not current_underline:
                        motd_text += "&n"
                        current_underline = True
                    if strikethrough and not current_strikethrough:
                        motd_text += "&m"
                        current_strikethrough = True
                    if obfuscated and not current_obfuscated:
                        motd_text += "&k"
                        current_obfuscated = True
                    
                    motd_text += text
                    
                it += 1
            
            if block.next().isValid():
                motd_text += "\\n"
            block = block.next()
        
        return motd_text
    
    def tg_CopyOutput(self):
        clipboard = QApplication.clipboard()
        text = self.ui.textGeneratorOutput.text()
        clipboard.setText(text)