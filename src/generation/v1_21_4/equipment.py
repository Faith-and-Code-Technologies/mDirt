import ast, os, shutil, json
from jinja2 import Environment, FileSystemLoader

class EquipmentGenerator:
    def __init__(self, header, namespaceDirectory, equipment, namespace):
        self.header = header
        self.namespaceDirectory = namespaceDirectory
        self.equipment = equipment
        self.packNamespace = namespace

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'equipment_templates')),
            autoescape=True
        )

    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)
        
    def generate(self):

        # Give Equipment Function
        content = self.getTemplate('giveEquipment.mcfunction.j2', {
            'header': self.header,
            'equipment': self.equipment,
            'packNamespace': self.packNamespace
        })

        with open(f'{self.namespaceDirectory}/function/give_equipment.mcfunction', 'w') as file:
            file.write(content)


class EquipmentResourcer:
    def __init__(self, resPackDirectory, packNamespace, equipment):
        self.resPackDirectory = resPackDirectory
        self.packNamespace = packNamespace
        self.equipment = equipment

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'equipment_templates')),
            autoescape=True
        )
    
    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)
    
    def generate(self):
        # Create namespace/models/item/*.json
        for equip in self.equipment:
            equipmentName = self.equipment[equip]["name"]
            horse = self.equipment[equip]["includeHorse"]

            # Generate it for helmet, chestplate, leggings, and boots
            for item in ["helmet", "chestplate", "leggings", "boots"]:
                modelPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/models/item/'
                content = self.getTemplate('model.json.j2', {
                    'packNamespace': self.packNamespace,
                    'equipmentName': equipmentName,
                    'equipmentType': item
                })

                with open(f'{modelPath}{equip}_{item}.json', "a") as file:
                    file.write(content)
            
            if horse:
                modelPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/models/item/'
                content = self.getTemplate('model.json.j2', {
                    'packNamespace': self.packNamespace,
                    'equipmentName': equipmentName,
                    'equipmentType': "horse_armor"
                })

                with open(f'{modelPath}{equip}_horse_armor.json', "a") as file:
                    file.write(content)
        
        # Create namespace/items/*.json
        for equip in self.equipment:
            horse = self.equipment[equip]["includeHorse"]
            equipmentName = self.equipment[equip]["name"]

            # Generate it for helmet, chestplate, leggings, and boots
            for item in ["helmet", "chestplate", "leggings", "boots"]:
                modelPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/items/'
                content = self.getTemplate('modelDef.json.j2', {
                    'packNamespace': self.packNamespace,
                    'equipmentName': equipmentName,
                    'equipmentType': item
                })

                with open(f'{modelPath}{equip}_{item}.json', "a") as file:
                    file.write(content)
            
            if horse:
                modelPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/items/'
                content = self.getTemplate('modelDef.json.j2', {
                    'packNamespace': self.packNamespace,
                    'equipmentName': equipmentName,
                    'equipmentType': "horse_armor"
                })

                with open(f'{modelPath}{equip}_horse_armor.json', "a") as file:
                    file.write(content)
        
        # Create namespace/equipment/NAME.json
        for equip in self.equipment:
            horse = self.equipment[equip]["includeHorse"]
            equipmentName = equip

            modelPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/equipment/'
            if not horse:
                content = self.getTemplate('equipment.json.j2', {
                    'packNamespace': self.packNamespace,
                    'equipmentName': equipmentName
                })
            else:
                content = self.getTemplate('equipmentHorse.json.j2', {
                    'packNamespace': self.packNamespace,
                    'equipmentName': equipmentName
                })

            with open(f'{modelPath}{equip}.json', "a") as file:
                file.write(content)
        
        # Copy namespace/textures/item/*.png
        for equip in self.equipment:
            horse = self.equipment[equip]["includeHorse"]
            currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/item/'
            for texture in self.equipment[equip]["itemTextures"]:
                name = self.equipment[equip]["name"] + "_" + texture
                if texture == "horseArmor":
                    name = self.equipment[equip]["name"] + "_horse_armor"
                shutil.copy(
                    self.equipment[equip]["itemTextures"][texture], 
                    os.path.normpath(f'{currentPath}/{name}.png')
                    )
        
        # Copy namespace/textures/entity/equipment/*/*.png
        for equip in self.equipment:
            for texture in self.equipment[equip]["modelTextures"]:
                if texture == "h_l": currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/entity/equipment/humanoid_leggings/'
                elif texture == "horseArmor": currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/entity/equipment/horse_body/'
                else: currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/entity/equipment/humanoid/'
                shutil.copy(
                    self.equipment[equip]["modelTextures"][texture], 
                    os.path.normpath(f'{currentPath}/emerald.png')
                    )