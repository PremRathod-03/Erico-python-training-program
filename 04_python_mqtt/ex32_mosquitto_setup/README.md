# Exercise 32 – Setting up an MQTT Broker (Mosquitto)

## Install
| OS | Command |
|---|---|
| macOS | `brew install mosquitto` |
| Ubuntu/Debian | `sudo apt install mosquitto mosquitto-clients` |
| Windows | installer from https://mosquitto.org/download/ (adds `mosquitto`, `mosquitto_pub`, `mosquitto_sub`) |

## Run the broker
```bash
cd 04_python_mqtt/ex32_mosquitto_setup
mkdir -p mosquitto_data
mosquitto -c mosquitto.conf -v          # -v = verbose, shows every connect/publish
```
On macOS you can also run it as a background service with `brew services start mosquitto`. Homebrew's config lives at `/opt/homebrew/etc/mosquitto/mosquitto.conf`.

## Test with the command-line tools
Terminal 1 – subscribe:
```bash
mosquitto_sub -h localhost -t test/topic -v
```
Terminal 2 – publish:
```bash
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
```
Terminal 1 prints `test/topic Hello MQTT`.

Useful flags:
- `-q 1` sets QoS, `-r` sends a retained message, `-d` prints debug output for every packet
- `mosquitto_sub -t '#' -v` subscribes to everything (handy for debugging)

## Docker alternative
```bash
docker run -it -p 1883:1883 -v "$PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf" eclipse-mosquitto
```
For Docker, change `listener 1883 localhost` to `listener 1883` so the broker accepts connections from outside the container.
