#! /usr/bin/env python

import requests
import subprocess


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
