#!/bin/sh

# Configure git
git config --global user.email "travis@thusoy.com"
git config --global user.name "Tarjei Husøy (via Travis CI)"

./tools/travis-decrypt-ssh-key.sh
