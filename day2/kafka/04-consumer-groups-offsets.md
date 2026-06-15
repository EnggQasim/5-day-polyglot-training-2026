# Kafka — Step 4: Consumer groups and offsets

Two ideas that make Kafka powerful for real systems: **consumer groups** (share work) and **offsets** (remember progress).

---

## Consumer groups: sharing the work

A **consumer group** is a team of consumers with the same `group.id`. Kafka splits the topic's **partitions** among the group members so they share the load — and never read the same message twice within the group.

Rule: **each partition is handled by exactly one consumer in the group.**

```
Topic player-scores (3 partitions)        Consumer group "score-readers"
  partition 0  ─────────────────►  consumer A
  partition 1  ─────────────────►  consumer A
  partition 2  ─────────────────►  consumer B
```

- More consumers (up to the partition count) = more parallel work.
- More consumers **than** partitions = the extra ones sit idle (no partition to own).
- If a consumer dies, Kafka **rebalances**: its partitions are handed to the others automatically.

Different groups are independent: two groups each get **all** the messages. That is how a leaderboard group and an analytics group both read every score.

### See it yourself

Run the consumer from the last lesson in **two** terminals (same `group.id = score-readers`). Then produce several messages. Watch the two consumers split the partitions between them — each message is handled by only one of them.

Now change the `group.id` in one consumer to `analytics` and rerun: that consumer gets **all** messages again, because it is a separate group.

---

## Offsets: remembering where you are

An **offset** is the position of a message within a partition (0, 1, 2, …). Kafka stores, per group and per partition, the offset a group has **committed** (finished processing). So:

- A consumer that restarts continues from its last committed offset — no messages missed or repeated.
- A brand-new group with no committed offset uses `auto.offset.reset` (`earliest` = from the start, `latest` = only new messages).

### Commit modes

- **Auto-commit (default)** — the client commits offsets periodically for you. Simple; good enough for the labs.
- **Manual commit** — you call `consumer.commit()` after you have *safely processed* a message. Safer for important work, because you only mark progress once the work is truly done.

```python
consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "score-readers",
    "enable.auto.commit": False,     # we will commit ourselves
    "auto.offset.reset": "earliest",
})
# ... after processing a message successfully:
consumer.commit(msg)                 # mark this offset as done
```

### Inspect a group's offsets and lag

"Lag" = how far behind a group is (messages produced but not yet consumed).

```bash
docker exec -it pq_broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --describe --group score-readers
```

The output shows, per partition: `CURRENT-OFFSET` (where the group is), `LOG-END-OFFSET` (newest message), and `LAG` (the difference). Watching lag is how you tell if consumers are keeping up.

**Commands also in** [`code/04_groups_offsets.sh`](code/04_groups_offsets.sh).

➡️ Next: the lab — **[05-lab-score-stream.md](05-lab-score-stream.md)**

---

## ⭐ Must-learn from this topic

- **Consumer groups** — partitions split across members; rebalancing on failure.
- **One partition → one consumer** (within a group); extra consumers idle.
- **Offsets & commits** — auto vs manual commit; `auto.offset.reset`.
- **Lag** — produced minus consumed; how you tell if consumers keep up.

### 📚 Official docs
- [Consumer groups](https://docs.confluent.io/platform/current/clients/consumer.html) — sharing work & rebalancing.
- [`kafka-consumer-groups` tool](https://docs.confluent.io/platform/current/installation/cli-reference.html) — inspecting offsets/lag.
- [Offset management](https://kafka.apache.org/documentation/#impl_offsettracking) — how offsets are stored.
