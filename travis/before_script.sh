#!/bin/sh

# Configure git
git remote set-url origin $REPO.git
git config --global user.email "tarjei@roms.no"
git config --global user.name "Tarjei Husøy (via Travis CI)"

# Install aws cli and configure
pip install awscli
echo > ~/.aws/config <<aws-iam-config
[default]
aws_access_key_id = $S3_ACCESS_ID
aws_secret_access_key = $S3_ACCESS_KEY
region = eu-west-1
aws-iam-config
