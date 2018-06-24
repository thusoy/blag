#!/usr/bin/env bash

set -eu

version_tag=$(git rev-parse --short=20 HEAD)

main () {
    pull_notes
    add_git_note
    # upload_artifact
    # push_git_notes
}


pull_notes () {
    git fetch origin "refs/notes/*:refs/notes/*"
}


add_git_note () {
    git notes --ref=artifacts add -F <(cat <<EOF
ACI/url: https://thusoy-artifacts.s3.amazonaws.com/blag/blag-$version_tag.aci
ACI/sha256: $(shasum -a 256 build/blag.aci | cut -d' ' -f1)
EOF
    )
}


push_git_notes () {
    git push origin refs/notes/*
}


upload_artifact () {
    aws s3 cp \
        build/blag.aci \
        "s3://thusoy-artifacts/blag/blag-$version_tag.aci" \
        --acl public-read
}


main
