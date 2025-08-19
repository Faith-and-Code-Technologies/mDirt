import os, shutil, json
from jinja2 import Environment, FileSystemLoader

class StructureGenerator:
    def __init__(self, namespaceDirectory, packNamespace, packAuthor, structures):
        self.namespaceDirectory = namespaceDirectory
        self.packNamespace = packNamespace
        self.packAuthor = packAuthor
        self.structures = structures

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'structure_templates')),
            autoescape=True
        )

    def getTemplate(self, template: str, context: dict):
        temp = self.env.get_template(template)
        return temp.render(context)

    def generate(self):
        # Generate required folders
        os.makedirs(os.path.join(self.namespaceDirectory, "worldgen", "structure"), exist_ok=True)
        os.makedirs(os.path.join(self.namespaceDirectory, "worldgen", "structure_set"), exist_ok=True)
        os.makedirs(os.path.join(self.namespaceDirectory, "worldgen", "template_pool"), exist_ok=True)

        # Create dictionary of `Project Start to Heightmap` things
        psth = {
            'Motion blocking': 'MOTION_BLOCKING',
            'Motion blocking no leaves': 'MOTION_BLOCKING_NO_LEAVES',
            'Ocean floor': 'OCEAN_FLOOR',
            'Ocean floor worldgen': 'OCEAN_FLOOR_WG',
            'World surface': 'WORLD_SURFACE',
            'World surface worldgen': 'WORLD_SURFACE_WG'
        }

        # Loop through all structures
        for structure in self.structures:
            struct = self.structures[structure]

            # Write to worldgen/structure/.json
            content = self.getTemplate('structure.json.j2', {
                'biomes': struct['biomes'],
                'step': struct['step'].replace(' ', '_').lower(),
                'terrain_adaptation': struct['terrain_adaptation'].lower(),
                'namespace': self.packNamespace,
                'name': struct['name'],
                'start_height': struct['start_height'],
                'psth': psth[struct['psth']]
            })

            path = os.path.join(self.namespaceDirectory, "worldgen", "structure", f'{struct['name']}.json')
            with open(path, 'w') as file:
                file.write(content)
            
            # Write to worldgen/structure_set/.json
            content = self.getTemplate('structure_set.json.j2', {
                'namespace': self.packNamespace,
                'name': struct['name'],
                'spacing': struct['spacing'],
                'seperation': struct['seperation']
            })

            path = os.path.join(self.namespaceDirectory, "worldgen", "structure_set", f'{struct['name']}.json')
            with open(path, 'w') as file:
                file.write(content)
            
            # Write to worldgen/template_pool/.json
            content = self.getTemplate('template_pool.json.j2', {
                'namespace': self.packNamespace,
                'name': struct['name']
            })

            path = os.path.join(self.namespaceDirectory, "worldgen", "template_pool", f'{struct['name']}.json')
            with open(path, 'w') as file:
                file.write(content)

            # Copy Structure .nbt
            path = os.path.join(self.namespaceDirectory, 'structure')
            destPath = os.path.join(path, os.path.splitext(os.path.basename(str(struct["structure"])))[-2])
            shutil.copy(struct['structure'], os.path.normpath(f'{destPath}.nbt'))