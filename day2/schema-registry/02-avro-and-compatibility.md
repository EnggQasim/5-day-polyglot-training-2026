# Schema Registry — Step 2: Avro and compatibility

Data shapes change over time — you add a field, make something optional, etc. **Compatibility rules** let a schema evolve **without breaking** the producers and consumers already running. This is the most valuable idea in this whole topic.

---

## The compatibility modes

When you register a new version of a schema, the registry checks it against the old one using the **compatibility mode** set for that subject. The common modes:

- **BACKWARD** (the default) — new schema can read data written with the **old** schema. So you can **upgrade consumers first**. Allowed changes: *delete a field*, or *add an optional field (with a default)*.
- **FORWARD** — old schema can read data written with the **new** schema. So you can **upgrade producers first**. Allowed: *add a field*, or *delete an optional field*.
- **FULL** — both backward and forward at once (most strict, safest).
- **NONE** — no checks (dangerous; anything goes).

> Plain-English version of BACKWARD: "old messages must still make sense to the new code." That is why adding a field **with a default** is safe — old messages simply use the default.

---

## A safe change vs a breaking change

Start with:

```json
{ "type": "record", "name": "PlayerScore", "namespace": "pq",
  "fields": [
    { "name": "player", "type": "string" },
    { "name": "points", "type": "int" }
  ]
}
```

**Safe (BACKWARD-compatible):** add a new field **with a default**.

```json
{ "name": "country", "type": "string", "default": "??" }
```

Old messages had no `country`; new code reads them and uses `"??"`. Nothing breaks.

**Breaking:** change `points` from `int` to `string`, or add a required field with **no default**. The registry will **reject** it under BACKWARD mode — which is exactly what you want, because it would have broken consumers.

---

## Check and set compatibility (REST)

The registry has a REST API on port 8081.

```bash
# the global default compatibility
curl http://localhost:8081/config

# list all registered subjects
curl http://localhost:8081/subjects

# test whether a new schema is compatible with the latest version of a subject
# (returns {"is_compatible": true/false})
curl -X POST http://localhost:8081/compatibility/subjects/pq-scores-value/versions/latest \
  -H "Content-Type: application/json" \
  -d '{"schema": "{\"type\":\"record\",\"name\":\"PlayerScore\",\"fields\":[{\"name\":\"player\",\"type\":\"string\"},{\"name\":\"points\",\"type\":\"int\"}]}"}'

# set compatibility for one subject (e.g. to FULL)
curl -X PUT http://localhost:8081/config/pq-scores-value \
  -H "Content-Type: application/json" \
  -d '{"compatibility": "FULL"}'
```

**Commands also in** [`code/compatibility_checks.sh`](code/compatibility_checks.sh).

---

## Why you will be glad this exists

Without compatibility checks, a small change by one team quietly breaks another team's consumers. With them, a breaking change is **caught at deploy time** with a clear error, and safe changes flow through automatically. It turns "data shape" from a source of outages into a managed, versioned contract.

➡️ Next: the lab — **[03-lab-avro-produce-consume.md](03-lab-avro-produce-consume.md)**

---

## ⭐ Must-learn from this topic

- **Compatibility modes** — BACKWARD (default), FORWARD, FULL, NONE.
- **Safe vs breaking changes** — add a field *with a default* (safe) vs change a type / add a required field (breaking).
- **Registry REST API** — `/config`, `/subjects`, `/compatibility/...`.
- **Why** — breaking changes are caught at deploy time, not in production.

### 📚 Official docs
- [Schema evolution & compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html) — the rules in detail.
- [Schema Registry REST API](https://docs.confluent.io/platform/current/schema-registry/develop/api.html) — endpoints reference.
- [Avro schema resolution](https://avro.apache.org/docs/) — how Avro reconciles versions.
