# Exercise 31 – MQTT vs HTTP

**MQTT** (Message Queuing Telemetry Transport) is a lightweight **publish/subscribe** protocol. Clients keep one long-lived TCP connection to a central **broker**. Publishers send messages to hierarchical **topics** (for example `home/living-room/temperature`), and the broker pushes each message to every client subscribed to that topic, so senders and receivers never talk directly. The fixed header is only 2 bytes, delivery guarantees are chosen per message through three **QoS levels** (0 at most once, 1 at least once, 2 exactly once), and the protocol includes **retained messages**, **persistent sessions**, and a **Last Will and Testament** that announces when a device drops off unexpectedly. **HTTP**, by contrast, is a **request/response** protocol. A client opens a connection, sends a request with text headers that are often hundreds of bytes, and the server replies. Communication is one-to-one and client-initiated, and the server cannot push data unless you add polling, long-polling, WebSockets or Server-Sent Events. Reliability comes from TCP plus whatever retry logic the application implements.

**MQTT is preferred** when many constrained devices must exchange small, frequent messages over unreliable or low-bandwidth networks: IoT sensor telemetry, smart-home control, industrial monitoring (IIoT), vehicle and fleet tracking, and mobile push notifications. Its persistent connection and tiny overhead save battery and data, the broker decouples thousands of devices, and QoS levels plus persistent sessions let messages survive brief disconnections. **HTTP remains the better fit** for request/response interactions such as REST APIs, web pages, file uploads/downloads and CRUD operations, where caching, the browser ecosystem and stateless scaling matter more than real-time push. A common architecture combines the two: devices publish over MQTT, a backend service subscribes and stores the data, and dashboards read it through an HTTP API (the Flask apps in module 3).

| Aspect | MQTT | HTTP |
|---|---|---|
| Model | Publish/subscribe via broker | Request/response, client ↔ server |
| Connection | Persistent TCP connection | Usually short-lived per request (keep-alive optional) |
| Header overhead | 2-byte fixed header | Hundreds of bytes of text headers |
| Direction | Bi-directional, broker pushes | Client must initiate (pull) |
| Delivery guarantees | QoS 0 / 1 / 2 built in | Relies on TCP + application retries |
| Fan-out | One publish → many subscribers | One request → one response |
| Extras | Retained messages, Last Will, persistent sessions | Caching, status codes, rich methods (GET/POST/PUT/DELETE) |
| Default ports | 1883 (plain), 8883 (TLS) | 80 (plain), 443 (TLS) |
| Best for | IoT telemetry, real-time events | Web pages, REST APIs, file transfer |
