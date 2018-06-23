#!/bin/sh

# Produce an ACI image (eventually an OCI bundle when rkt can run those)

set -eu

rm -rf build

sudo docker build -t localhost:5000/blag .
registry_container_id=$(sudo docker run -d --rm --network=host registry)
trap 'sudo docker kill "$registry_container_id"' INT TERM EXIT

start_time=$(date +'%s')
while :; do
    curl localhost:5000 -s && break || echo "Failed to connect to registry, retrying"
    sleep 1
    # Add 1 since expr exits with an error if the return is 0
    if [ "$(expr "$(date +'%s')" - "$start_time" + 1)" -gt 61 ]; then
        echo 'Failed to connect to local registry, aborting' >&2
        exit 1
    fi
done

sudo docker push localhost:5000/blag

docker2aci --insecure-allow-http docker://localhost:5000/blag
mkdir -p build
mv blag-latest.aci build/blag.aci
