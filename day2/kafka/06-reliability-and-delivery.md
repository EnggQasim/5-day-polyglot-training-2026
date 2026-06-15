# Kafka — Step 6: Reliability and delivery guarantees

Streaming is only useful if you can trust the data. This lesson covers how Kafka keeps data safe (**replication / ISR**) and the producer settings that decide **how many times a message can arrive** (`acks`, idempotence, exactly-once).

---

## Replication and ISR (not losing data)

A topic partition can be **replicated** onto several brokers: one **leader** + some **followers**. Producers and consumers talk to the leader; followers copy its data. If the leader broker dies, a follower is promoted — no data lost.

- **Replication factor** = how many copies (e.g. 3). Set per topic.
- **ISR = In-Sync Replicas** = the set of replicas that are **fully caught up** with the leader. Only an in-sync replica can become the new leader, so ISR is Kafka's safety pool.
- **`min.insync.replicas`** = the minimum ISR required to accept a write. With replication factor 3 and `min.insync.replicas=2`, a write needs the leader + at least one follower in sync, so it survives losing one broker.

> Our training cluster has **one** broker (replication factor 1), so there is no real redundancy — but the settings below are exactly what you would use in production. We can still set and read them.

---

## `acks`: how sure is the producer that the write landed?

The producer's **`acks`** setting trades speed for safety:

- **`acks=0`** — fire and forget. Fastest, but a lost message is never noticed. (Don't use for important data.)
- **`acks=1`** — wait for the **leader** to write it. Good, but if the leader dies before a follower copies it, you can lose that message.
- **`acks=all`** (a.k.a. `acks=-1`) — wait for **all in-sync replicas**. Safest. Combined with `min.insync.replicas`, this is the durable choice.

```python
producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "acks": "all",          # wait for all in-sync replicas
})
```

---

## Idempotent producer (no duplicates from retries)

When a producer retries after a network blip, the message could be written **twice**. The **idempotent producer** gives each message a sequence number so the broker drops duplicates — you get **exactly one copy** even with retries.

```python
producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "acks": "all",
    "enable.idempotence": True,   # safe retries: no duplicates
})
```

`enable.idempotence=True` automatically implies `acks=all` and bounded retries. This alone gives **"effectively once" delivery to a topic**, and it is the recommended default for producers.

---

## Exactly-once across read→process→write (transactions)

The hardest case: a service **reads** from one topic, **processes**, and **writes** to another. If it crashes midway, you might process the same input twice. Kafka's **transactions API** lets the consume-process-produce cycle commit **atomically** — all of it happens, or none of it.

```python
producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "enable.idempotence": True,
    "transactional.id": "score-processor-1",   # names this transactional producer
})
producer.init_transactions()
producer.begin_transaction()
# ... produce derived messages AND record the consumer offsets ...
producer.commit_transaction()   # all-or-nothing
```

This is **exactly-once semantics (EOS)**. In KSQLDB and Kafka Streams you get it by simply setting `processing.guarantee=exactly_once_v2` — they use these transactions under the hood.

---

## The mental model

| You want… | Use |
|-----------|-----|
| Max speed, can lose data | `acks=0` |
| Reasonable safety | `acks=1` |
| Durable writes | `acks=all` + `min.insync.replicas≥2` + replication≥3 |
| No duplicate writes on retry | `enable.idempotence=True` |
| Exactly-once read→process→write | transactions / `processing.guarantee=exactly_once_v2` |

**Run the reliable producer:** [`code/06_reliable_producer.py`](code/06_reliable_producer.py) — same as our earlier producer but configured for durability.

➡️ Next: the benchmark lab — **[07-lab-throughput-benchmark.md](07-lab-throughput-benchmark.md)**

---

## ⭐ Must-learn from this topic

- **Replication & ISR** — copies across brokers; `min.insync.replicas` for safety.
- **`acks`** — 0 / 1 / all, the speed-vs-durability dial.
- **Idempotent producer** — `enable.idempotence=True` removes retry duplicates.
- **Exactly-once** — the transactions API; `processing.guarantee=exactly_once_v2`.

### 📚 Official docs
- [Producer configs (acks, idempotence)](https://kafka.apache.org/documentation/#producerconfigs) — the settings.
- [Replication & ISR design](https://kafka.apache.org/documentation/#replication) — how durability works.
- [Exactly-once semantics](https://docs.confluent.io/platform/current/clients/producer.html#idempotent-producer) — idempotence & transactions.
