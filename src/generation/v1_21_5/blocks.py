import ast
import os
import shutil


class BlockGenerator:
    def __init__(self, header, namespaceDir, packNamespace, packAuthor, blocks, items):
        self.namespaceDirectory = namespaceDir
        self.packNamespace = packNamespace
        self.packAuthor = packAuthor
        self.header = header
        self.blocks = blocks
        self.items = items

    def generate(self):
        os.mkdir(f"{self.namespaceDirectory}/function/blocks")

        # Placed Item Frame Advancement
        with open(
            f"{self.namespaceDirectory}/advancement/placed_item_frame.json", "w"
        ) as file:
            file.write(
                f'{{"criteria": {{"requirement": {{"trigger": "minecraft:item_used_on_block","conditions": {{"location": [{{"condition": "minecraft:match_tool","predicate": {{"items": ["minecraft:item_frame"]}}}}]}}}}}}, "rewards": {{"function": "{self.packNamespace}:blocks/placed_item_frame"}}}}'
            )

        # Placed Item Frame Function
        with open(
            f"{self.namespaceDirectory}/function/blocks/placed_item_frame.mcfunction",
            "w",
        ) as file:
            file.write(
                f"{self.header}advancement revoke @s only {self.packNamespace}:placed_item_frame\n"
                f"execute as @e[tag={self.packAuthor}.item_frame_block,distance=..10] at @s run function {self.packNamespace}:blocks/check_placed_item_frame"
            )

        # Check Placed Item Frame, block/place Functions
        with open(
            f"{self.namespaceDirectory}/function/blocks/check_placed_item_frame.mcfunction", "a"
        ) as file:
            for block in self.blocks:
                os.mkdir(
                    f'{self.namespaceDirectory}/function/blocks/{self.blocks[block]["name"]}'
                )
                with open(
                    f'{self.namespaceDirectory}/function/blocks/{self.blocks[block]["name"]}/place.mcfunction',
                    "a",
                ) as file2:
                    file2.write(
                        f'{self.header}setblock ~ ~ ~ {self.blocks[block]["baseBlock"]} keep\n'
                    )
                    if self.blocks[block]["placeSound"] != "":
                        file2.write(
                            f'playsound {self.blocks[block]["placeSound"]} block @e[type=player,distance=..5] ~ ~ ~ 10 1 1\n'
                        )
                    if self.blocks[block]["directional"]:
                        file2.write(
                            f'execute at @p if entity @p[y_rotation=135..-135,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~-0.469 {{Rotation:[0F,90F],brightness:{{sky:15,block:0}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"{self.packNamespace}:{self.blocks[block]["name"]}"}}}}}}\n'
                        )
                        file2.write(
                            f'execute at @p if entity @p[y_rotation=-135..-45,x_rotation=-45..45] at @s run summon item_display ~0.469 ~0.469 ~ {{Rotation:[90F,90F],brightness:{{sky:15,block:0}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"{self.packNamespace}:{self.blocks[block]["name"]}"}}}}}}\n'
                        )
                        file2.write(
                            f'execute at @p if entity @p[y_rotation=-45..45,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~0.469 {{Rotation:[180F,90F],brightness:{{sky:15,block:0}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"{self.packNamespace}:{self.blocks[block]["name"]}"}}}}}}\n'
                        )
                        file2.write(
                            f'execute at @p if entity @p[y_rotation=45..135,x_rotation=-45..45] at @s run summon item_display ~-0.469 ~0.469 ~ {{Rotation:[90F,-90F],brightness:{{sky:15,block:0}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"{self.packNamespace}:{self.blocks[block]["name"]}"}}}}}}\n'
                        )
                        file2.write(
                            f'execute if entity @p[x_rotation=45..90] at @s run summon item_display ~ ~ ~ {{brightness:{{sky:15,block:0}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"{self.packNamespace}:{self.blocks[block]["name"]}"}}}}}}\n'
                        )
                        file2.write(
                            f'execute if entity @p[x_rotation=-90..-45] at @s run summon item_display ~ ~0.469 ~-0.47 {{Rotation:[0F,90F],brightness:{{sky:15,block:0}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,-1f,1f,1f],right_rotation:[1.000f,0.5f,0.5f,0f],translation:[0f,0.47f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"{self.packNamespace}:{self.blocks[block]["name"]}"}}}}}}\n'
                        )
                    else:
                        file2.write(
                            f'summon item_display ~ ~ ~ {{brightness:{{sky:15,block:0}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"{self.packNamespace}:{self.blocks[block]["name"]}"}}}}}}\n'
                        )
                file.write(
                    f"{self.header}execute as @s[tag={self.packAuthor}.{self.blocks[block]['name']}] run function {self.packNamespace}:blocks/{self.blocks[block]['name']}/place\n"
                )
            file.write("kill @s")

        # As Blocks, block/block, block/break Functions
        with open(
            f"{self.namespaceDirectory}/function/blocks/as_blocks.mcfunction", "a"
        ) as file:
            file.write(self.header)
            for block in self.blocks:
                with open(
                    f"{self.namespaceDirectory}/function/blocks/{block}/{block}.mcfunction",
                    "w",
                ) as file2:
                    file2.write(
                        f'{self.header}execute unless block ~ ~ ~ {self.blocks[block]["baseBlock"]} run function {self.packNamespace}:blocks/{self.blocks[block]["name"]}/break'
                    )
                with open(
                    f"{self.namespaceDirectory}/function/blocks/{block}/break.mcfunction",
                    "a",
                ) as file2:
                    file2.write(
                        f'{self.header}execute as @e[type=item,sort=nearest,limit=1,distance=..2,nbt={{OnGround:0b,Age:0s}}] run kill @s\n'
                        f'loot spawn ~ ~ ~ loot {self.packNamespace}:{self.blocks[block]["name"]}\n'
                        f"kill @s"
                    )

                file.write(
                    f'execute as @s[tag={self.packAuthor}.{self.blocks[block]["name"]}] run function {self.packNamespace}:blocks/{self.blocks[block]["name"]}/{self.blocks[block]["name"]}\n'
                )

        # Give Blocks Function
        with open(
            f"{self.namespaceDirectory}/function/give_blocks.mcfunction", "a"
        ) as file:
            file.write(self.header)
            for block in self.blocks:
                file.write(
                    f'give @s item_frame[item_name=\'{{"italic":false,"text":"{self.blocks[block]["displayName"]}"}}\',item_model="{self.packNamespace}:{self.blocks[block]["name"]}",entity_data={{id:"minecraft:item_frame",Fixed:1b,Invisible:1b,Silent:1b,Invulnerable:1b,Facing:1,Tags:["{self.packAuthor}.item_frame_block","{self.packAuthor}.{self.blocks[block]["name"]}"]}}] 1\n'
                )

        # Loot Tables
        for block in self.blocks:
            with open(
                f'{self.namespaceDirectory}/loot_table/{self.blocks[block]["name"]}.json',
                "w",
            ) as file:
                if self.blocks[block]["blockDrop"] == "self":
                    file.write(
                        f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "minecraft:item_frame"}}],"functions": [{{"function": "minecraft:set_components","components": {{"minecraft:item_model": "{self.packNamespace}:{self.blocks[block]["name"]}","minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{self.blocks[block]["displayName"]}\\"}}","minecraft:entity_data": {{"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{self.blocks[block]["name"]}"]}}}}}}]}}]}}'
                    )
                else:
                    if self.blocks[block]["blockDrop"] not in self.items and self.blocks[block]["blockDrop"] not in self.blocks:
                        file.write(
                            f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "{self.blocks[block]["blockDrop"]}"}}]}}]}}'
                        )
                    elif self.blocks[block]["blockDrop"] in self.items:
                        item = self.items[self.blocks[block]["blockDrop"]]
                        file.write(
                            f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "{item["baseItem"]}","functions":[{{"function": "minecraft:set_components","components":{{"minecraft:item_name": "{{\\"italic\\":false,\\"text\\":\\"{item["displayName"]}\\"}}","minecraft:max_stack_size":{item["stackSize"]},"minecraft:item_model": "{self.packNamespace}:{item["name"]}"}}}}]}}]}}]}}'
                        )
                    elif self.blocks[block]["blockDrop"] in self.blocks:
                        blck = self.blocks[self.blocks[block]["blockDrop"]]
                        file.write(
                            f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "minecraft:item_frame"}}],"functions": [{{"function": "minecraft:set_components","components": {{"minecraft:item_model": "{self.packNamespace}:{blck["name"]}","minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{blck["displayName"]}\\"}}","minecraft:entity_data": {{"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{blck["name"]}"]}}}}}}]}}]}}'
                        )


class BlockResourcer:
    def __init__(self, resPackDirectory, packNamespace, blocks):
        self.resPackDirectory = resPackDirectory
        self.blocks = blocks
        self.packNamespace = packNamespace

    def generate(self):
        # Base Model For Blocks
        for block in self.blocks:
            with open(f"{self.resPackDirectory}/assets/{self.packNamespace}/items/{self.blocks[block]["name"]}.json", "a") as file:
                file.write(f'{{"model":{{"type":"minecraft:model","model":"{self.packNamespace}:item/{self.blocks[block]["name"]}"}}}}')

        # Copy Block Textures To Pack
        for block in self.blocks:
            texturePath = (
                f"{self.resPackDirectory}/assets/{self.packNamespace}/textures/item/"
            )

            if ".json" not in self.blocks[block]["model"]:
                for path in self.blocks[block]["textures"].values():
                    if not os.path.exists(
                        os.path.join(
                            texturePath,
                            os.path.splitext(os.path.basename(str(path)))[-2] + ".png",
                        )
                    ):
                        shutil.copy(
                            path,
                            os.path.join(
                                texturePath,
                                os.path.splitext(os.path.basename(str(path)))[-2]
                                + ".png",
                            ),
                        )
            else:
                path = self.blocks[block]["textures"]['5']
                if not os.path.exists(
                    os.path.join(
                        texturePath,
                        os.path.splitext(os.path.basename(str(path)))[-2] + ".png",
                    )
                ):
                    shutil.copy(
                        path,
                        os.path.join(
                            texturePath,
                            os.path.splitext(os.path.basename(str(path)))[-2] + ".png",
                        ),
                    )

        # Copy / Write Block Model To Pack
        for block in self.blocks:

            textureNames = []

            for texture in self.blocks[block]["textures"]:
                textureNames.append(os.path.splitext(os.path.basename(self.blocks[block]["textures"][texture]))[0])

            with open(
                f'{self.resPackDirectory}/assets/{self.packNamespace}/models/item/{self.blocks[block]["name"]}.json',
                "w",
            ) as file:
                if ".json" not in self.blocks[block]["model"]:
                    file.write(
                        f'{{"credit": "Made with mDirt 2.1","textures": {{"0": "{self.packNamespace}:item/{textureNames[0]}","1": "{self.packNamespace}:item/{textureNames[1]}","2": "{self.packNamespace}:item/{textureNames[2]}","3": "{self.packNamespace}:item/{textureNames[3]}","4": "{self.packNamespace}:item/{textureNames[4]}","5": "{self.packNamespace}:item/{textureNames[5]}","particle": "{self.packNamespace}:item/{textureNames[0]}"}},"elements": [{{"from": [0, 0, 0],"to": [16, 16, 16],"faces": {{"north": {{"uv": [0, 0, 16, 16], "texture": "#2"}},"east": {{"uv": [0, 0, 16, 16], "texture": "#3"}},"south": {{"uv": [0, 0, 16, 16], "texture": "#4"}},"west": {{"uv": [0, 0, 16, 16], "texture": "#1"}},"up": {{"uv": [0, 0, 16, 16], "texture": "#0"}},"down": {{"uv": [0, 0, 16, 16], "texture": "#5"}}}}}}],"display": {{"thirdperson_righthand": {{"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]}},"thirdperson_lefthand": {{"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]}},"firstperson_righthand": {{"rotation": [0, 45, 0],"scale": [0.4, 0.4, 0.4]}},"ground": {{"translation": [0, 3.25, 0],"scale": [0.4, 0.4, 0.4]}},"gui": {{"rotation": [28, 45, 0],"scale": [0.6, 0.6, 0.6]}}}}}}'
                    )
                else:
                    with open(self.blocks[block]["model"], "r") as f:
                        model = ast.literal_eval(f.read())
                    for texture in model["textures"]:
                        model["textures"][
                            texture
                        ] = f'{self.packNamespace}:item/{model["textures"][texture]}'
                    file.write(str(model).replace("'", '"'))
