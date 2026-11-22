# Exercise 39 – Securing MQTT Communication

Goal: the broker **requires a username/password** and **encrypts traffic with TLS**.

```bash
cd 04_python_mqtt/ex39_security
chmod +x *.sh
./create_password_file.sh iotuser      # prompts for a password and writes ./passwd (hashed)
./generate_certs.sh                    # CA + server certificate in ./certs
mosquitto -c mosquitto_secure.conf -v  # TLS on 8883, password-only plain listener on 1884
```

## Test the setup
CLI:
```bash
# correct credentials over TLS
mosquitto_sub -h localhost -p 8883 --cafile certs/ca.crt -u iotuser -P '<password>' -t secure/test -v
mosquitto_pub -h localhost -p 8883 --cafile certs/ca.crt -u iotuser -P '<password>' -t secure/test -m hi
# anonymous -> "Connection error: Connection Refused: not authorised."
mosquitto_pub -h localhost -p 1884 -t secure/test -m hi
```
Python:
```bash
export MQTT_USER=iotuser MQTT_PASSWORD='<password>'
python secure_client.py           # Secure round trip: SUCCESS
python secure_client.py --wrong   # Connection refused: Not authorized
```

## What each setting does
| Setting | Purpose |
|---|---|
| `allow_anonymous false` | Rejects clients that do not send credentials |
| `password_file` | Hashed usernames/passwords created with `mosquitto_passwd` |
| `listener 8883` + `cafile/certfile/keyfile` | TLS-encrypted listener (8883 is the standard MQTTS port) |
| `tls_version tlsv1.2` | Refuses older, insecure TLS versions |
| `require_certificate true` | Optional mutual TLS: clients also need a certificate signed by the CA |

> If you start Mosquitto as root (for example via `sudo` or inside Docker), it switches to the `mosquitto` user and can no longer read a `600` password file owned by you. Either `chown mosquitto passwd certs/server.key`, or add `user root` for local testing only.

`passwd` and `certs/` are git-ignored, so keys and password hashes never reach GitHub.
