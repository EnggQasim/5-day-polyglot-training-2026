# Kafka — Step 5: LAB (stream Pixel Quest score events)

In this lab you build a small but realistic streaming pipeline:
1. A **generator** producer that keeps emitting random score events.
2. A **consumer** that keeps a running in-memory leaderboard and prints the top 5.

This mimics a live game backend: scores flow in continuously, and a reader keeps the standings up to date.

---

## Step 1 — Make sure the topic exists

```bash
docker exec -it pq_broker kafka-topics --bootstrap-server localhost:9092 \
  --create --topic player-scores --partitions 3 --replication-factor 1 \
  --if-not-exists
```

## Step 2 — Run the generator (producer)

`05_score_generator.py` sends a new random score every half second, keyed by player so each player's events stay ordered.

```bash
python day2/kafka/code/05_score_generator.py
```

You will see lines like `sent hero_07 +120 (offset 14)`. Leave it running.

## Step 3 — Run the leaderboard (consumer)

In a second terminal, `05_leaderboard_consumer.py` adds up each player's points as events arrive and reprints the top 5.

```bash
python day2/kafka/code/05_leaderboard_consumer.py
```

Output updates live:

```
--- LIVE LEADERBOARD ---
1. elf_mona     1820
2. ninja_sara   1450
3. hero_07      1200
4. mage_lily     980
5. tank_omar     760
```

---

## What to observe

- **Decoupling:** the generator does not know the consumer exists. You can stop and restart either one independently.
- **Replay:** stop the consumer, let the generator run, then start the consumer with a **fresh** `group.id` and `auto.offset.reset=earliest` — it rebuilds the whole leaderboard from history. That is Kafka's superpower: the events are still there.
- **Scaling:** start a second leaderboard consumer with the **same** group id — they split the partitions and share the load (each handles part of the stream).
- **Lag:** in a third terminal, run the `kafka-consumer-groups --describe` command from lesson 4 to watch the consumer keep up.

---

## What you achieved

- A continuous **producer** and a stateful **consumer** working as a live pipeline.
- Saw **decoupling, replay, scaling, and lag** with your own data.

### Deliverable for this track
Commit both scripts and note: *How is this leaderboard different from the Redis sorted-set leaderboard you built on Day 1? When would you compute it from a Kafka stream vs store it directly in Redis?* (Hint: Kafka gives you the full history of events to recompute or feed many consumers; Redis gives you the instant current answer.)

➡️ Next: **[06-reliability-and-delivery.md](06-reliability-and-delivery.md)**

---

## ⭐ Must-learn from this topic

- **A live pipeline** — continuous producer + stateful consumer.
- **Replay** — rebuild state from history with a fresh group + `earliest`.
- **Scaling out** — add consumers in the same group to share partitions.
- **Stream vs store** — Kafka (history of events) vs Redis (instant current value).

### 📚 Official docs
- [Kafka design](https://kafka.apache.org/documentation/#design) — why replay & retention work.
- [confluent-kafka Python client](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html) — producer/consumer API.
- [Kafka use cases](https://kafka.apache.org/uses) — where streaming fits.
