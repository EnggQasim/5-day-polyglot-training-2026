#!/usr/bin/env bash
# Inspect consumer groups, their offsets, and lag.

# list all consumer groups
docker exec -it pq_broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 --list

# describe one group: shows CURRENT-OFFSET, LOG-END-OFFSET, LAG per partition
docker exec -it pq_broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --describe --group score-readers

# (advanced) reset a group's offsets back to the start, then re-consume
# docker exec -it pq_broker kafka-consumer-groups \
#   --bootstrap-server localhost:9092 \
#   --group score-readers --topic player-scores \
#   --reset-offsets --to-earliest --execute
