import json

async def get_default_lines(self, ctx):
    filepath = self.path / 'default_lines.json'
    with open(filepath) as json_file:
        return(json.load(json_file))