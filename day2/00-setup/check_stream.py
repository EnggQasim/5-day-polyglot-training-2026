"""
Day 2 setup checker. Confirms the four streaming services are reachable.
Uses only the Python standard library (socket + urllib), so it runs even
before you install confluent-kafka.

Usage:
    python day2/00-setup/check_stream.py
"""
import json
import socket
import urllib.request


def check_kafka():
    # a plain TCP connect to the broker port is enough to prove it is up
    with socket.create_connection(("localhost", 9092), timeout=5):
        return "localhost:9092 reachable"


def http_json(url, timeout=5):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        body = r.read().decode()
        try:
            return r.status, json.loads(body)
        except json.JSONDecodeError:
            return r.status, body


def check_schema_registry():
    status, _ = http_json("http://localhost:8081/subjects")
    return f"HTTP {status} from :8081"


def check_connect():
    status, plugins = http_json("http://localhost:8083/connector-plugins")
    names = " ".join(p.get("class", "") for p in plugins) if isinstance(plugins, list) else ""
    if "postgres" in names.lower() or "Postgres" in names:
        return "Debezium Postgres plugin present"
    return f"HTTP {status} (connect up; plugins listed)"


def check_ksqldb():
    status, info = http_json("http://localhost:8088/info")
    if isinstance(info, dict):
        ks = info.get("KsqlServerInfo", {})
        return f"server {ks.get('serverStatus', 'reachable')}"
    return f"HTTP {status}"


def main():
    checks = [
        ("Kafka broker", check_kafka),
        ("Schema Registry", check_schema_registry),
        ("Kafka Connect", check_connect),
        ("KSQLDB", check_ksqldb),
    ]
    all_ok = True
    for name, func in checks:
        try:
            print(f"{name:<16} : OK  ({func()})")
        except Exception as e:
            all_ok = False
            print(f"{name:<16} : FAILED -> {e}")

    print()
    print("All good. You are ready for Day 2." if all_ok
          else "Some checks failed. Wait a minute for the JVM services to boot, then retry.")


if __name__ == "__main__":
    main()
