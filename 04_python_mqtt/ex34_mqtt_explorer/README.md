# Exercise 34 – MQTT Explorer

[MQTT Explorer](https://mqtt-explorer.com/) is a GUI client that shows every topic on a broker as a live tree.

## Steps
1. Install: `brew install --cask mqtt-explorer` (macOS) or download it from mqtt-explorer.com.
2. Start your local broker (Exercise 32): `mosquitto -c ../ex32_mosquitto_setup/mosquitto.conf -v`
3. In MQTT Explorer, create a connection:
   - Name: `Local Mosquitto`
   - Protocol: `mqtt://`, Host: `localhost`, Port: `1883`
   - Click **ADVANCED** to check the default subscriptions (`#` and `$SYS/#`), then **CONNECT**.
4. **Publish**: in the right panel, set Topic `test/explorer`, choose `raw` or `json`, enter `Hello from MQTT Explorer`, set QoS, then click **PUBLISH**.
5. **Subscribe/see the message**: the topic `test/explorer` appears in the tree with the payload, history and a diff of value changes.
6. Run `python explorer_check.py` to publish from Python. The JSON message shows up in the Explorer tree under `test/explorer`, and the script prints the copy it receives back.

No GUI available? The public test broker `test.mosquitto.org:1883` works the same way. Run `MQTT_HOST=test.mosquitto.org python explorer_check.py` and use a unique topic.
