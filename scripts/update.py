#! /usr/bin/env python

import os.path
import requests
import subprocess

TRAVIS_CONTENT = """---
sudo: required
language: python

services:
  - docker

python: "2.7"

cache: pip

virtualenv:
  system_site_packages: false

install:
- pip install --upgrade setuptools
- pip install ome-ansible-molecule/

script:
- cd $ROLE && ../scripts/test.sh

env:
"""

with open(".travis.yml", "w") as f:
    f.write(TRAVIS_CONTENT)

TESTS_EXCLUSION = {
    "ansible-role-debug-dumpallvars": "broken",
    "ansible-role-munin-node":
        "No molecule.yml or test.yml (tested by munin role)",
    "ansible-role-omero-logmonitor": "Molecule test doesn't work",
    "ansible-role-omero-web-apps": "Broken (deprecated?)",
    "ansible-role-devspace": "Docker/docker",
    "ansible-role-docker":
        "docker_version used in molecule no longer available",
    "ansible-role-celery-docker": "Docker/docker",
    "ansible-role-prometheus": "",
    "ansible-role-nginx-ssl-selfsigned": "Deprecated",
    "ansible-role-jekyll-build": "Deprecated",
    "ome-ansible-molecule": "Meta package",
}

subprocess.call(["git", "submodule", "init"])

URL = "https://github.com/openmicroscopy/ome-ansible-molecule"
subprocess.call([
    "git", "submodule", "add", URL, 'ome-ansible-molecule'])


GH_SEARCH_API = 'https://api.github.com/search/repositories'
GH_REPOS = GH_SEARCH_API + '?q=ansible-role+in:name+archived:false+fork:true+user:openmicroscopy'

def get_repos():
    response = requests.get(GH_REPOS)
    repos = response.json()['items']
    while 'next' in response.links.keys():
        response = requests.get(response.links['next']['url'])
        repos.extend(response.json()['items'])
    return repos


for repo in sorted(get_repos()):
    subprocess.call([
        "git", "submodule", "add", repo['html_url'], repo['name']])
    subprocess.call([
        "git", "submodule", "update",  "--remote", repo['name']])
    if repo['name'] in TESTS_EXCLUSION:
        continue
    if not os.path.exists(os.path.join(repo['name'], 'molecule')):
        continue
    with open(".travis.yml", "a") as f:
        f.write(" - ROLE=%s\n" % repo['name'])

