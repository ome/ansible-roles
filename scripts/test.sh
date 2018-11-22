#!/usr/bin/env bash

if molecule list -s travis; then
    molecule test -s travis
else
    molecule test --all
fi
