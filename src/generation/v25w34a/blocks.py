import ast, os, shutil
from jinja2 import Environment, FileSystemLoader

class BlockGenerator:
    def __init__(self, header, namespaceDir, packNamespace, packAuthor, blocks, items, equipment):
        self.namespaceDirectory = namespaceDir
        self.packNamespace = packNamespace
        self.packAuthor = packAuthor
        self.header = header
        self.blocks = blocks
        self.items = items
        self.equipment = equipment

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'block_templates')),
            autoescape=True
        )
    
    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)

    def generate(self):
        os.makedirs(f'{self.namespaceDirectory}/function/blocks', exist_ok=True)

        # Create Placed Item Frame Advancement
        content = self.getTemplate('placedItemFrame.json.j2', {'packNamespace': self.packNamespace})

        with open(os.path.join(self.namespaceDirectory, f'advancement/placed_item_frame.json'), 'w') as file:
            file.write(content)
        
        # Placed Item Frame Function
        content = self.getTemplate('placedItemFrame.mcfunction.j2', {
            'header': self.header,
            'packNamespace': self.packNamespace,
            'packAuthor': self.packAuthor
        })

        with open(f'{self.namespaceDirectory}/function/blocks/placed_item_frame.mcfunction', 'w') as file:
            file.write(content)
        
        # Check Placed Item Frame Function
        content = self.getTemplate('checkPlacedItemFrame.mcfunction.j2',{
            'header': self.header,
            'blocks': self.blocks,
            'packNamespace': self.packNamespace,
            'packAuthor': self.packAuthor
        })

        with open(f'{self.namespaceDirectory}/function/blocks/check_placed_item_frame.mcfunction', 'w') as file:
            file.write(content)

        # block/* Functions
        for block in self.blocks:
            os.mkdir(f'{self.namespaceDirectory}/function/blocks/{block}')

            # block/place
            content = self.getTemplate('place.mcfunction.j2', {
                'header': self.header,
                'blocks': self.blocks,
                'block': block,
                'packAuthor': self.packAuthor,
                'packNamespace': self.packNamespace
            })

            with open(f'{self.namespaceDirectory}/function/blocks/{block}/place.mcfunction', 'w') as file:
                file.write(content)

            # block/block
            content = self.getTemplate('block.mcfunction.j2', {
                'header': self.header,
                'blocks': self.blocks,
                'block': block,
                'packNamespace': self.packNamespace
            })

            with open(f'{self.namespaceDirectory}/function/blocks/{block}/{block}.mcfunction', 'w') as file:
                file.write(content)

            # block/break
            content = self.getTemplate('break.mcfunction.j2', {
                'header': self.header,
                'blocks': self.blocks,
                'block': block,
                'packNamespace': self.packNamespace
            })

            with open(f'{self.namespaceDirectory}/function/blocks/{block}/break.mcfunction', 'w') as file:
                file.write(content)
            
        # As Blocks Function
        content = self.getTemplate('asBlocks.mcfunction.j2', {
            'header': self.header,
            'blocks': self.blocks,
            'packAuthor': self.packAuthor,
            'packNamespace': self.packNamespace
        })

        with open(f'{self.namespaceDirectory}/function/blocks/as_blocks.mcfunction', 'w') as file:
            file.write(content)

        # Give Blocks Function
        content = self.getTemplate('giveBlocks.mcfunction.j2', {
            'header': self.header,
            'blocks': self.blocks,
            'packAuthor': self.packAuthor,
            'packNamespace': self.packNamespace
        })

        with open(f'{self.namespaceDirectory}/function/give_blocks.mcfunction', 'w') as file:
            file.write(content)
        
        # Loot Tables
        for block in self.blocks:
            content = self.getTemplate('block.json.j2', {
                'blocks': self.blocks,
                'block': block,
                'items': self.items,
                'equipment': self.equipment,
                'packAuthor': self.packAuthor,
                'packNamespace': self.packNamespace
            })

            with open(f'{self.namespaceDirectory}/loot_table/{block}.json', 'w') as file:
                file.write(content)


class BlockResourcer:
    def __init__(self, resPackDirectory, packNamespace, blocks):
        self.resPackDirectory = resPackDirectory
        self.blocks = blocks
        self.packNamespace = packNamespace

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'block_templates')),
            autoescape=True
        )
    
    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)

    def generate(self):
        # Block Model Definition
        for block in self.blocks:
            content = self.getTemplate('modelDef.json.j2', {
                'packNamespace': self.packNamespace,
                'block': block
            })

            with open(f'{self.resPackDirectory}/assets/{self.packNamespace}/items/{block}.json', 'w') as file:
                file.write(content)
        
        # Copy Block Textures To Pack
        for block in self.blocks:
            texturePath = (
                f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/item/'
            )

            if ".json" not in self.blocks[block]["model"]:
                for path in self.blocks[block]["textures"].values():
                    if not os.path.exists(os.path.join(texturePath, os.path.splitext(os.path.basename(str(path)))[-2] + ".png",)):
                        shutil.copy(path, os.path.join(texturePath, os.path.splitext(os.path.basename(str(path)))[-2] + ".png",),)
            else:
                path = self.blocks[block]["textures"]["5"]
                if not os.path.exists(os.path.join(texturePath, os.path.splitext(os.path.basename(str(path)))[-2] + ".png",)):
                    shutil.copy(path, os.path.join(texturePath, os.path.splitext(os.path.basename(str(path)))[-2] + ".png",),)
        
        # Copy / Write Block Model To Pack
        for block in self.blocks:
            textureNames = []

            for texture in self.blocks[block]["textures"]:
                textureNames.append(os.path.splitext(os.path.basename(self.blocks[block]["textures"][texture]))[0])
            
            content = self.getTemplate('model.json.j2', {
                'textureNames': textureNames,
                'packNamespace': self.packNamespace
            })
            with open(f'{self.resPackDirectory}/assets/{self.packNamespace}/models/item/{self.blocks[block]["name"]}.json', 'w') as file:
                if ".json" not in self.blocks[block]["model"]:
                    file.write(content)
                else:
                    with open(self.blocks[block]["model"], "r") as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][
                            texture
                        ] = f'{self.packNamespace}:item/{model["textures"][texture]}'
                    file.write(str(model).replace("'", '"'))