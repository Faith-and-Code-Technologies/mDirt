import os, shutil

class PaintingGenerator:
    def __init__(self, header, namespaceDirectory, packNamespace, packAuthor, paintings, minecraftDirectory):
        self.header = header
        self.namespaceDirectory = namespaceDirectory
        self.packNamespace = packNamespace
        self.packAuthor = packAuthor
        self.paintings = paintings
        self.minecraftDirectory = minecraftDirectory

    def generate(self):
        self.placeableList = []
        
        os.mkdir(f'{self.namespaceDirectory}/painting_variant')
        for painting in self.paintings:
            if self.paintings[painting]["placeable"]:
                self.placeableList.append(f'{self.packNamespace}:{self.paintings[painting]["name"]}')
            
            # Write Painting Variant
            with open(f'{self.namespaceDirectory}/painting_variant/{self.paintings[painting]["name"]}.json', 'w') as file:
                file.write(f'{{"asset_id":"{self.packNamespace}:{os.path.splitext(os.path.basename(str(self.paintings[painting]["texture"])))[-2]}","author":"{self.packAuthor}","height":{self.paintings[painting]["height"]},"width":{self.paintings[painting]["width"]},"title":"{self.paintings[painting]["displayName"]}"}}')
        
        # Add Placeable Paintings to tag
        os.mkdir(f'{self.minecraftDirectory}/tags/painting_variant')
        
        with open(f'{self.minecraftDirectory}/tags/painting_variant/placeable.json', 'a') as file:
            file.write(f'{{"values":{str(self.placeableList).replace("'", '"')}}}')
        
        # Give Paintings McFunction
        with open(f'{self.namespaceDirectory}/function/give_paintings.mcfunction', 'a') as file:
            file.write(self.header)
            for painting in self.paintings:
                file.write(f'give @s painting[entity_data={{id:"minecraft:painting",variant:"{self.packNamespace}:{self.paintings[painting]["name"]}"}}] 1\n')


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