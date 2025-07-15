from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSpinBox, 
                             QPushButton, QColorDialog)


class PotionEffect:
    def __init__(self, effectId, duration=30, amplifier=1):
        self.effectId = effectId
        self.duration = duration
        self.amplifier = amplifier
    
    def toMinecraftFormat(self):
        cleanId = self.effectId.lower().replace(" ", "_")
        return f'{{id:"{cleanId}",amplifier:{self.amplifier-1},duration:{self.duration*20}}}'
    
    def __eq__(self, other):
        return isinstance(other, PotionEffect) and self.effectId == other.effectId


class PotionEffectWidget(QWidget):
    def __init__(self, effectId, onRemoveCallback, parent=None):
        super().__init__(parent)
        self.effectId = effectId
        self.onRemoveCallback = onRemoveCallback
        self.setupUi()
    
    def setupUi(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        effectLabel = QLabel(f"<b>{self.effectId}</b>")
        effectLabel.setMinimumWidth(12)
        
        durationLabel = QLabel("Duration:")
        self.durationSpinbox = QSpinBox()
        self.durationSpinbox.setRange(1, 999999)
        self.durationSpinbox.setValue(30)
        self.durationSpinbox.setSuffix(" seconds")
        
        amplifierLabel = QLabel("Level:")
        self.amplifierSpinbox = QSpinBox()
        self.amplifierSpinbox.setRange(1, 255)
        self.amplifierSpinbox.setValue(1)
        
        removeBtn = QPushButton("−")
        removeBtn.setMaximumWidth(30)
        removeBtn.clicked.connect(self.removeEffect)
        
        layout.addWidget(effectLabel)
        layout.addWidget(durationLabel)
        layout.addWidget(self.durationSpinbox)
        layout.addWidget(amplifierLabel)
        layout.addWidget(self.amplifierSpinbox)
        layout.addWidget(removeBtn)
    
    def removeEffect(self):
        if self.onRemoveCallback:
            self.onRemoveCallback(self)
    
    def getEffectData(self):
        return {
            'duration': self.durationSpinbox.value(),
            'amplifier': self.amplifierSpinbox.value()
        }
    
    def getPotionEffect(self):
        return PotionEffect(
            self.effectId,
            self.durationSpinbox.value(),
            self.amplifierSpinbox.value()
        )


class PotionGenerator:
    def __init__(self, availableEffects=None):
        self.availableEffects = availableEffects or []
        self.effects = []
        self.color = 0xFFFFFF
        self.name = ""
        self.potionType = "potion"
    
    def addEffect(self, effect):
        if isinstance(effect, str):
            effect = PotionEffect(effect)
        
        for existingEffect in self.effects:
            if existingEffect.effectId == effect.effectId:
                raise ValueError(f"{effect.effectId} is already added to this Potion!")
        
        self.effects.append(effect)
    
    def removeEffect(self, effectId):
        self.effects = [e for e in self.effects if e.effectId != effectId]
    
    def removeEffectByIndex(self, index):
        if 0 <= index < len(self.effects):
            self.effects.pop(index)
    
    def clearEffects(self):
        self.effects = []
    
    def setColor(self, color):
        self.color = color & 0xFFFFFF
    
    def setName(self, name):
        self.name = name
    
    def setPotionType(self, potionType):
        self.potionType = potionType
    
    def getColorHex(self):
        return f"#{self.color:06x}"
    
    def hasEffect(self, effectId):
        return any(e.effectId == effectId for e in self.effects)
    
    def getEffectCount(self):
        return len(self.effects)
    
    def generateCommand(self):
        if not self.effects:
            return ""
        
        cleanType = self.potionType.lower().replace(' ', '_')
        command = f"/give @s {cleanType}"
        
        command += "[potion_contents={potion:\"minecraft:water\","
        command += f"custom_color:{self.color},"
        command += "custom_effects:["
        
        effectParts = []
        for effect in self.effects:
            effectParts.append(effect.toMinecraftFormat())
        
        command += ",".join(effectParts)
        command += "]},"
        
        command += f"custom_name={{\"italic\":false,\"text\":\"{self.name}\"}}"
        command += "] 1"
        
        return command


class PotionColorPicker:
    @staticmethod
    def showColorDialog(parent=None, initialColor=None):
        if initialColor is not None:
            from PySide6.QtGui import QColor
            color = QColorDialog.getColor(QColor(initialColor), parent)
        else:
            color = QColorDialog.getColor(parent=parent)
        
        if color.isValid():
            return color.rgb() & 0xFFFFFF
        return None
    
    @staticmethod
    def colorToHex(colorInt):
        return f"#{colorInt:06x}"
    
    @staticmethod
    def colorToStylesheet(colorInt):
        hexColor = PotionColorPicker.colorToHex(colorInt)
        return f"background-color: {hexColor}; border: 1px solid black;"


if __name__ == "__main__":
    generator = PotionGenerator()
    
    try:
        generator.addEffect(PotionEffect("Speed", 60, 2))
        generator.addEffect(PotionEffect("Jump Boost", 45, 1))
        generator.setName("Super Speed Potion")
        generator.setColor(0xFF0000)
        
        print("Generated command:")
        print(generator.generateCommand())
        
    except ValueError as e:
        print(f"Error: {e}")