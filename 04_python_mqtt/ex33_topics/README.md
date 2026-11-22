# Exercise 33 – MQTT Topics and Messages

## Smart-home topic structure
```
home/
├── living-room/
│   ├── temperature
│   ├── humidity
│   └── light/state
├── kitchen/
│   ├── temperature
│   └── smoke
├── bedroom/
│   ├── temperature
│   └── light/state
└── garage/
    └── door/state
```
Conventions: lowercase, `-` inside words, no leading `/`, no spaces, and the most general level first (`home/<room>/<device>/<property>`).

## Wildcards
| Subscription | Matches | Does not match |
|---|---|---|
| `home/+/temperature` | `home/kitchen/temperature`, `home/bedroom/temperature` | `home/kitchen/smoke` |
| `home/+/light/state` | every room's light state | `home/kitchen/temperature` |
| `home/kitchen/#` | everything under kitchen | `home/bedroom/temperature` |
| `home/#` | every smart-home topic | `office/temperature` |

- `+` matches **exactly one** level and can appear anywhere.
- `#` matches **zero or more** levels and must be the last character.

`topics.py` checks these rules with paho's `topic_matches_sub()`, then publishes to every topic and subscribes with `home/+/temperature` and `home/kitchen/#` against a live broker.

With the CLI tools:
```bash
mosquitto_sub -t 'home/+/temperature' -v
mosquitto_pub -t home/living-room/temperature -m 24.5
```
