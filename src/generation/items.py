import ast
import os
import shutil


class ItemGenerator:
    def __init__(self, header, namespaceDirectory, items, namespace):
        self.header = header
        self.namespaceDirectory = namespaceDirectory
        self.items = items
        self.packNamespace = namespace

    def generate(self):
        os.mkdir(f'{self.namespaceDirectory}/function/items')

        # Give Items Function
        with open(
            f"{self.namespaceDirectory}/function/give_items.mcfunction", "a"
        ) as file:
            file.write(self.header)
            for item in self.items:
                rightClick = self.items[item]["rightClick"]
                if not rightClick["enabled"]:
                    file.write(f'give @s {self.items[item]["baseItem"]}[item_name=\'{{"italic":false,"text":"{self.items[item]["displayName"]}"}}\',custom_model_data={self.items[item]["cmd"]},custom_data={{"{self.items[item]["name"]}":true}}] 1\n')
                else:
                    file.write(f'give @s {self.items[item]["baseItem"]}[item_name=\'{{"italic":false,"text":"{self.items[item]["displayName"]}"}}\',custom_model_data={self.items[item]["cmd"]},custom_data={{"{self.items[item]["name"]}":true}},food={{can_always_eat:true,nutrition:0,saturation:0}},consumable={{animation:"none",consume_seconds:99999,has_consume_particles:false}}] 1\n')
        
        # Item mcfunction & Item Cooldown mcfunction & Item Execute mcfunction
        for item in self.items:
            os.mkdir(f'{self.namespaceDirectory}/function/items/{self.items[item]["name"]}')
            rightClick = self.items[item]["rightClick"]
            if not rightClick["enabled"]: continue

            if rightClick["mode"] == "impulse":
                with open(f'{self.namespaceDirectory}/function/items/{self.items[item]["name"]}/{self.items[item]["name"]}.mcfunction', 'w') as f:
                    f.write(f'{self.header}'
                            f'execute unless score @s {self.items[item]["name"]}_cooldown matches 1.. run function {self.packNamespace}:items/{self.items[item]["name"]}/execute\n'
                            f'advancement revoke @s only {self.packNamespace}:{self.items[item]["name"]}_use\n'
                            f'advancement revoke @s only {self.packNamespace}:{self.items[item]["name"]}_cooldown\n'
                            f'scoreboard players set @s {self.items[item]["name"]}_cooldown 2\n')
                
                with open(f'{self.namespaceDirectory}/function/items/{self.items[item]["name"]}/cooldown.mcfunction', 'w') as f:
                    f.write(f'{self.header}'
                            f'scoreboard players remove @s {self.items[item]["name"]}_cooldown 1\n'
                            f'execute if score @s {self.items[item]["name"]}_cooldown matches 1.. run return run advancement revoke @s only {self.packNamespace}:{self.items[item]["name"]}_cooldown\n'
                            f'scoreboard players reset @s {self.items[item]["name"]}_cooldown\n')
                
                with open(f'{self.namespaceDirectory}/function/items/{self.items[item]["name"]}/execute.mcfunction', 'w') as f:
                    f.write(f'{self.header}'
                            f'{rightClick["function"]}')
            
            elif rightClick["mode"] == "tick":
                with open(f'{self.namespaceDirectory}/function/items/{self.items[item]["name"]}/{self.items[item]["name"]}.mcfunction', 'w') as f:
                    f.write(f'{self.header}'
                            f'advancement revoke @s only {self.packNamespace}:{self.items[item]["name"]}_use\n'
                            f'function {self.packNamespace}:items/{self.items[item]["name"]}/execute')
                
                with open(f'{self.namespaceDirectory}/function/items/{self.items[item]["name"]}/execute.mcfunction', 'w') as f:
                    f.write(f'{self.header}'
                            f'{rightClick["function"]}')
        
        # Item Cooldown & Item Use advancements
        for item in self.items:
            rightClick = self.items[item]["rightClick"]
            if not rightClick["enabled"]: continue

            with open(f'{self.namespaceDirectory}/advancement/{self.items[item]["name"]}_use.json', 'w') as f:
                    f.write(f'{{"criteria": {{"use_item":{{"trigger":"minecraft:using_item","condtions": {{"items": {{"predicates":{{"minecraft:custom_data":{{"{self.items[item]["name"]}":true}}}}}}}}}}}},"rewards":{{"function":"{self.packNamespace}:items/{self.items[item]["name"]}/{self.items[item]["name"]}"}}}}')

            if rightClick["mode"] == "impulse":
                with open(f'{self.namespaceDirectory}/advancement/{self.items[item]["name"]}_cooldown.json', 'w') as f:
                    f.write(f'{{"criteria": {{"tick":{{"trigger":"minecraft:tick"}}}},"rewards":{{"function":"{self.packNamespace}:items/{self.items[item]["name"]}/cooldown"}}}}')
        
        # Append Scoreboard Declerations Within Load mcfunction
        with open(f'{self.namespaceDirectory}/function/load.mcfunction', 'a') as f:
            for item in self.items:
                rightClick = self.items[item]["rightClick"]
                if not rightClick["enabled"]: continue

                if rightClick["mode"] == "impulse":
                    f.write(f'scoreboard objectives add {self.items[item]["name"]}_cooldown dummy\n')
        

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
