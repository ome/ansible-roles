#! /usr/bin/env python

import requests
import subprocess
import glob
import os

TRAVIS_CONTENT = """---
os: linux
dist: xenial
language: python
python: "3.6"

services:
  - docker

install:
 - pip install --upgrade setuptools
 - pip install ome-ansible-molecule/

script:
 - cd $ROLE && ../scripts/test.sh

jobs:
  allow_failures:
  - env: ROLE=ansible-role-python3-virtualenv SCENARIO=interpreter-py3
  - env: ROLE=ansible-role-certbot SCENARIO=
  - env: ROLE=ansible-role-docker SCENARIO=default
  - env: ROLE=ansible-role-munin-node SCENARIO=

env:
"""

with open(".travis.yml", "w") as f:
    f.write(TRAVIS_CONTENT)

subprocess.call(["git", "submodule", "init"])

URL = "https://github.com/ome/ome-ansible-molecule"
subprocess.call([
    "git", "submodule", "add", URL, 'ome-ansible-molecule'])


GH_SEARCH_API = ('https://api.github.com/search/repositories'
                 '?q=ansible-role-+in:name+org:ome+fork:true')


def get_repos():
    response = requests.get(GH_SEARCH_API)
    repos = response.json()['items']
    while 'next' in response.links.keys():
        response = requests.get(response.links['next']['url'])
        repos.extend(response.json()['items'])
    return repos


for repo in sorted(get_repos(), key=lambda k: k['name']):
    if repo['name'] == 'ansible-roles':
        continue

    subprocess.call([
        "git", "submodule", "add", repo['html_url'], repo['name']])
    if repo['archived']:
        continue

    molecule_files = glob.glob("%s/molecule/*/molecule.yml" % repo['name'])
    if len(molecule_files) is 0:
        with open(".travis.yml", "a") as f:
            f.write(" - ROLE=%s SCENARIO=\n" % repo['name'])
    else:
        for molecule_file in molecule_files:
            scenario = os.path.basename(os.path.dirname(molecule_file))
            with open(".travis.yml", "a") as f:
                f.write(" - ROLE=%s SCENARIO=%s\n" % (repo['name'], scenario))
