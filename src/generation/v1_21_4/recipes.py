import os
from jinja2 import Environment, FileSystemLoader

class RecipeGenerator:
    def __init__(self, namespaceDirectory, packNamespace, packAuthor, blocks, items, recipes):
        self.namespaceDirectory = namespaceDirectory
        self.packAuthor = packAuthor
        self.blocks = blocks
        self.items = items
        self.recipes = recipes
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
                    lines = []
                    items = []
                    letters = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I"}

                    # Generate the crafting pattern (rows of letters)
                    result = [letters.get(key, " ") for key in range(9)]
                    for i in range(0, len(result), 3):
                        line = f'"{result[i]}{result[i + 1]}{result[i + 2]}"' if i + 2 < len(result) else f'"{result[i]}{result[i + 1]}"'
                        lines.append(line)

                    # Generate key-value pairs for items
                    itms = [(letters[int(k)], v) for k, v in recip.items() if v]
                    for i, (key, value) in enumerate(itms):
                        items.append(f'"{key}":"minecraft:{value}"')
                        if i < len(itms) - 1:
                            items[-1] += ","

                    # Determine output item and type (item, block, or vanilla)
                    output_item_id = recip.get(9)
                    if output_item_id in self.items:
                        outputItem = self.items[output_item_id]
                        outputType = "item"
                    elif output_item_id in self.blocks:
                        outputItem = self.blocks[output_item_id]
                        outputType = "block"
                    else:
                        outputItem = recip[9]
                        outputType = "vanilla"

                    content = self.getTemplate('shaped.json.j2', {
                        'packNamespace': self.packNamespace,
                        'packAuthor': self.packAuthor,
                        'blocks': self.blocks,
                        'items': self.items,
                        'recipeItems': items,
                        'lines': lines,
                        'outputItem': outputItem,
                        'outputCount': self.recipes[recipe]['outputCount'],
                        'outputType': outputType
                    })

                    with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)
                
                else:
                    content = self.getTemplate('shapeless.json.j2', {
                        'recipes': self.recipes,
                        'blocks': self.blocks,
                        'items': self.items,
                        'packNamespace': self.packNamespace,
                        'packAuthor': self.packAuthor
                    })

                    with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)
            
            elif self.recipes[recipe]["type"] in ("smelting", "blasting", "smoking", "campfire_cooking"):
                content = self.getTemplate('fire.json.j2', {
                    'recipe_type': self.recipes[recipe]["type"],
                    'ingredient': self.recipes[recipe]["items"][10],
                    'output_id': self.recipes[recipe]["items"][11],
                    'items': self.items,
                    'blocks': self.blocks,
                    'packNamespace': self.packNamespace,
                    'packAuthor': self.packAuthor
                })

                with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)

            elif self.recipes[recipe]["type"] == "stonecutting":
                content = self.getTemplate('stonecutting.json.j2', {
                    'recipe_type': self.recipes[recipe]["type"],
                    'ingredient': self.recipes[recipe]["items"][10],
                    'output_id': self.recipes[recipe]["items"][11],
                    'output_count': self.recipes[recipe]["outputCount2"],
                    'items': self.items,
                    'blocks': self.blocks,
                    'packNamespace': self.packNamespace,
                    'packAuthor': self.packAuthor
                })

                with open(f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json', 'w') as file:
                        file.write(content)