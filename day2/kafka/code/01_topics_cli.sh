#!/usr/bin/env bash
# Kafka topic + console producer/consumer commands.
# Run the lines you need one at a time (the producer/consumer are interactive).

# create a topic with 3 partitions
docker exec -it pq_broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --topic player-scores \
  --partitions 3 --replication-factor 1

# list topics
docker exec -it pq_broker kafka-topics --bootstrap-server localhost:9092 --list

# describe our topic
docker exec -it pq_broker kafka-topics --bootstrap-server localhost:9092 \
  --describe --topic player-scores

# console producer (type messages, Ctrl+C to stop)
docker exec -it pq_broker kafka-console-producer \
  --bootstrap-server localhost:9092 --topic player-scores

# console consumer (reads from the beginning, Ctrl+C to stop)
docker exec -it pq_broker kafka-console-consumer \
  --bootstrap-server localhost:9092 --topic player-scores --from-beginning

# producer WITH keys (key:value)
docker exec -it pq_broker kafka-console-producer \
  --bootstrap-server localhost:9092 --topic player-scores \
  --property "parse.key=true" --property "key.separator=:"

# consumer that prints keys
docker exec -it pq_broker kafka-console-consumer \
  --bootstrap-server localhost:9092 --topic player-scores \
  --from-beginning --property print.key=true --property key.separator=" => "
