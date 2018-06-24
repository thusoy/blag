#!/usr/bin/env bash

set -eu

openssl aes-256-cbc -md sha256 -d -base64 -in <(cat <<EOF
U2FsdGVkX19jCcd7R4R9vpqEAEQ+1rtat+G16wcAhSXUJ5p9w0qv3aryGTES2HlV
kceLK/Nf7IMtZ5nc1JCM5wrMkhGW6Ufjev/KrpWHw73ZYbEX1OH0RlN6cCkvuOKg
nbAPAbH5p+wwMwAiSHO2gGJDUn0ZYvFiLtprsJ+whMvRfL4Wqiykk+tLCkYFBquD
zXAQO1qFbozFRPIwSRZODHXBuCxD8C/Pg1lJRrbqIWkIzGjiKCv9j7nGDRIwoCI8
e66QuhvK/GhFklS/F0+57W8FBF1YI045CQhiUjUOwdVCv+/ofDOTv3FK0bFO3vHL
dUmdGER7/20F7vWtHfMQ/J2COmKHOOe4AES6pI88r+nWM4gAnw+FuL5R/cDwHBzz
6msoCProhOsvFMMj44CCdG3gB5mvE/nXlZveie/HiXpgZyr608T5HP8Bd4GcZqik
ufrprW1Oc5H4e+IpkMFroDG5Zqw89lW5LmpmUO4DDDX79F+ZqFZWVa4EjlzJvCET
Zdx+Rb95liJGr2zmgQoULxZQPjRVu6+2tJeXzzOIwJs=
EOF
) -out ~/.ssh/id_ed25519 -k "$DEPLOY_KEY_SECRET"

chmod 400 ~/.ssh/id_ed25519
