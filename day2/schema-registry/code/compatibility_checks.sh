#!/usr/bin/env bash
# Explore the Schema Registry REST API (port 8081).

# global default compatibility mode
curl http://localhost:8081/config ; echo

# list all registered subjects
curl http://localhost:8081/subjects ; echo

# list versions of one subject (after the lab has registered it)
curl http://localhost:8081/subjects/pq-scores-value/versions ; echo

# fetch the latest schema for a subject
curl http://localhost:8081/subjects/pq-scores-value/versions/latest ; echo

# test if a candidate schema is compatible with the latest version
curl -X POST http://localhost:8081/compatibility/subjects/pq-scores-value/versions/latest \
  -H "Content-Type: application/json" \
  -d '{"schema": "{\"type\":\"record\",\"name\":\"PlayerScore\",\"fields\":[{\"name\":\"player\",\"type\":\"string\"},{\"name\":\"points\",\"type\":\"int\"}]}"}' ; echo

# set a subject's compatibility mode (BACKWARD | FORWARD | FULL | NONE)
curl -X PUT http://localhost:8081/config/pq-scores-value \
  -H "Content-Type: application/json" \
  -d '{"compatibility": "FULL"}' ; echo
