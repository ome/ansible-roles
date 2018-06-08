#! /usr/bin/env python

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
- pip install ome-ansible-molecule-dependencies/

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
    "ansible-role-omero-logmonitor": "Molecule test doesn't work",
    "ansible-role-omero-web-apps": "Broken (deprecated?)",
    "ansible-role-devspace": "",
    "ansible-role-docker": "",
    "ansible-role-celery-docker": "",
    "ansible-role-prometheus": "",
    "ansible-role-nginx-ssl-selfsigned": "Deprecated",
}

URL = "https://github.com/openmicroscopy/ome-ansible-molecule-dependencies"
subprocess.call([
    "git", "submodule", "add", URL, 'ome-ansible-molecule-dependencies'])


GH_SEARCH_API = 'https://api.github.com/search/repositories'
GH_REPOS = GH_SEARCH_API + '?q=ansible-role+in:file+org:openmicroscopy'


def get_repos():
    response = requests.get(GH_REPOS)
    repos = response.json()['items']
    while 'next' in response.links.keys():
        response = requests.get(response.links['next']['url'])
        repos.extend(response.json()['items'])
    return repos


for repo in get_repos():
    subprocess.call([
        "git", "submodule", "add", repo['html_url'], repo['name']])

    if repo['name'] in TESTS_EXCLUSION:
        continue
    with open(".travis.yml", "a") as f:
        f.write(" - ROLE=%s\n" % repo['name'])

subprocess.call([
    "git", "submodule", "update",  "--remote"])
