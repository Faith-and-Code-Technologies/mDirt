import os

class BlockGenerator:
    def __init__(self, header, namespaceDir, packNamespace, packAuthor, blocks):
        self.namespaceDirectory = namespaceDir
        self.packNamespace = packNamespace
        self.packAuthor = packAuthor
        self.header = header
        self.blocks = blocks

    def generate(self):
        os.mkdir(f"{self.namespaceDirectory}\\function\\blocks")

        # Placed Item Frame Advancement
        with open(
                f"{self.namespaceDirectory}\\advancement\\placed_item_frame.json", "w"
        ) as file:
            file.write(
                f'{{"criteria": {{"requirement": {{"trigger": "minecraft:item_used_on_block","conditions": {{"location": [{{"condition": "minecraft:match_tool","predicate": {{"items": ["minecraft:item_frame"]}}}}]}}}}}}, "rewards": {{"function": "{self.packNamespace}:placed_item_frame"}}}}'
            )

        # Placed Item Frame Function
        with open(
                f"{self.namespaceDirectory}\\function\\blocks\\placed_item_frame.mcfunction",
                "w",
        ) as file:
            file.write(
                f"{self.header}advancement revoke @s only {self.packNamespace}:placed_item_frame\n"
                f"execute as @e[tag={self.packAuthor}.item_frame_block,distance=..10] at @s run function {self.packNamespace}:check_placed_item_frame"
            )

        # Check Placed Item Frame, block/place Functions
        with open(
                f"{self.packNamespace}\\function\\blocks\\check_placed_item_frame", "a"
        ) as file:
            for block in self.blocks:
                os.mkdir(
                    f'{self.namespaceDirectory}\\function\\blocks\\{self.blocks[block]["name"]}'
                )
                with open(
                        f'{self.namespaceDirectory}\\function\\{self.blocks[block]["name"]}\\place.mcfunction',
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
                            f'execute at @p if entity @p[y_rotation=135..-135,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~-0.469 {{Rotation:[0F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n'
                        )
                        file2.write(
                            f'execute at @p if entity @p[y_rotation=-135..-45,x_rotation=-45..45] at @s run summon item_display ~0.469 ~0.469 ~ {{Rotation:[90F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n'
                        )
                        file2.write(
                            f'execute at @p if entity @p[y_rotation=-45..45,x_rotation=-45..45] at @s run summon item_display ~ ~0.469 ~0.469 {{Rotation:[180F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n'
                        )
                        file2.write(
                            f'execute at @p if entity @p[y_rotation=45..135,x_rotation=-45..45] at @s run summon item_display ~-0.469 ~0.469 ~ {{Rotation:[90F,-90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n'
                        )
                        file2.write(
                            f'execute if entity @p[x_rotation=45..90] at @s run summon item_display ~ ~ ~ {{brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n'
                        )
                        file2.write(
                            f'execute if entity @p[x_rotation=-90..-45] at @s run summon item_display ~ ~0.469 ~-0.47 {{Rotation:[0F,90F],brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,-1f,1f,1f],right_rotation:[1.000f,0.5f,0.5f,0f],translation:[0f,0.47f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n'
                        )
                    else:
                        file2.write(
                            f'summon item_display ~ ~ ~ {{brightness:{{sky:15,block:0}}}},Tags:["{self.packAuthor}.{self.blocks[block]["name"]}","{self.packAuthor}.custom_block"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:custom_model_data":{self.blocks[block]["cmd"]}}}}}}}\n'
                        )
                file.write(
                    f"{self.header}execute as @s[tag={self.packAuthor}.{self.blocks[block]['name']}] run function {self.packNamespace}:blocks/{self.blocks[block]['name']}/place\n"
                )
            file.write("kill @s")

        # As Blocks, block/block, block/break Functions
        with open(
                f"{self.namespaceDirectory}\\function\\blocks\\as_blocks.mcfunction", "a"
        ) as file:
            file.write(self.header)
            for block in self.blocks:
                with open(
                        f"{self.namespaceDirectory}\\function\\blocks\\{block}\\{block}.mcfunction",
                        "w",
                ) as file2:
                    file2.write(
                        f'{self.header}execute unless block ~ ~ ~ {self.blocks[block]["baseBlock"]} run function {self.packNamespace}:blocks/{self.blocks[block]["name"]}/break'
                    )
                with open(
                        f"{self.namespaceDirectory}\\function\\blocks\\{block}\\break.mcfunction",
                        "a",
                ) as file2:
                    file2.write(
                        f'{self.header}execute as @e[type=item,sort=nearest,limit=1,distance=..2,nbt={{OnGround:0b,Age:0s,Item:{{id:"{self.blocks[block]["baseBlock"]}"}}}}] run kill @s\n'
                        f'loot spawn ~ ~ ~ loot {self.packNamespace}:{self.blocks[block]["name"]}\n'
                        f"kill @s"
                    )

                file.write(
                    f'execute as @s[tag={self.packAuthor}.{self.blocks[block]["name"]}] run function {self.packNamespace}:blocks/{self.blocks[block]["name"]}/{self.blocks[block]["name"]}\n'
                )

        # Give Blocks Function
        with open(
                f"{self.namespaceDirectory}\\function\\give_blocks.mcfunction", "a"
        ) as file:
            file.write(self.header)
            for block in self.blocks:
                file.write(
                    f'give @s item_frame[item_name=\'{{"italic":false,"text":"{self.blocks[block]["displayName"]}}}\',custom_model_data={self.blocks[block]["cmd"]},entity_data={{id:"minecraft:item_frame",Fixed:1b,Invisible:1b,Silent:1b,Invulnerable:1b,Facing:1,Tags:["{self.packAuthor}.item_frame_block","{self.packAuthor}.{self.blocks[block]["name"]}"]}}] 1\n'
                )

        # Loot Tables
        for block in self.blocks:
            with open(
                    f'{self.namespaceDirectory}\\loot_table\\{self.blocks[block]["name"]}.json',
                    "w",
            ) as file:
                if self.blocks[block]["blockDrop"] == "":
                    file.write(
                        f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "minecraft:item_frame"}}],"functions": [{{"function": "minecraft:set_components","components": {{"minecraft:custom_model_data": {self.blocks[block]["cmd"]},"minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{self.blocks[block]["displayName"]}\\"}}","minecraft:entity_data": {{"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{self.blocks[block]["name"]}"]}}}}}}]}}]}}'
                    )
                else:
                    file.write(
                        f'{{"pools": [{{"rolls": 1,"entries": [{{"type": "minecraft:item","name": "{self.blocks[block]["blockDrop"]}"}}]}}]}}'
                    )