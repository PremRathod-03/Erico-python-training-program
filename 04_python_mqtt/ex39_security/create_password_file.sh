#!/usr/bin/env bash
# Exercise 39 - create the Mosquitto password file with one user.
# Usage: ./create_password_file.sh [username]   (you will be prompted for the password)
set -euo pipefail
cd "$(dirname "$0")"

USERNAME="${1:-iotuser}"
# -c creates/overwrites the file; passwords are stored as salted hashes
mosquitto_passwd -c ./passwd "$USERNAME"
chmod 600 ./passwd
echo "Created ./passwd for user '$USERNAME'"
