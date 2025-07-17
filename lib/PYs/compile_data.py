import os
import shutil
import zipfile
import json
from pathlib import Path
from collections import defaultdict, OrderedDict
import platform

def infer_jsonschema_type(values):
    if all(v in ("true", "false") for v in values):
        return "boolean", None
    return "string", sorted(values)

def get_sounds_json(target_version=None):
    system = platform.system()
    if system == "Windows":
        mc_assets = os.path.expandvars(r"%APPDATA%\.minecraft\assets")
    elif system == "Darwin":
        mc_assets = os.path.expanduser(r"~/Library/Application Support/minecraft/assets")
    else:
        mc_assets = os.path.expanduser(r"~/.minecraft/assets")

    index_dir = os.path.join(mc_assets, "indexes")
    versions = [f for f in os.listdir(index_dir) if f.endswith(".json")]

    if target_version:
        index_file = target_version + ".json"
        if index_file not in versions:
            print(f"Version {target_version} not found. Available: {[v.rstrip('.json') for v in versions]}")
            return
    else:
        index_file = max(versions, key=lambda v: (v != "pre-1.6", v))

    index_path = os.path.join(index_dir, index_file)

    with open(index_path, "r") as f:
        data = json.load(f)

    entry = "minecraft/sounds.json"
    if entry in data["objects"]:
        h = data["objects"][entry]["hash"]
        src = os.path.join(mc_assets, "objects", h[:2], h)
        dst = os.path.join(os.path.dirname(__file__), "sounds.json")
        shutil.copyfile(src, dst)
        print(f"Copied sounds.json from {index_file} to {dst}")
    else:
        print("sounds.json not found in index.")

blocks = []
items = []
biomes = []
enchantments = []
blockstates_data = {}
effects = []
damage_types = []
sound_events = []
entities = []
game_events = []

def get_minecraft_files(version: str, soundver: str):
    if platform.system() == "Windows":
        base_path = os.path.expandvars(r"%APPDATA%\.minecraft")
    elif platform.system() == "Darwin":
        base_path = os.path.expanduser("~/Library/Application Support/minecraft")
    else:
        base_path = os.path.expanduser("~/.minecraft")

    minecraft_path = os.path.join(base_path, "versions", version, f"{version}.jar")


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

    get_sounds_json(target_version=soundver)

    items_path = extract_folder / "assets/minecraft/items"
    blocks_path = extract_folder / "assets/minecraft/blockstates"
    biome_path = extract_folder / "data/minecraft/worldgen/biome"
    enchantment_path = extract_folder / "data/minecraft/enchantment"
    effects_path = extract_folder / "assets/minecraft/textures/mob_effect"
    damage_types_path = extract_folder / "data/minecraft/damage_type"
    sounds_json_path = Path(__file__).parent / "sounds.json"
    entity_path = extract_folder / "assets/minecraft/textures/entity" # top level folders & .pngs
    vibrations_file = extract_folder / "data/minecraft/tags/game_event/vibrations.json"


    for file in items_path.glob("*.json"):
        items.append(file.name.removesuffix(".json"))

    blockstates_schema = {}

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
                                        state_values[key].add(json.dumps(v, sort_keys=True))
                                    else:
                                        state_values[key].add(str(v))
                            else:
                                if isinstance(value, dict):
                                    state_values[key].add(json.dumps(value, sort_keys=True))
                                else:
                                    state_values[key].add(str(value))

            if state_values:
                properties = OrderedDict()
                for key, values in sorted(state_values.items()):
                    inferred_type, enum_vals = infer_jsonschema_type(values)
                    schema = {"type": inferred_type}
                    if enum_vals:
                        schema["enum"] = enum_vals
                    properties[key] = schema

                blockstates_schema[block_name] = {
                    "type": "object",
                    "properties": properties,
                    "required": []
                }

    for file in biome_path.glob("*.json"):
        biomes.append(file.name.removesuffix(".json"))

    for file in enchantment_path.glob("*.json"):
        enchantments.append(file.name.removesuffix(".json"))

    for file in effects_path.glob("*.png"):
        effects.append(file.name.removesuffix(".png"))
    
    for file in damage_types_path.glob("*.json"):
        damage_types.append(file.name.removesuffix(".json"))

    if sounds_json_path.exists():
        with open(sounds_json_path, "r") as f:
            try:
                sound_data = json.load(f)
                sound_events.extend(sound_data.keys())
            except json.JSONDecodeError:
                print("Failed to parse sounds.json.")

    for item in entity_path.iterdir():
        if item.is_dir():
            entities.append(item.name)
        elif item.is_file() and item.suffix == ".png":
            entities.append(item.name.removesuffix(".png"))

    with open(vibrations_file, "r") as f:
        try:
            data = json.load(f)
            if isinstance(data.get("values"), list):
                game_events.extend(data["values"])
        except json.JSONDecodeError:
            print(f"Failed to parse {vibrations_file}")

    zip_file_path.unlink()
    sounds_json_path.unlink()
    shutil.rmtree(extract_folder)

    blocks.sort()
    items.sort()
    biomes.sort()
    enchantments.sort()
    effects.sort()
    damage_types.sort()
    sound_events.sort()
    entities.sort()
    game_events.sort()

    with open(f"lib/{version}_data.json", "w") as f:
        json.dump({
            "blocks": blocks,
            "items": items,
            "biomes": biomes,
            "enchantments": enchantments,
            "effects": effects,
            "damage_types": damage_types,
            "sound_events": sound_events,
            "entities": entities,
            "game_events": game_events
        }, f, indent=4)
    
    blockstate_oneof = {
        "definitions": {
            "blockStates": {
                "oneOf": []
            }
        }
    }

    blockstate_oneof = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "definitions": {
            "blockStates": {
                "oneOf": []
            }
        }
    }

    for block_name in blocks:
        state_schema = blockstates_schema.get(block_name)

        if state_schema:
            # Block has defined state properties
            properties_schema = {
                **state_schema,
                "additionalProperties": False
            }
        else:
            # Block has no states — allow empty object only
            properties_schema = {
                "type": "object",
                "maxProperties": 0
            }

        wrapped_schema = {
            "type": "object",
            "properties": {
                "block": {
                    "type": "string",
                    "title": "Block",
                    "const": block_name
                },
                "properties": properties_schema
            },
            "required": ["block"],
            "additionalProperties": False
        }

        blockstate_oneof["definitions"]["blockStates"]["oneOf"].append(wrapped_schema)

    # Save full version (detailed oneOf)
    #with open(f"lib/{version}_blockstates.json", "w") as f:
        #json.dump(blockstate_oneof, f, indent=4)

    # Save simple original version (just definitions)
    blockstates_simple = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "definitions": {
            "blockStates": blockstates_schema
        }
    }

    #with open(f"lib/{version}_blockstates_simple.json", "w") as f:
        #json.dump(blockstates_simple, f, indent=4)

# 1.21.4 = 19
# 1.21.5 = 24
# 1.21.6/1.21.7/1.21.8 = 26 <- this file is NOT the same for 1.21.6 and 7 versions though!
# We have NO IDEA why Mojang names their sounds this way.
get_minecraft_files("1.21.8", "26")