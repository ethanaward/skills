# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


import imp
import time

import abc
import os.path
import re
from adapt.intent import Intent
from os.path import join, dirname, splitext, isdir


__author__ = 'seanfitz'

PRIMARY_SKILLS = ['intent', 'wake']
BLACKLISTED_SKILLS = ["send_sms", "media"]
SKILLS_BASEDIR = dirname(__file__)
THIRD_PARTY_SKILLS_DIR = "/opt/mycroft/third_party"

MainModule = '__init__'



def load_skill(skill_descriptor, emitter):
    try:
        skill_module = imp.load_module(
            skill_descriptor["name"] + MainModule, *skill_descriptor["info"])
        if (hasattr(skill_module, 'create_skill') and
                callable(skill_module.create_skill)):
            # v2 skills framework
            skill = skill_module.create_skill()
            skill.bind(emitter)
            skill.initialize()
            return skill
        else:
            pass
    except:
        pass
    return None


def get_skills(skills_folder):
    skills = []
    possible_skills = os.listdir(skills_folder)
    for i in possible_skills:
        location = join(skills_folder, i)
        if (not isdir(location) or
                not MainModule + ".py" in os.listdir(location)):
            continue

        skills.append(create_skill_descriptor(location))
    skills = sorted(skills, key=lambda p: p.get('name'))
    return skills


def create_skill_descriptor(skill_folder):
    info = imp.find_module(MainModule, [skill_folder])
    return {"name": os.path.basename(skill_folder), "info": info}


def load_skills(emitter, skills_root=SKILLS_BASEDIR):
    skills = get_skills(skills_root)
    for skill in skills:
        if skill['name'] in PRIMARY_SKILLS:
            load_skill(skill, emitter)

    for skill in skills:
        if (skill['name'] not in PRIMARY_SKILLS and
                skill['name'] not in BLACKLISTED_SKILLS):
            load_skill(skill, emitter)


