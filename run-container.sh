#!/bin/sh

sudo rkt run \
    --net=host \
    --insecure-options=ondisk,image \
    --volume config,kind=host,source=$(pwd)/dev_settings.py \
    --mount volume=config,target=/app/config.py \
    --volume log-conf,kind=host,source=$(pwd)/dev_log_conf.yaml \
    --mount volume=log-conf,target=/app/dev_log_conf.yaml \
    --set-env=BLAG_CONFIG_FILE=/app/config.py \
    ./build/blag.aci
