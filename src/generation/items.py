class ItemGenerator:
    def __init__(self, header, namespaceDirectory, items):
        self.header = header
        self.namespaceDirectory = namespaceDirectory
        self.items = items

    def generate(self):
        with open(f"{self.namespaceDirectory}\\function\\give_items.mcfunction", "a") as file:
            file.write(self.header)
            for item in self.items:
                file.write(f'give @s {self.items[item]["baseItem"]}[item_name=\'{{"italic":false,"text":"{self.items[item]["displayName"]}"}}\',custom_model_data={self.items[item]["cmd"]}] 1\n')