#!/usr/bin/env bash

set -eu

openssl aes-256-cbc -d -in <(cat <<EOF | base64 -d
U2FsdGVkX19EdxCWB9DkrTCbG7Dtzx3AgWgkwJ5ljT8yIqMmK2Ivxcd9mBOZI2E0+U6cFwNTGM9F
ROF6bT9pWh3ILPy+atERqRq76xPfZzS49jr9g6vUxQrPRJUcWRIxyOWqr5vjsXgEM+dBYROlCo8B
R22d+8sIvDwLdM2mmJrsFgElVTIIlp3gYe7lgoeEzL2oC4cXI86nU3OH0bCUxkaf7wMUFC6a68Eg
7VbXRC3BTT/HbnCXDGazsxEz9e3FujuvHMeT1Eer8MMYLbYK9tJndoK0/VZ+a51lBf18dzcRDJFX
ZAgXE1zgkPZ8XcwyT01A2SuUEB33KaP7ZXNNXK8J+mRcgzk6gl6W+W3EtqvX1laxCI3Wn1khRf1L
19jdbFkF/uwq6/u+rbdGU74btVlQExF7xHOhNg0a9vyBft6ngz7e4Dc9fiIEB86Ko4Jb7+qnF5kq
Tdzq1v3O9+8fWCgIN1aCF5J84PNkrgs/twuhss0JqFeCqGZoWFKnnMSOMkcj1V+qib+Zw3BmGlN4
yc0QSPXYgxXWOS3Txh4f/ns=
EOF
) -out ~/.ssh/id_ed25519 -k "$DEPLOY_KEY_SECRET"

chmod 400 ~/.ssh/id_ed25519
