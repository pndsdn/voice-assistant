import os
import json

SOUND_FOLDER = f'{os.path.join(os.path.dirname(__file__))}/sound/'

COMMANDS = json.loads(open('commands.json', "rb").read())
