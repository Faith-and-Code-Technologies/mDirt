import ast, os, shutil, json
from jinja2 import Environment, FileSystemLoader

class ItemGenerator:
    def __init__(self, header, namespaceDirectory, items, namespace):
        self.header = header
        self.namespaceDirectory = namespaceDirectory
        self.items = items
        self.packNamespace = namespace

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'item_templates')),
            autoescape=True
        )
    
    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)

    def generate(self):
        os.mkdir(f'{self.namespaceDirectory}/function/items')

        # Give Items Function
        content = self.getTemplate('giveItems.mcfunction.j2', {
            'header': self.header,
            'items': self.items,
            'packNamespace': self.packNamespace
        })

        with open(f'{self.namespaceDirectory}/function/give_items.mcfunction', 'w') as file:
            file.write(content)

        # Item, Cooldown, & Execute Functions
        for item in self.items:
            os.mkdir(f'{self.namespaceDirectory}/function/items/{item}')
            rightClick = self.items[item]["rightClick"]
            if rightClick["enabled"]:

                # Item
                content = self.getTemplate('item.mcfunction.j2', {
                    'header': self.header,
                    'item': item,
                    'packNamespace': self.packNamespace,
                    'mode': rightClick["mode"]
                })

                with open(f'{self.namespaceDirectory}/function/items/{item}/{item}.mcfunction', 'w') as file:
                    file.write(content)

                # Cooldown
                content = self.getTemplate('cooldown.mcfunction.j2', {
                    'header': self.header,
                    'item': item,
                    'packNamespace': self.packNamespace,
                    'mode': rightClick["mode"]
                })

                with open(f'{self.namespaceDirectory}/function/items/{item}/cooldown.mcfunction', 'w') as file:
                    file.write(content)
                
                # Execute
                content = self.getTemplate('execute.mcfunction.j2', {
                    'header': self.header,
                    'rightClick': rightClick
                })

                with open(f'{self.namespaceDirectory}/function/items/{item}/execute.mcfunction', 'w') as file:
                    file.write(content)
        
        # Cooldown & Use Advancements
        for item in self.items:
            rightClick = self.items[item]["rightClick"]
            if rightClick["enabled"]:

                # Use
                content = self.getTemplate('itemUse.json.j2', {
                    'packNamespace': self.packNamespace,
                    'item': item
                })

                with open(f'{self.namespaceDirectory}/advancement/{item}_use.json', 'w') as file:
                    file.write(content)
                
                # Cooldown
                content = self.getTemplate('itemCooldown.json.j2', {
                    'packNamespace': self.packNamespace,
                    'item': item
                })

                if rightClick["mode"] == "impulse":
                    with open(f'{self.namespaceDirectory}/advancement/{item}_cooldown.json', 'w') as file:
                        file.write(content)
        
        # Append Scoreboard Declerations Within Load
        with open(f'{self.namespaceDirectory}/function/load.mcfunction', 'a') as f:
            for item in self.items:
                rightClick = self.items[item]["rightClick"]
                if rightClick["enabled"]:
                    if rightClick["mode"] == "impulse": f.write(f'\nscoreboard objectives add {self.items[item]["name"]}_cooldown dummy')


class ItemResourcer:
    def __init__(self, resPackDirectory, packNamespace, items):
        self.items = items
        self.resPackDirectory = resPackDirectory
        self.packNamespace = packNamespace

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'item_templates')),
            autoescape=True
        )
    
    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)
    
    def generate(self):
        # Write Item Model Definition
        modelPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/items/'
        for item in self.items:
            content = self.getTemplate('modelDef.json.j2', {
                'packNamespace': self.packNamespace,
                'item': item
            })

            with open(f'{modelPath}{item}.json', "a") as file:
                file.write(content)
        
        # Copy / Write Item Model To Pack
        for item in self.items:
            currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/models/item'
            content = self.getTemplate('model.json.j2', {
                'model': self.items[item]["model"],
                'packNamespace': self.packNamespace,
                'texture': os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]
            })

            with open(f'{currentPath}/{item}.json', "w") as file:
                if ".json" in self.items[item]["model"]: # Checking for custom model. If so, copy it.
                    with open(self.items[item]["model"], "r") as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][texture] = f'item/{model["textures"][texture]}'
                    json.dumps(model)
                else:
                    file.write(content)
        
        # Copy Item Texture To Pack
        for item in self.items:
            currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/item'
            shutil.copy(
                self.items[item]["texture"], 
                os.path.normpath(f'{currentPath}/{os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]}.png')
                )