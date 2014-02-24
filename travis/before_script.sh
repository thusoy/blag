#!/bin/sh

# Configure git
git remote set-url origin $REPO.git
git config --global user.email "tarjei@roms.no"
git config --global user.name "Tarjei Husøy (via Travis CI)"

# Install aws cli and configure
pip install awscli

mkdir ~/.aws
echo "[default]
aws_access_key_id = $TRAVIS_IAM_ACCESS_ID
aws_secret_access_key = $TRAVIS_IAM_ACCESS_KEY
region = eu-west-1
" > ~/.aws/config
