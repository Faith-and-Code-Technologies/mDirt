import os, shutil, json
from jinja2 import Environment, FileSystemLoader

class PaintingGenerator:
    def __init__(self, header, namespaceDirectory, packNamespace, packAuthor, paintings, minecraftDirectory):
        self.header = header
        self.namespaceDirectory = namespaceDirectory
        self.packNamespace = packNamespace
        self.packAuthor = packAuthor
        self.paintings = paintings
        self.minecraftDirectory = minecraftDirectory

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'painting_templates')),
            autoescape=True
        )
    
    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)
    
    def generate(self):
        os.mkdir(f'{self.namespaceDirectory}/painting_variant')
        os.mkdir(f'{self.minecraftDirectory}/tags/painting_variant')

        for painting in self.paintings:
            
            # Painting Variant JSON
            content = self.getTemplate('painting.json.j2', {
                'paintings': self.paintings,
                'painting': painting,
                'packAuthor': self.packAuthor,
                'packNamespace': self.packNamespace,
                'texture': os.path.splitext(os.path.basename(str(self.paintings[painting]["texture"])))[-2]
            })

            with open(f'{self.namespaceDirectory}/painting_variant/{painting}.json', 'w') as file:
                file.write(content)
            
        # Give Paintings Function
        content = self.getTemplate('givePaintings.mcfunction.j2', {
            'header': self.header,
            'paintings': self.paintings,
            'packNamespace': self.packNamespace
        })

        with open(f'{self.namespaceDirectory}/function/give_paintings.mcfunction', 'a') as file:
            file.write(content)

        # Add Paintings to Placeable Tag
        content = self.getTemplate('placeable.json.j2', {
            'paintings': self.paintings,
            'packNamespace': self.packNamespace
        })

        with open(f'{self.minecraftDirectory}/tags/painting_variant/placeable.json', 'a') as file:
            file.write(content)


class PaintingResourcer:
    def __init__(self, resPackDirectory, packNamespace, paintings):
        self.resPackDirectory = resPackDirectory
        self.packNamespace = packNamespace
        self.paintings = paintings

    def generate(self):
        # Copy Painting Texture To Pack
        for painting in self.paintings:
            currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/painting'
            shutil.copy(
                self.paintings[painting]["texture"],
                os.path.normpath(
                    f'{currentPath}/{os.path.splitext(os.path.basename(str(self.paintings[painting]["texture"])))[-2]}.png'
                ),
            )