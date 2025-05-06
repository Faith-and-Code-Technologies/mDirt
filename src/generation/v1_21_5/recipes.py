class RecipeGenerator:
    def __init__(self, namespaceDirectory, packNamespace, packAuthor, blocks, items, recipes):
        self.namespaceDirectory = namespaceDirectory
        self.packAuthor = packAuthor
        self.blocks = blocks
        self.items = items
        self.recipes = recipes
        self.packNamespace = packNamespace

    def generate(self):
        for recipe in self.recipes:
            if self.recipes[recipe]["type"] == "crafting":
                if self.recipes[recipe]["exact"]:
                    with open(
                        f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json',
                        "a",
                    ) as file:
                        letters = {
                            0: "A",
                            1: "B",
                            2: "C",
                            3: "D",
                            4: "E",
                            5: "F",
                            6: "G",
                            7: "H",
                            8: "I"
                        }
                        recip = self.recipes[recipe]["items"]
                        file.write(
                            '{"type": "minecraft:crafting_shaped", "pattern": ['
                        )
                        result = []

                        for key in range(9):
                            try:
                                value = recip[key]
                                result.append(letters[key])
                            except KeyError:
                                result.append(" ")



                        for i in range(0, len(result), 3):
                            if i < len(result) - 3:
                                line = f'"{result[i]}{result[i + 1]}{result[i + 2]}",\n'
                            else:
                                line = f'"{result[i]}{result[i + 1]}{result[i + 2]}"\n'
                            file.write(line)

                        file.write('],"key":{')
                        items = [
                            (k, v) for k, v in recip.items() if v not in (None, "")
                        ][:-1]
                        for i, (key, value) in enumerate(items):
                            if value != "" and value:
                                file.write(f'"{letters[int(key)]}":"minecraft:{value}"')
                                if i < len(items) - 1:
                                    file.write(",")
                        
                        
                        if recip[9] in self.items:
                            idx = self.items[recip[9]]
                            file.write(
                                f'}},"result":{{ "id":"{idx["baseItem"]}", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_name":"{{\\"italic\\":false,\\"text\\":\\"{idx["displayName"]}\\"}}", "minecraft:item_model":"{self.packNamespace}:{idx["name"]}" }} }} }}'
                            )
                        elif recip[9] in self.blocks:
                            idx = self.blocks[recip[9]]
                            file.write(
                                f'}},"result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_model":"{self.packNamespace}:{idx["name"]}", "minecraft:custom_name": "{{\\"italic\\":false,\\"text\\":\\"{idx["displayName"]}\\"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }} }}'
                            )
                        
                        else:
                            file.write(
                                f'}},"result": {{ "id":"minecraft:{recip[9]}", "count":{self.recipes[recipe]["outputCount"]}}}}}'
                            )

                else:
                    with open(
                        f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json',
                        "a",
                    ) as file:
                        file.write('{"type": "minecraft:crafting_shapeless", "ingredients":[[')
                        recip = self.recipes[recipe]["items"]
                        items = [
                            (k, v) for k, v in recip.items() if v not in (None, "")
                        ][:-1]
                        for ingredient, (key, value) in enumerate(items):
                            if value:
                                file.write(f'"minecraft:{value}"')
                                if ingredient < len(items) - 1:
                                    file.write(",")
                        if not recip[9] in self.items and not recip[9] in self.blocks:
                            file.write(
                                f']],"result":{{"id": "minecraft:{recip[9]}", "count":{self.recipes[recipe]["outputCount"]}}}}}'
                            )
                        elif recip[9] in self.items:
                            idx = self.items[recip[9]]
                            file.write(
                                f']],"result":{{ "id":"{idx["baseItem"]}", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_name":"{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:item_model":"{self.packNamespace}:{idx["name"]}"}} }} }}'
                            )
                        elif recip[9] in self.blocks:
                            idx = self.blocks[recip[9]]
                            file.write(
                                f']],"result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_model":"{self.packNamespace}:{idx["name"]}", "minecraft:custom_name": "{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}}}'
                            )

            elif self.recipes[recipe]["type"] in ("smelting", "blasting", "smoking", "campfire_cooking"):
                with open(
                    f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json',
                    "a",
                ) as file:
                    recip = self.recipes[recipe]["items"]
                    if not recip[11] in self.items and not recip[11] in self.blocks:
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recipe[10]}", "result": {{ "id": "minecraft:{recip[11]}"}} }}'
                        )
                    elif recip[11] in self.items:
                        idx = self.items[recip[11]]
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}", "result": {{ "id": "minecraft:{recip[11]}", "components": {{"minecraft:item_name":"{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:item_model":"{self.packNamespace}:{idx["name"]}" }}}}}}'
                        )
                    elif recip[11] in self.blocks:
                        idx = self.blocks[recip[11]]
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}","result":{{ "id":"minecraft:item_frame", "components": {{ "minecraft:item_model":"{self.packNamespace}:{idx["name"]}", "minecraft:custom_name": "{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }} }}'
                        )

            elif self.recipes[recipe]["type"] == "stonecutting":
                with open(
                        f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json',
                        "a",
                ) as file:
                    recip = self.recipes[recipe]["items"]
                    if not recip[11] in self.items and not recip[11] in self.blocks:
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recipe[10]}", "result": {{ "id": "minecraft:{recip[11]}"}} }}'
                        )
                    elif recip[11] in self.items:
                        idx = self.items[recip[11]]
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}", "result": {{ "id": "minecraft:{recip[11]}", "count":{self.recipes[recipe]["outputCount2"]}, "components": {{"minecraft:item_name":"{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:item_model":"{self.packNamespace}:{idx["name"]}" }}}}}}'
                        )
                    elif recip[11] in self.blocks:
                        idx = self.blocks[recip[11]]
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}","result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount2"]}, "components": {{ "minecraft:item_model":"{self.packNamespace}:{idx["name"]}", "minecraft:custom_name": "{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}}}'
                        )
