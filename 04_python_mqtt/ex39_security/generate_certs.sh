#!/usr/bin/env bash
# Exercise 39 - generate a private Certificate Authority and a server certificate
# for local TLS testing. Certificates are written to ./certs (git-ignored).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p certs && cd certs

CN="${1:-localhost}"

# 1) Certificate Authority
openssl req -new -x509 -days 365 -nodes -newkey rsa:2048 \
  -keyout ca.key -out ca.crt -subj "/CN=Training MQTT CA"

# 2) Server key + signing request (CN and SAN must match the host clients connect to)
openssl req -new -nodes -newkey rsa:2048 \
  -keyout server.key -out server.csr -subj "/CN=${CN}"

printf "subjectAltName=DNS:%s,IP:127.0.0.1\n" "$CN" > server.ext

# 3) Sign the server certificate with the CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out server.crt -days 365 -extfile server.ext

chmod 600 ca.key server.key
rm -f server.csr server.ext
echo "Certificates created in $(pwd): ca.crt, server.crt, server.key"
