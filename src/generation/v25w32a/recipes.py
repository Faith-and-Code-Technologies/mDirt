import os
from jinja2 import Environment, FileSystemLoader

class RecipeGenerator:
    def __init__(self, namespaceDirectory, packNamespace, packAuthor, blocks, items, recipes, equipment):
        self.namespaceDirectory = namespaceDirectory
        self.packAuthor = packAuthor
        self.blocks = blocks
        self.items = items
        self.recipes = recipes
        self.equipment = equipment
        self.packNamespace = packNamespace

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'recipe_templates')),
            autoescape=True
        )
    
    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)

    def generate(self):
        for recipe in self.recipes:
            if self.recipes[recipe]["type"] == "crafting":
                if self.recipes[recipe]["exact"]:
                    recip = self.recipes[recipe]["items"]
                    letters = {"0": "A", "1": "B", "2": "C", "3": "D", "4": "E", "5": "F", "6": "G", "7": "H", "8": "I"}

                    content = self.getTemplate('shaped.json.j2', {
                        'ingredients': recip,
                        'outputCount': self.recipes[recipe]['outputCount'],
                        'letters': letters,
                        'blocks': self.blocks,
                        'items': self.items,
                        'equipment': self.equipment,
                        'packNamespace': self.packNamespace,
                        'packAuthor': self.packAuthor
                    })

                    with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)
                
                else:
                    content = self.getTemplate('shapeless.json.j2', {
                        'ingredients': self.recipes[recipe]["items"],
                        'outputCount': self.recipes[recipe]['outputCount'],
                        'blocks': self.blocks,
                        'items': self.items,
                        'equipment': self.equipment,
                        'packNamespace': self.packNamespace,
                        'packAuthor': self.packAuthor
                    })

                    with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)
            
            elif self.recipes[recipe]["type"] in ("smelting", "blasting", "smoking", "campfire_cooking"):
                content = self.getTemplate('fire.json.j2', {
                    'recipe_type': self.recipes[recipe]["type"],
                    'ingredient': self.recipes[recipe]["items"]["10"],
                    'result': self.recipes[recipe]["items"]["11"],
                    'items': self.items,
                    'blocks': self.blocks,
                    'equipment': self.equipment,
                    'packNamespace': self.packNamespace,
                    'packAuthor': self.packAuthor
                })

                with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)

            elif self.recipes[recipe]["type"] == "stonecutting":
                content = self.getTemplate('stonecutting.json.j2', {
                    'ingredient': self.recipes[recipe]["items"]["10"],
                    'result': self.recipes[recipe]["items"]["11"],
                    'outputCount': self.recipes[recipe]["outputCount2"],
                    'items': self.items,
                    'blocks': self.blocks,
                    'equipment': self.equipment,
                    'packNamespace': self.packNamespace,
                    'packAuthor': self.packAuthor
                })

                with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)