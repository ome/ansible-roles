#!/usr/bin/env bash

if [[ -f molecule.yml ]];
then
    molecule test
else
    ### From .travis.yml of the non-molecule roles
    # Create ansible.cfg with correct roles_path
    printf '[defaults]\nroles_path=../' >ansible.cfg
    # Basic role syntax check
    ansible-playbook tests/test.yml -i tests/inventory --syntax-check
fi