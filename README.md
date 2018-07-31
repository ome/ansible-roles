Ansible roles
=============

[![Build Status](https://travis-ci.org/ome/ansible-roles.svg)](https://travis-ci.org/ome/ansible-roles)


A super-repository collecting of all the existing OME Ansible roles including
those released on [Galaxy](http://galaxy.ansible.com/openmicroscopy/).

Update
------

The [update.py](scripts/update.py) script allows to add new Ansible roles as
submodules as well as updating existing submodules to track the `master`
branch. From the top-level repository: run

    $ python scripts/update.py
