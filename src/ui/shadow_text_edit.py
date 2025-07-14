from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QPainter

SHADOW_COLOR_PROPERTY = 112233

class ShadowTextEdit(QTextEdit):
    """Allows drawing of shadows behind text"""
    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        doc = self.document()
        block = doc.begin()

        # Iterate blocks and fragments to draw shadows
        while block.isValid():
            layout = block.layout()
            it = block.begin()
            while not it.atEnd():
                fragment = it.fragment()
                if fragment.isValid():
                    fmt = fragment.charFormat()
                    shadow_color = fmt.property(SHADOW_COLOR_PROPERTY)
                    if shadow_color:     
                        rect = layout.boundingRect()
                        pos = self.contentOffset()

                        painter.setPen(shadow_color.darker(150))
                        painter.drawText(rect.translated(pos.x() + 2, pos.y() + 2), fragment.text())
                it += 1
            block = block.next()

        super().paintEvent(event)