# Module 4 – Python MQTT

| # | Topic | Files |
|---|---|---|
| 31 | Introduction to MQTT | `ex31_mqtt_vs_http/report.md` |
| 32 | Setting up an MQTT broker | `ex32_mosquitto_setup/` (README + `mosquitto.conf`) |
| 33 | Topics and messages | `ex33_topics/` (smart-home topic tree, `+`/`#` wildcards) |
| 34 | MQTT Explorer | `ex34_mqtt_explorer/` (GUI steps + `explorer_check.py`) |
| 35 | MQTT publisher | `ex35_publisher/publisher.py` |
| 36 | MQTT subscriber | `ex36_subscriber/subscriber.py` |
| 37 | Callbacks | `ex37_callbacks/subscriber_callbacks.py` |
| 38 | QoS levels | `ex38_qos/qos_demo.py` (prints the packet flow per QoS) |
| 39 | Securing MQTT | `ex39_security/` (password file, TLS certs, secure config, client) |
| 40 | MQTT in IoT | `ex40_iot_sensor/` (sensor simulator + real-time logger) |
| 41 | Integrating MQTT with Python | `ex41_integration/` (QoS pub/sub + threaded queue workers) |
| MP7 | Mini-Project 7 | `mini_project_7_mqtt_pubsub/` (random-data publisher + display subscriber) |

All scripts use **paho-mqtt 2.x** (`CallbackAPIVersion.VERSION2`) and connect to `localhost:1883`. You can override this with `--host/--port` or the `MQTT_HOST` / `MQTT_PORT` environment variables.

## Run everything
```bash
brew install mosquitto
mosquitto -v                                   # terminal 1: broker

# terminal 2
python ex33_topics/topics.py
python ex34_mqtt_explorer/explorer_check.py
python ex36_subscriber/subscriber.py --duration 20 &
python ex35_publisher/publisher.py
python ex37_callbacks/subscriber_callbacks.py --duration 10
python ex38_qos/qos_demo.py
python ex40_iot_sensor/sensor_logger.py &      # then:
python ex40_iot_sensor/sensor_simulator.py --count 10 --interval 1
python ex41_integration/qos_pub_sub.py
python ex41_integration/concurrent_subscriber.py --demo

# Mini-Project 7 (two terminals)
python mini_project_7_mqtt_pubsub/subscriber.py
python mini_project_7_mqtt_pubsub/publisher.py --count 20
```
Offline unit tests: `python -m unittest discover -s tests -v`
