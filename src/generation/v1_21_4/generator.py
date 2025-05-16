import os
import json
import importlib
import sys

import blocks
import items
import recipes
import paintings

from utils.alert import alert

from PySide6.QtWidgets import QFileDialog

class Generator():
    def __init__(self, app_ver):
        self.APP_VERSION = app_ver

    def generateResourcePack(self):
        self.resPackDirectory = os.path.join(self.outputDir, f'{self.packName} Resource Pack')
        os.makedirs(self.resPackDirectory, exist_ok=True)
        assets_dir = os.path.join(self.resPackDirectory, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        version = self.packVersion.replace(".", "_")
        is_legacy = self.packVersion == "1.21.3"

        if is_legacy:
            # Legacy 1.21.3 folder structure
            mc_path = os.path.join(assets_dir, "minecraft")
            os.makedirs(os.path.join(mc_path, "atlases"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "models"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "textures"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "textures", "item"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "models", "item"), exist_ok=True)
            os.makedirs(os.path.join(mc_path, "models", self.packNamespace), exist_ok=True)

            # Atlas
            atlas_path = os.path.join(mc_path, "atlases", "blocks.json")
            with open(atlas_path, "w") as file:
                json.dump({
                    "sources": [{
                        "type": "directory",
                        "source": self.packNamespace,
                        "prefix": f'{self.packNamespace}/'
                    }]
                }, file, indent=4)
        else:
            # Modern format
            ns_path = os.path.join(assets_dir, self.packNamespace)
            os.makedirs(os.path.join(ns_path, "items"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "models", "item"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "textures", "item"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "textures", "painting"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "models"), exist_ok=True)
            os.makedirs(os.path.join(ns_path, "textures"), exist_ok=True)

        # pack.mcmeta
        with open(os.path.join(self.resPackDirectory, "pack.mcmeta"), "w") as pack:
            json.dump({
                "pack": {
                    "pack_format": self.resourceFormat,
                    "description": self.packDescription
                }
            }, pack, indent=4)

        # Load resource generators
        internal = 'src.' if getattr(sys, 'frozen', False) else ''
        BlockResourcer = importlib.import_module(f'{internal}generation.v{version}.blocks').BlockResourcer
        ItemResourcer = importlib.import_module(f'{internal}generation.v{version}.items').ItemResourcer
        PaintingResourcer = importlib.import_module(f'{internal}generation.v{version}.paintings').PaintingResourcer

        # Generate resources
        if self.blocks:
            blockResourcer = BlockResourcer(self.resPackDirectory, self.packNamespace, self.blocks)
            blockResourcer.generate()

        if self.items:
            itemResourcer = ItemResourcer(
                self.resPackDirectory,
                self.packNamespace,
                self.exists,
                self.data,
                self.items,
            )
            itemResourcer.generate()

        if self.paintings and not is_legacy:
            paintingResourcer = PaintingResourcer(
                self.resPackDirectory,
                self.packNamespace,
                self.paintings
            )
            paintingResourcer.generate()

    def generateDatapack(self):
        self.outputDir = QFileDialog.getExistingDirectory(self, "Output Directory", "")
        if not self.outputDir:
            alert("Please select a valid output directory!")
            return
        
        self.packName = self.packDetails["name"]
        self.packNamespace = self.packDetails["namespace"]
        self.packDescription = self.packDetails["description"]
        self.packAuthor = self.packDetails["author"]
        self.packVersion = self.packDetails["version"]
        
        self.packDirectory = os.path.join(self.outputDir, self.packName)

        # Create base directories
        os.makedirs(self.packDirectory, exist_ok=True)
        os.makedirs(os.path.join(self.packDirectory, "data"), exist_ok=True)

        self.namespaceDirectory = os.path.join(self.packDirectory, "data", self.packNamespace)
        self.minecraftDirectory = os.path.join(self.packDirectory, "data", "minecraft")

        os.makedirs(self.minecraftDirectory, exist_ok=True)
        os.makedirs(self.namespaceDirectory, exist_ok=True)

        # Write pack.mcmeta
        pack_meta = {
            "pack": {
                "pack_format": self.dataFormat,
                "description": self.packDescription
            }
        }
        with open(os.path.join(self.packDirectory, "pack.mcmeta"), "w") as f:
            json.dump(pack_meta, f, indent=4)

        is_legacy = self.packVersion == "1.21.3"

        if is_legacy:
            # Create feature folders
            os.makedirs(os.path.join(self.namespaceDirectory, "functions"), exist_ok=True)
            if self.blocks or self.items:
                os.makedirs(os.path.join(self.namespaceDirectory, "advancements"), exist_ok=True)
            if self.blocks:
                os.makedirs(os.path.join(self.namespaceDirectory, "loot_tables"), exist_ok=True)
            if self.recipes:
                os.makedirs(os.path.join(self.namespaceDirectory, "recipes"), exist_ok=True)

            # Create tags folders
            tags_function_dir = os.path.join(self.minecraftDirectory, "tags", "functions")
            os.makedirs(tags_function_dir, exist_ok=True)

            # Write tick.mcfunction
            tick_path = os.path.join(self.namespaceDirectory, "functions", "tick.mcfunction")
            with open(tick_path, "w") as tick:
                if self.blocks:
                    tick.write(f'{self.header}execute as @e[type=item_display,tag={self.packAuthor}.custom_block] at @s run function {self.packNamespace}:blocks/as_blocks')
                else:
                    tick.write(self.header)

            # Write load.mcfunction
            load_path = os.path.join(self.namespaceDirectory, "functions", "load.mcfunction")
            with open(load_path, "w") as load:
                load.write(f'{self.header}tellraw @a {{"text":"[mDirt {self.APP_VERSION}] - Successfully loaded pack!","color":"red"}}')

        else:
            # Create feature folders
            os.makedirs(os.path.join(self.namespaceDirectory, "function"), exist_ok=True)
            if self.blocks or self.items:
                os.makedirs(os.path.join(self.namespaceDirectory, "advancement"), exist_ok=True)
            if self.blocks:
                os.makedirs(os.path.join(self.namespaceDirectory, "loot_table"), exist_ok=True)
            if self.recipes:
                os.makedirs(os.path.join(self.namespaceDirectory, "recipe"), exist_ok=True)

            # Create tags folders
            tags_function_dir = os.path.join(self.minecraftDirectory, "tags", "function")
            os.makedirs(tags_function_dir, exist_ok=True)

            # Write tick.mcfunction
            tick_path = os.path.join(self.namespaceDirectory, "function", "tick.mcfunction")
            with open(tick_path, "w") as tick:
                if self.blocks:
                    tick.write(f'{self.header}execute as @e[type=item_display,tag={self.packAuthor}.custom_block] at @s run function {self.packNamespace}:blocks/as_blocks')
                else:
                    tick.write(self.header)

            # Write load.mcfunction
            load_path = os.path.join(self.namespaceDirectory, "function", "load.mcfunction")
            with open(load_path, "w") as load:
                load.write(f'{self.header}tellraw @a {{"text":"[mDirt {self.APP_VERSION}] - Successfully loaded pack!","color":"red"}}')

        # Write tick/load JSON tags
        tick_json_path = os.path.join(tags_function_dir, "tick.json")
        load_json_path = os.path.join(tags_function_dir, "load.json")

        with open(tick_json_path, "w") as tick:
            json.dump({"values": [f'{self.packNamespace}:tick']}, tick, indent=4)

        with open(load_json_path, "w") as load:
            json.dump({"values": [f'{self.packNamespace}:load']}, load, indent=4)
        
        version = self.packVersion.replace(".", "_")

        if getattr(sys, 'frozen', False):
            internal = 'src.'
        else:
            internal = ''

        blockGenerator = blocks.BlockGenerator()
        itemGenerator = items.ItemGenerator()
        recipeGenerator = recipes.RecipeGenerator()
        paintingGenerator = paintings.PaintingGenerator()

        #######################
        # CUSTOM BLOCKS       #
        #######################

        if self.blocks:
            blockGenerator = blockGenerator(
                self.header,
                self.namespaceDirectory,
                self.packNamespace,
                self.packAuthor,
                self.blocks,
                self.items,
            )

            blockGenerator.generate()

        #######################
        # CUSTOM ITEMS        #
        #######################

        if self.items:
            itemGenerator = itemGenerator(
                self.header, 
                self.namespaceDirectory, 
                self.items,
                self.packNamespace
            )

            itemGenerator.generate()

        #######################
        # CUSTOM RECIPES      #
        #######################

        if self.recipes:
            recipeGenerator = recipeGenerator(
                self.namespaceDirectory,
                self.packNamespace,
                self.packAuthor,
                self.blocks,
                self.items,
                self.recipes,
            )

            recipeGenerator.generate()
        
        #######################
        # CUSTOM PAINTINGS    #
        #######################

        if self.paintings:
            paintingGenerator = paintingGenerator(
                self.header,
                self.namespaceDirectory,
                self.packNamespace,
                self.packAuthor,
                self.paintings,
                self.minecraftDirectory,
            )

            paintingGenerator.generate()

        #######################
        # RESOURCE PACK       #
        #######################

        self.generateResourcePack()

        #######################
        # FINISH GENERATE     #
        #######################