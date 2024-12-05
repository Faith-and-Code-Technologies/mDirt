class RecipeGenerator:
    def __init__(self, namespaceDirectory, packNamespace, packAuthor, blocks, items, recipes):
        self.namespaceDirectory = namespaceDirectory
        self.packAuthor = packAuthor
        self.blocks = blocks
        self.items = items
        self.recipes = recipes

    def generate(self):
        for recipe in self.recipes:
            if self.recipes[recipe]["type"] == "crafting":
                if not self.recipes[recipe]["shapeless"]:
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
                                value = recip[str(key)]
                                result.append(letters[key])
                            except KeyError:
                                result.append(" ")


                        print(result)

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
                        if not recip[str(9)] in self.items and not recip[9] in self.blocks:
                            file.write(
                                f'}},"result": {{ "id":"minecraft:{recip[str(9)]}", "count":{self.recipes[recipe]["outputCount"]}}}}}'
                            )
                        elif recip[str(9)] in self.items:
                            idx = self.items[recip[str(9)]]
                            file.write(
                                f'}},"result":{{ "id":"{idx["baseItem"]}", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_name":"{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:custom_model_data": {idx["cmd"]} }} }} }}'
                            )
                        elif recip[str(9)] in self.blocks:
                            idx = self.blocks[recip[str(9)]]
                            file.write(
                                f'}},"result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:custom_model_data": {idx["cmd"]}, "minecraft:custom_name": "{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}'
                            )

                else:
                    with open(
                        f'{self.namespaceDirectory}/recipe/{self.recipes[recipe]["name"]}.json',
                        "a",
                    ) as file:
                        recip = self.recipes[recipe]["items"]
                        items = [
                            (k, v) for k, v in recip.items() if v not in (None, "")
                        ][:-3]
                        for ingredient, (key, value) in enumerate(items):
                            if value:
                                file.write(f'"minecraft:{value}"')
                                if ingredient < len(items) - 1:
                                    file.write(",")
                        if not recip[str(9)] in self.items and not recip[str(9)] in self.blocks:
                            file.write(
                                f']],"result":{{"id": "minecraft:{recip[str(9)]}", "count":{self.recipes[recipe]["outputCount"]}}}}}'
                            )
                        elif recip[str(9)] in self.items:
                            idx = self.items[recip[str(9)]]
                            file.write(
                                f'}},"result":{{ "id":"{idx["baseItem"]}", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:item_name":"{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:custom_model_data": {idx["cmd"]}}} }} }}'
                            )
                        elif recip[str(9)] in self.blocks:
                            idx = self.blocks[recip[str(9)]]
                            file.write(
                                f'}},"result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount"]}, "components": {{ "minecraft:custom_model_data": {idx["cmd"]}, "minecraft:custom_name": "{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}'
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
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}", "result": {{ "id": "minecraft:{recip[11]}", "components": {{"minecraft:item_name":"{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:custom_model_data": {idx["cmd"]} }}}}'
                        )
                    elif recip[11] in self.blocks:
                        idx = self.blocks[recip[11]]
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}","result":{{ "id":"minecraft:item_frame", "components": {{ "minecraft:custom_model_data": {idx["cmd"]}, "minecraft:custom_name": "{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}'
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
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}", "result": {{ "id": "minecraft:{recip[11]}", "count":{self.recipes[recipe]["outputCount2"]}, "components": {{"minecraft:item_name":"{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:custom_model_data": {idx["cmd"]} }}}}'
                        )
                    elif recip[11] in self.blocks:
                        idx = self.blocks[recip[11]]
                        file.write(
                            f'{{ "type": "minecraft:{self.recipes[recipe]["type"]}", "ingredient": "minecraft:{recip[10]}","result":{{ "id":"minecraft:item_frame", "count":{self.recipes[recipe]["outputCount2"]}, "components": {{ "minecraft:custom_model_data": {idx["cmd"]}, "minecraft:custom_name": "{{/"italic/":false,/"text/":/"{idx["displayName"]}/"}}", "minecraft:entity_data": {{ "id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["{self.packAuthor}.item_frame_block","{self.packAuthor}.{idx["name"]}"] }} }} }}'
                        )
