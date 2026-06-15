# Kafka — Step 2: Topics and the command-line tools

Before writing any code, let's use Kafka's built-in command-line tools. They live **inside** the broker container, so we run them with `docker exec`.

> Reminder: open a terminal (VS Code → Terminal, or PowerShell) and make sure both stacks are up (`docker compose up -d` and `docker compose -f day2/docker-compose.day2.yml up -d`).

---

## Create a topic

We make a topic called `player-scores` with 3 partitions.

```bash
docker exec -it pq_broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --topic player-scores \
  --partitions 3 --replication-factor 1
```

- `--partitions 3` — split the topic into 3 ordered logs (for parallel reading).
- `--replication-factor 1` — keep 1 copy (we have only one broker; production uses 3).

## List and describe topics

```bash
# list all topics
docker exec -it pq_broker kafka-topics --bootstrap-server localhost:9092 --list

# see details of our topic (partitions, leader, etc.)
docker exec -it pq_broker kafka-topics --bootstrap-server localhost:9092 \
  --describe --topic player-scores
```

The `--describe` output shows each partition and which broker is its **leader** (the broker that handles its reads/writes).

---

## Send messages from the command line (a console producer)

This opens a prompt; whatever you type and Enter becomes a message on the topic.

```bash
docker exec -it pq_broker kafka-console-producer \
  --bootstrap-server localhost:9092 --topic player-scores
```

Type a few lines, pressing Enter after each:

```
hero_07 scored 150
elf_mona scored 500
ninja_sara scored 300
```

Press **Ctrl+C** to stop.

---

## Read messages back (a console consumer)

In another terminal, read everything from the start:

```bash
docker exec -it pq_broker kafka-console-consumer \
  --bootstrap-server localhost:9092 --topic player-scores \
  --from-beginning
```

You will see the three lines you typed. Notice they keep printing — a consumer **stays open** waiting for new messages. Press **Ctrl+C** to stop.

> Try this: leave the consumer running, open the producer again, and type a new line. It appears in the consumer almost instantly. That is the "highway" in action.

---

## Sending messages with a key

A **key** decides the partition, which keeps order per key. Send key-value pairs separated by `:`:

```bash
docker exec -it pq_broker kafka-console-producer \
  --bootstrap-server localhost:9092 --topic player-scores \
  --property "parse.key=true" --property "key.separator=:"
```

Then type:

```
hero_07:scored 150
hero_07:scored 60
elf_mona:scored 500
```

All `hero_07` messages land on the **same partition**, so their order is preserved. To see keys when consuming:

```bash
docker exec -it pq_broker kafka-console-consumer \
  --bootstrap-server localhost:9092 --topic player-scores \
  --from-beginning --property print.key=true --property key.separator=" => "
```

**All these commands are also in** [`code/01_topics_cli.sh`](code/01_topics_cli.sh).

➡️ Next: **[03-producers-consumers.md](03-producers-consumers.md)** — do the same from Python.

---

## ⭐ Must-learn from this topic

- **`kafka-topics`** — create / list / describe topics; partitions & replication factor.
- **`kafka-console-producer` / `kafka-console-consumer`** — send & read messages by hand.
- **`--from-beginning`** — read a topic's full history.
- **Keys on the CLI** — `parse.key=true`, `key.separator`.

### 📚 Official docs
- [Kafka CLI tools](https://docs.confluent.io/platform/current/installation/cli-reference.html) — the command-line utilities.
- [Topic operations](https://kafka.apache.org/documentation/#basic_ops) — managing topics.
- [Main concepts & terminology](https://kafka.apache.org/documentation/#intro_concepts_and_terms).
