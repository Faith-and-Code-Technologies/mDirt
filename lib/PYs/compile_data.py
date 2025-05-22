import os
import shutil
import zipfile
import json
from pathlib import Path
from collections import defaultdict

blocks = []
items = []
biomes = []
enchantments = []
blockstates_data = {}

def get_minecraft_files(version: str):
    minecraft_path = (
        f"C:/Users/wiseg/AppData/Roaming/.minecraft/versions/{version}/{version}.jar"
    )

    if not os.path.exists(minecraft_path):
        return

    current_directory = Path(__file__).parent
    zip_path = current_directory / f"{version}.jar"

    shutil.copy(minecraft_path, zip_path)
    zip_file_path = zip_path.with_suffix(".zip")
    os.rename(zip_path, zip_file_path)

    extract_folder = current_directory / "extracted_files"
    extract_folder.mkdir(exist_ok=True)

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    items_path = extract_folder / "assets/minecraft/items"
    blocks_path = extract_folder / "assets/minecraft/blockstates"
    biome_path = extract_folder / "data/minecraft/worldgen/biome"
    enchantment_path = extract_folder / "data/minecraft/enchantment"

    for file in items_path.glob("*.json"):
        items.append(file.name.removesuffix(".json"))

    for file in blocks_path.glob("*.json"):
        block_name = file.name.removesuffix(".json")
        blocks.append(block_name)

        with open(file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue

            variants = data.get("variants", {})
            multipart = data.get("multipart", [])

            state_values = defaultdict(set)

            if variants:
                for variant_key in variants:
                    if variant_key == "":
                        continue
                    pairs = variant_key.split(",")
                    for pair in pairs:
                        key, value = pair.split("=")
                        state_values[key.strip()].add(value.strip())

            elif multipart:
                for part in multipart:
                    when = part.get("when")
                    if isinstance(when, dict):
                        for key, value in when.items():
                            if isinstance(value, list):
                                for v in value:
                                    if isinstance(v, dict):
                                        # Convert dict to JSON string
                                        state_values[key].add(json.dumps(v, sort_keys=True))
                                    else:
                                        state_values[key].add(str(v))
                            else:
                                if isinstance(value, dict):
                                    state_values[key].add(json.dumps(value, sort_keys=True))
                                else:
                                    state_values[key].add(str(value))

            if state_values:
                blockstates_data[block_name] = {
                    key: sorted(list(vals)) for key, vals in state_values.items()
                }

    for file in biome_path.glob("*.json"):
        biomes.append(file.name.removesuffix(".json"))

    for file in enchantment_path.glob("*.json"):
        enchantments.append(file.name.removesuffix(".json"))

    zip_file_path.unlink()
    shutil.rmtree(extract_folder)

    blocks.sort()
    items.sort()
    biomes.sort()
    enchantments.sort()

    with open(f"lib/{version}_data.json", "w") as f:
        json.dump({"blocks": blocks, "items": items, "biomes": biomes, "enchantments": enchantments, "blockstates": blockstates_data}, f, indent=4)


get_minecraft_files("1.21.5")