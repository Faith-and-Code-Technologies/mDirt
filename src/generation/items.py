import ast
import os
import shutil


class ItemGenerator:
    def __init__(self, header, namespaceDirectory, items):
        self.header = header
        self.namespaceDirectory = namespaceDirectory
        self.items = items

    def generate(self):
        with open(
            f"{self.namespaceDirectory}/function/give_items.mcfunction", "a"
        ) as file:
            file.write(self.header)
            for item in self.items:
                file.write(
                    f'give @s {self.items[item]["baseItem"]}[item_name=\'{{"italic":false,"text":"{self.items[item]["displayName"]}"}}\',custom_model_data={self.items[item]["cmd"]}] 1\n'
                )


class ItemResourcer:
    def __init__(self, resPackDirectory, packNamespace, exists, data, items):
        self.items = items
        self.resPackDirectory = resPackDirectory
        self.exists = exists
        self.data = data
        self.packNamespace = packNamespace

    def generate(self):
        # Write Base Item Model To Pack
        for item in self.items:
            modelPath = f"{self.resPackDirectory}/assets/minecraft/models/item/"
            if not os.path.exists(
                f'{modelPath}{self.items[item]["baseItem"].removeprefix("minecraft:")}.json'
            ):
                self.exists[self.items[item]["baseItem"]] = False
            with open(
                f'{modelPath}{self.items[item]["baseItem"].removeprefix("minecraft:")}.json',
                "a",
            ) as file:
                if not self.exists[self.items[item]["baseItem"]]:
                    self.exists[self.items[item]["baseItem"]] = True
                    modelType = self.data["models"][f'minecraft:{self.items[item]["baseItem"]}']
                    file.write(f'{str(modelType)[:-1]}, "overrides": ['.replace("'", '"'))
                file.write(
                    f'{{ "predicate": {{ "minecraft:custom_model_data": {self.items[item]["cmd"]}}}, "model": "{self.packNamespace}/{self.items[item]["name"]}"}},'
                )

        # Remove Trailing Comma At Each Model
        for file in os.listdir(
            f"{self.resPackDirectory}/assets/minecraft/models/item"
        ):
            if file.endswith(".json") and not "item_frame" in file:
                with open(
                    os.path.join(
                        f"{self.resPackDirectory}/assets/minecraft/models/item/",
                        file,
                    ),
                    "r+",
                ) as f:
                    content = f.read()
                    f.seek(0)
                    f.write(content[:-1])
                    f.truncate()
                    f.write("]}")

        # Copy / Write Item Model To Pack
        for item in self.items:
            currentPath = f"{self.resPackDirectory}/assets/minecraft/models/{self.packNamespace}"
            with open(f'{currentPath}/{self.items[item]["name"]}.json', "w") as file:
                if ".json" in self.items[item]["model"]:
                    with open(self.items[item]["model"], "r") as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][
                            texture
                        ] = f'{self.packNamespace}/{model["textures"][texture]}'
                    file.write(str(model).replace("'", '"'))
                else:
                    file.write(
                        f'{{"parent":"{self.data["models"][f'minecraft:{self.items[item]["baseItem"]}']["parent"]}", "textures": {{ "layer0": "minecraft:{self.packNamespace}/{os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]}"}}}}'
                    )

        os.mkdir(
            f"{self.resPackDirectory}/assets/minecraft/textures/{self.packNamespace}"
        )

        # Copy Item Texture To Pack
        for item in self.items:
            currentPath = f"{self.resPackDirectory}/assets/minecraft/textures/{self.packNamespace}"
            shutil.copy(
                self.items[item]["texture"],
                os.path.normpath(
                    f'{currentPath}/{os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]}.png'
                ),
            )
