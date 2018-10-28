#!/usr/bin/env bash

set -eu

version_tag=$(git rev-parse --short=20 HEAD)

main () {
    pull_notes
    add_git_note
    upload_artifact
    push_git_notes
}


pull_notes () {
    # Notes are not pulled automatically by Travis, thus we have to pull them
    # ourselves to ensure we've got the latest before we start adding some.
    # The notes ref was added by ./configure, so a fetch is enough.
    git fetch origin
}


add_git_note () {
    git notes --ref=artifacts add -F <(cat <<EOF
ACI/url: https://thusoy-artifacts.s3.amazonaws.com/blag/blag-$version_tag.aci
ACI/sha256: $(shasum -a 256 build/blag.aci | cut -d' ' -f1)
EOF
    )
}


push_git_notes () {
    GIT_SSH="ssh -i ~/.ssh/id_ed25519" git push git@github.com:thusoy/blag refs/notes/*
}


upload_artifact () {
    aws s3 cp \
        build/blag.aci \
        "s3://thusoy-artifacts/blag/blag-$version_tag.aci" \
        --acl public-read
}


main
