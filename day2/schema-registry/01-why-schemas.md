# Schema Registry — Step 1: Why schemas?

## The problem with "just send JSON"

So far we sent score events as free-form JSON. That works until someone changes the shape. Imagine the producer team renames `points` to `score`, or starts sending it as text `"150"` instead of a number. Every consumer silently breaks, and you find out in production.

Kafka itself does **not** check what is inside a message — to Kafka, a message is just bytes. So who makes sure producers and consumers **agree** on the shape of the data? That is the job of the **Schema Registry**.

## What is Schema Registry?

The **Schema Registry** is a service (running as `pq_schema_registry` on port 8081) that stores the agreed **schema** — the shape — of the data in each topic. It gives you:

- **One source of truth** for each topic's data shape.
- **Validation:** a producer must send data that matches the registered schema, or it is rejected *before* it reaches Kafka.
- **Safe evolution:** rules that allow you to change a schema over time **without** breaking existing consumers.

```
 Producer ──(1) "here is my data + schema id")──► Kafka topic
     │                                              │
     └──(register/lookup schema)──► Schema Registry ◄──(look up schema by id)── Consumer
```

The message on Kafka carries a tiny **schema id**, not the whole schema. Consumers use the id to fetch the schema from the registry and decode the bytes correctly.

## Avro (the data format we use)

A **schema** needs a format. The most common with Kafka is **Avro**: a compact binary format with a clear schema written in JSON. (Alternatives: Protobuf, JSON Schema — the registry supports all three.)

A tiny Avro schema for a score event looks like this:

```json
{
  "type": "record",
  "name": "PlayerScore",
  "namespace": "pq",
  "fields": [
    { "name": "player", "type": "string" },
    { "name": "points", "type": "int" }
  ]
}
```

This says: every message is a record with a string `player` and an integer `points`. If a producer tries to send `points` as a string, it is rejected.

## Why binary Avro instead of JSON text?

- **Smaller & faster:** binary is more compact than text JSON, which matters at millions of messages.
- **Typed:** `int` really means int; no guessing.
- **Validated & versioned:** the registry enforces the schema and tracks versions.

## Key words

- **Subject** — the name under which a schema is registered. By default it is `<topic>-value` (e.g. `pq-scores-value`).
- **Schema id** — a number the registry assigns to each schema; embedded in every message.
- **Compatibility** — the rule for how a schema may change (next lesson).

➡️ Next: **[02-avro-and-compatibility.md](02-avro-and-compatibility.md)**

---

## ⭐ Must-learn from this topic

- **Why schemas** — Kafka stores bytes; the registry enforces the agreed data shape.
- **Schema id in each message** — consumers fetch the schema by id to decode.
- **Avro** — compact, typed, JSON-defined records (vs free-form JSON text).
- **Subject** — usually `<topic>-value`; where a schema is registered.

### 📚 Official docs
- [Schema Registry overview](https://docs.confluent.io/platform/current/schema-registry/index.html) — what it is and why.
- [Avro serializer/deserializer](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html) — using Avro with Kafka.
- [Apache Avro spec](https://avro.apache.org/docs/) — the data format itself.
