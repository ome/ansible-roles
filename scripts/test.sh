#!/usr/bin/env bash

if [ -d molecule/travis ]; then
    molecule test -s travis
else
    molecule test
fi
