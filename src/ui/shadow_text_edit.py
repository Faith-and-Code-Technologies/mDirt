from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QPointF

SHADOW_COLOR_PROPERTY = 12345

class ShadowTextEdit(QTextEdit):
    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            
            doc = self.document()
            
            block = doc.begin()
            while block.isValid():
                layout = block.layout()
                if layout is None:
                    block = block.next()
                    continue
                    
                block_pos = doc.documentLayout().blockBoundingRect(block).topLeft()
                
                it = block.begin()
                while not it.atEnd():
                    fragment = it.fragment()
                    if fragment.isValid():
                        fmt = fragment.charFormat()
                        shadow_color = fmt.property(SHADOW_COLOR_PROPERTY)
                        
                        if shadow_color and isinstance(shadow_color, QColor):
                            fragment_start = fragment.position() - block.position()
                            fragment_length = fragment.length()
                            
                            for i in range(fragment_length):
                                char_pos = fragment_start + i
                                line = layout.lineForTextPosition(char_pos)
                                if line.isValid():
                                    x_result = line.cursorToX(char_pos)
                                    if isinstance(x_result, tuple):
                                        x = x_result[0]
                                    else:
                                        x = x_result
                                    
                                    y = line.y() + line.ascent()
                                    
                                    char_text = fragment.text()[i]
                                    shadow_pos = QPointF(block_pos.x() + x + 2, block_pos.y() + y + 2)
                                    
                                    painter.setPen(shadow_color.darker(150))
                                    painter.setFont(fmt.font())
                                    painter.drawText(shadow_pos, char_text)
                    
                    it += 1
                block = block.next()
        except Exception as e:
            print(f"Paint error: {e}")
        finally:
            painter.end()
        
        super().paintEvent(event)