#! /usr/bin/env python

import requests
import os
import subprocess

TRAVIS_CONTENT = """---
sudo: required
language: python

services:
  - docker

python: "2.7"

virtualenv:
  system_site_packages: false

install:
- pip install --upgrade setuptools
- cd ome-ansible-molecule-dependencies && python setup.py install

script:
# Some roles can't be properly tested in Docker
# These should provide an alternative configuration just for testing syntax
- cd $ROLE
- if [ -f molecule-docker.yml ]; then mv molecule-docker.yml molecule.yml; fi
- ../scripts/test.sh

env:
"""

with open(".travis.yml", "w") as f:
    f.write(TRAVIS_CONTENT)

TESTS_EXCLUSION = {
    "ansible-role-haproxy": "Uses a non-standard test from upstream",
    "ansible-role-munin-node":
        "No molecule.yml or test.yml (tested by munin role)",
    "ansible-role-omero-logmonitor":
        "Molecule test doesn't work",
    "ansible-role-omero-web-apps":
        "Broken (deprecated?)",
}

URL = "https://github.com/openmicroscopy/ome-ansible-molecule-dependencies"
subprocess.call([
    "git", "submodule", "add", URL,'ome-ansible-molecule-dependencies'])


GH_REPOS = 'https://api.github.com/orgs/openmicroscopy/repos?per_page=200'
r = requests.get(GH_REPOS)
for i in r.json():
    if not i['name'].startswith('ansible-role'):
        continue
    subprocess.call(["git", "submodule", "add", i['html_url'], i['name']])
    
    if i['name'] in TESTS_EXCLUSION:
        continue
    with open(".travis.yml", "a") as f:
        f.write(" - ROLE=%s\n" % i['name'])
    
