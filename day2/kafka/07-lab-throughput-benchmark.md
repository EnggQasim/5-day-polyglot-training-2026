# Kafka — Step 7: LAB (throughput benchmark, ≥10k msg/s)

Goal: measure how many messages per second your Kafka setup can push and pull, and reach **≥10,000 msg/s**. Kafka ships purpose-built benchmark tools inside the broker container, so we use those (no code needed), then optionally a Python version.

---

## Step 1 — a topic for the test

```bash
docker exec -it pq_broker kafka-topics --bootstrap-server localhost:9092 \
  --create --topic perf-test --partitions 6 --replication-factor 1 --if-not-exists
```

More partitions = more parallelism, which helps throughput.

## Step 2 — producer benchmark

`kafka-producer-perf-test` blasts records and reports the rate:

```bash
docker exec -it pq_broker kafka-producer-perf-test \
  --topic perf-test \
  --num-records 500000 \
  --record-size 200 \
  --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092 acks=1
```

- `--num-records 500000` — send half a million messages.
- `--record-size 200` — each message is 200 bytes.
- `--throughput -1` — go as fast as possible (no rate limit).

Output ends with a line like:

```
500000 records sent, 250000.0 records/sec (47.68 MB/sec), 5.2 ms avg latency
```

`records/sec` is your producer throughput — should be well above 10,000/s on the training laptop.

> Try it twice: once with `acks=1`, once with `acks=all`. Notice the safer setting is a bit slower — that is the durability/speed trade-off from the last lesson, measured.

## Step 3 — consumer benchmark

```bash
docker exec -it pq_broker kafka-consumer-perf-test \
  --bootstrap-server localhost:9092 \
  --topic perf-test \
  --messages 500000
```

It reports `MB.sec` and `nMsg.sec` (messages/sec) for reading.

---

## Step 4 (optional) — Python throughput

`code/07_benchmark.py` measures how fast the Python client can produce, to compare with the CLI:

```bash
python day2/kafka/code/07_benchmark.py
```

It prints something like `produced 100000 msgs in 3.1s -> 32258 msg/s`.

The Python client is a little slower than the Java perf tool but should still clear 10k/s easily for small messages — the key is to **batch** (let `poll(0)` serve callbacks and `flush()` once at the end), not flush per message.

---

## What to observe

- **Partitions help:** rerun the producer test against a 1-partition topic vs the 6-partition one and compare.
- **`acks` cost:** `acks=all` < `acks=1` < `acks=0` in throughput, in exchange for safety.
- **Message size matters:** bigger `--record-size` = fewer msg/s but more MB/s.

### Deliverable for this track
Record your `records/sec` for producer and consumer (and the `acks=1` vs `acks=all` difference). Note in 2 lines: *what would you change to push throughput higher, and what does it cost?*

➡️ Next: **[../debezium/01-what-is-cdc.md](../debezium/01-what-is-cdc.md)**

---

## ⭐ Must-learn from this topic

- **Perf tools** — `kafka-producer-perf-test`, `kafka-consumer-perf-test`.
- **Reading results** — `records/sec`, `MB/sec`, average latency.
- **Levers** — partitions, batching (`linger.ms`, `batch.size`), `acks`, message size.
- **Trade-off, measured** — safer `acks` = lower throughput.

### 📚 Official docs
- [Kafka performance testing](https://developer.confluent.io/courses/architecture/benchmarking/) — using the perf tools.
- [Producer configs](https://kafka.apache.org/documentation/#producerconfigs) — `linger.ms`, `batch.size`, `acks`.
- [Kafka design — efficiency](https://kafka.apache.org/documentation/#maximizingefficiency) — why Kafka is fast.
