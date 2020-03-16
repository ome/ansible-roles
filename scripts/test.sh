#!/usr/bin/env bash

if [[ -d molecule ]]; then
    if [[ -z $SCENARIO ]]; then
        molecule test --all
    else
        molecule test -s $SCENARIO
    fi
else
    ### From .travis.yml of the non-molecule roles
    # Create ansible.cfg with correct roles_path
    printf '[defaults]\nroles_path=../' >ansible.cfg
    # Basic role syntax check
    ansible-playbook tests/test.yml -i tests/inventory --syntax-check
fi