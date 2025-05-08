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
            f'{self.namespaceDirectory}/function/give_items.mcfunction', "a"
        ) as file:
            file.write(self.header)
            for item in self.items:
                rightClick = self.items[item]["rightClick"]
                if not rightClick["enabled"]:
                    file.write(f'give @s {self.items[item]["baseItem"]}[item_name=\'{{"italic":false,"text":"{self.items[item]["displayName"]}"}}\',item_model="{self.packNamespace}:{self.items[item]["name"]}",custom_data={{"{self.items[item]["name"]}":true}},max_stack_size={self.items[item]["stackSize"]}] 1\n')
                else:
                    file.write(f'give @s {self.items[item]["baseItem"]}[item_name=\'{{"italic":false,"text":"{self.items[item]["displayName"]}"}}\',item_model="{self.packNamespace}:{self.items[item]["name"]}",custom_data={{"{self.items[item]["name"]}":true}},max_stack_size={self.items[item]["stackSize"]},food={{can_always_eat:true,nutrition:0,saturation:0}},consumable={{animation:"none",consume_seconds:99999,has_consume_particles:false}}] 1\n')
        
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
                    f.write(f'{{"criteria": {{"use_item":{{"trigger":"minecraft:using_item","conditions": {{"item": {{"predicates":{{"minecraft:custom_data":{{"{self.items[item]["name"]}":true}}}}}}}}}}}},"rewards":{{"function":"{self.packNamespace}:items/{self.items[item]["name"]}/{self.items[item]["name"]}"}}}}')

            if rightClick["mode"] == "impulse":
                with open(f'{self.namespaceDirectory}/advancement/{self.items[item]["name"]}_cooldown.json', 'w') as f:
                    f.write(f'{{"criteria": {{"tick":{{"trigger":"minecraft:tick"}}}},"rewards":{{"function":"{self.packNamespace}:items/{self.items[item]["name"]}/cooldown"}}}}')
        
        # Append Scoreboard Declerations Within Load mcfunction
        with open(f'{self.namespaceDirectory}/function/load.mcfunction', 'a') as f:
            for item in self.items:
                rightClick = self.items[item]["rightClick"]
                if not rightClick["enabled"]: continue

                if rightClick["mode"] == "impulse":
                    f.write(f'\nscoreboard objectives add {self.items[item]["name"]}_cooldown dummy')

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
            modelPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/items/'

            with open(f'{modelPath}{self.items[item]["name"]}.json', "a") as file:
                file.write(f'{{"model": {{"type": "minecraft:model", "model": "{self.packNamespace}:item/{self.items[item]["name"]}"}}}}')

        # Copy / Write Item Model To Pack
        for item in self.items:
            currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/models/item'
            with open(f'{currentPath}/{self.items[item]["name"]}.json', "w") as file:
                if ".json" in self.items[item]["model"]:
                    with open(self.items[item]["model"], "r") as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][texture] = f'item/{model["textures"][texture]}'
                    file.write(str(model).replace("'", '"'))
                else:
                    file.write(f'{{"parent":"minecraft:item/{self.items[item]["model"]}","textures":{{"layer0":"{self.packNamespace}:item/{os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]}"}}}}')


        # Copy Item Texture To Pack
        for item in self.items:
            currentPath = f'{self.resPackDirectory}/assets/{self.packNamespace}/textures/item'
            shutil.copy(
                self.items[item]["texture"],
                os.path.normpath(
                    f'{currentPath}/{os.path.splitext(os.path.basename(str(self.items[item]["texture"])))[-2]}.png'
                ),
            )
