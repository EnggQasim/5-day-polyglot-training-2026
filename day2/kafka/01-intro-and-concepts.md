# Kafka — Step 1: What it is, and the core ideas

## What is Kafka?

Apache Kafka is an **event streaming platform**. The simplest way to picture it: Kafka is a **highway for messages**. One program writes messages onto the highway; other programs read them — at their own speed, now or later.

A "message" (Kafka calls it an **event** or **record**) is just a small piece of data, like *"player hero_07 scored 150 points at 09:05"*.

We use Kafka when:
- Many systems need the **same events** (a score change feeds a leaderboard, an analytics job, and an alert).
- We want producers and consumers **decoupled** — they do not call each other directly; they just write/read the highway.
- We need to **replay** history (a new consumer can read events from the beginning).

## The words you must know

Learn these five words and Kafka stops being scary.

- **Broker** — a Kafka server. Our stack runs one broker (`pq_broker`). Production runs several.
- **Topic** — a named stream of messages, like a folder. Example: `player-scores`. Producers write to a topic; consumers read from it.
- **Partition** — a topic is split into partitions so it can scale and be read in parallel. Each partition is an **ordered, append-only log**.
- **Producer** — a program that **writes** messages to a topic.
- **Consumer** — a program that **reads** messages from a topic.

Picture it:

```
 Producer ──writes──►  Topic: player-scores
                       ├─ partition 0:  [m0][m1][m2] ...   (ordered)
                       └─ partition 1:  [m0][m1] ...
 Consumer ──reads───►  (gets messages in partition order)
```

## A few more ideas (we use them today)

- **Offset** — the position number of a message inside a partition (0, 1, 2, …). A consumer remembers "I have read up to offset 7", so it can continue later. This is how Kafka does *replay* and *resume*.
- **Consumer group** — a team of consumers that **share** the work of reading a topic. Kafka gives each partition to one member, so adding members spreads the load. (Lesson 4.)
- **Key** — each message can have a key (e.g. the player name). All messages with the same key go to the **same partition**, so their order is kept. Great when per-player order matters.
- **Retention** — Kafka keeps messages for a time/size you choose (e.g. 7 days), even after they are read. That is why it is a *log*, not just a queue.

## Why not just use a database table?

A database answers "what is true *now*". Kafka records "what *happened*, in order, over time" and lets many independent readers consume it without slowing each other down. They complement each other — which is exactly the Day 1 → Day 2 story.

## What runs in our stack

| Piece | Container | Port |
|-------|-----------|------|
| Kafka broker | `pq_broker` | 9092 (laptop), 29092 (inside Docker) |
| Zookeeper (broker coordination) | `pq_zookeeper` | 2181 |

> Zookeeper helps the broker keep track of cluster state. You will not touch it directly today; newer Kafka can run without it (KRaft mode), but our Confluent setup uses it.

➡️ Next: **[02-topics-and-cli.md](02-topics-and-cli.md)** — create a topic and send your first messages.

---

## ⭐ Must-learn from this topic

- **Core words** — broker, topic, partition, producer, consumer.
- **Offset** — the position in a partition; how Kafka resumes and replays.
- **Key → partition** — same key keeps order in one partition.
- **Retention** — Kafka keeps events after they are read (a log, not just a queue).

### 📚 Official docs
- [Apache Kafka — Introduction](https://kafka.apache.org/intro) — the concepts in brief.
- [Kafka Documentation](https://kafka.apache.org/documentation/) — the full reference.
- [Confluent Platform overview](https://docs.confluent.io/platform/current/overview.html) — the stack we run.
