#!/bin/sh

TEST_COMMAND="./test --stop --failed"

$TEST_COMMAND

./venv/bin/watchmedo shell-command \
    --patterns="*.py;*.html" \
    --recursive \
    --command "$TEST_COMMAND" \
    blag/ tools/
