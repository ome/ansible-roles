#! /usr/bin/env python

import requests
import os
import subprocess


URL = "https://github.com/openmicroscopy/ome-ansible-molecule-dependencies"
subprocess.call([
    "git", "submodule", "add", URL,'ome-ansible-molecule-dependencies'])

GH_REPOS = 'https://api.github.com/orgs/openmicroscopy/repos?per_page=200'
r = requests.get(GH_REPOS)
for i in r.json():
    if not i['name'].startswith('ansible-role'):
        continue
    subprocess.call(["git", "submodule", "add", i['html_url'], i['name']])
