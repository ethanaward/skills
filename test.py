import os
from shutil import copytree
import pprint
import glob

skills = [name for name in os.listdir(os.path.dirname(__file__))
            if os.path.isdir(os.path.join(os.path.dirname(__file__), name)) and not '.' in name]

for skill in skills:
    copytree(skill, os.path.join(os.path.dirname(__file__), 'mycroft-core', skill))

pprint.pprint(skills)