import os
import shutil
import zipfile
import json
from pathlib import Path
import requests as rs

def get_minecraft_files(version: str):
    user_name = os.getlogin()
    minecraft_path = f"C:/Users/{user_name}/AppData/Roaming/.minecraft/versions/{version}/{version}.jar"

    if not os.path.exists(minecraft_path):
        return

    current_directory = Path(__file__).parent
    zip_path = current_directory / f"{version}.jar"

    shutil.copy(minecraft_path, zip_path)
    zip_file_path = zip_path.with_suffix(".zip")
    os.rename(zip_path, zip_file_path)

    extract_folder = current_directory / 'FileSsSsS'
    extract_folder.mkdir(exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    models_item_path = extract_folder / "assets/minecraft/models/item"

    if not models_item_path.exists():
        return

    item_dict = {}


    for file in models_item_path.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'parent' in data:
            item_dict[f"minecraft:{file.stem}"] = data

    zip_file_path.unlink()
    shutil.rmtree(extract_folder)

    return item_dict

def get_minecraft_items_and_blocks(version: str):
    blocks_response = rs.get(f'https://raw.githubusercontent.com/PrismarineJS/minecraft-data/refs/heads/master/data/pc/{version}/blocks.json')
    blocks = json.loads(blocks_response.text)
    items_response = rs.get(f'https://raw.githubusercontent.com/PrismarineJS/minecraft-data/refs/heads/master/data/pc/{version}/items.json')
    items = json.loads(items_response.text)

    blocks_parsed = []
    items_parsed = []

    for block in blocks:
        if block["name"] != 'air': blocks_parsed.append(block["name"])

    for item in items:
        if item["name"] != 'air': items_parsed.append(item["name"])

    return blocks_parsed, items_parsed

def write_to_json(models: dict, blocks: list, items: list):
    with open(f'data.json', 'w') as f:
        json.dump({"models": models, "blocks": blocks, "items": items}, f, indent=4)

def make_data():
    latest_unparsed = rs.get("https://raw.githubusercontent.com/PrismarineJS/minecraft-data/refs/heads/master/data/pc/latest/proto.yml")
    content = latest_unparsed.text
    for line in content.splitlines():
        if line.startswith('!version:'):
            version = line.split('!version: ')[1].strip()
            print(version)
            break

    models = get_minecraft_files(version)
    blocks, items = get_minecraft_items_and_blocks(version)
    write_to_json(models, blocks, items)

make_data()