# Schema Registry — Step 3: LAB (produce & consume Avro)

In this lab you send score events as **Avro**, validated by the Schema Registry, and read them back. Then you try a safe schema change and a breaking one.

---

## Step 1 — install the Avro client

```bash
# venv active
pip install "confluent-kafka[avro]"
```

This adds the Avro serializer that talks to the Schema Registry.

## Step 2 — produce Avro messages

`avro_producer.py` registers the schema (from `player_score.avsc`) automatically and sends typed events to the topic `pq-scores`.

```bash
python day2/schema-registry/code/avro_producer.py
```

It prints something like:

```
produced PlayerScore(player=hero_07, points=150)
produced PlayerScore(player=elf_mona, points=500)
schema registered under subject 'pq-scores-value'
```

Check the subject exists:

```bash
curl http://localhost:8081/subjects
```

You should see `pq-scores-value`.

## Step 3 — consume Avro messages

`avro_consumer.py` looks up the schema by id and decodes each message into a typed dict.

```bash
python day2/schema-registry/code/avro_consumer.py
```

Output:

```
hero_07 -> 150
elf_mona -> 500
```

Notice you never told the consumer the schema — it fetched it from the registry using the id embedded in each message.

---

## Step 4 — try schema evolution

**Safe change:** open `player_score.avsc` and add a field **with a default**:

```json
{ "name": "country", "type": "string", "default": "??" }
```

Run the producer again. The registry accepts the new version (BACKWARD-compatible), and the **old** consumer still works — it just ignores the new field. That is safe evolution.

**Breaking change:** now change `points` from `"int"` to `"string"` and run the producer. The registry **rejects** it with a compatibility error, protecting every existing consumer. Change it back when done.

---

## What you achieved

- Sent and received **typed Avro** messages validated by the Schema Registry.
- Saw the registry **store a subject** and hand schemas to consumers by id.
- Proved a **safe** schema change works and a **breaking** one is blocked.

### Deliverable for this track
Commit `player_score.avsc` and both scripts. In your notes: *What real outage does schema compatibility prevent? Why is "add a field with a default" safe but "change a field's type" not?*

➡️ Next: **[../ksqldb/01-streams-vs-tables.md](../ksqldb/01-streams-vs-tables.md)**

---

## ⭐ Must-learn from this topic

- **Avro serializer/deserializer** — `AvroSerializer` / `AvroDeserializer` + `SchemaRegistryClient`.
- **Auto-registration** — the producer registers the schema under `<topic>-value`.
- **Decode by id** — the consumer needs no local schema.
- **Evolution in practice** — a defaulted field is accepted; a type change is rejected.

### 📚 Official docs
- [Avro serdes](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html) — the producer/consumer pattern.
- [confluent-kafka Python client](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html) — serializer classes.
- [Schema evolution](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html) — safe vs breaking changes.
