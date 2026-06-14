# Redis — Step 3: Persistence (RDB vs AOF)

Redis keeps data in RAM. But RAM is wiped when the server restarts. So how does Redis avoid losing everything on a restart? It can **save to disk** in two ways: **RDB** and **AOF**.

---

## RDB — snapshots

**RDB** takes a **snapshot** of all data every now and then and writes it to one file (`dump.rdb`).

- Like taking a photo of the whole database at a moment in time.
- Fast to save and load; small file.
- **Risk:** if Redis crashes between snapshots, you lose the changes since the last photo.

Trigger a snapshot by hand:

```
SAVE        -- save now, blocking (only for tiny data / learning)
BGSAVE      -- save in the background (normal way)
```

Snapshots are also configured to happen automatically, e.g. "save if 100 keys changed in 60 seconds".

---

## AOF — Append Only File

**AOF** writes **every change command** to a log file as it happens. To rebuild the data, Redis replays the log.

- Like keeping a diary of every single change.
- **Much safer** — you can lose at most one second of data (or zero, depending on settings).
- Bigger file and a little slower than RDB.

The `appendfsync` setting controls how often the log is flushed to disk:
- `always` — flush after every command (safest, slowest).
- `everysec` — flush once per second (good balance, the usual choice).
- `no` — let the OS decide (fastest, least safe).

---

## Which to use?

Most production setups turn on **both**: RDB for fast restarts and AOF for safety. For a pure cache where losing data is fine, you can turn both off and run fully in memory.

| | RDB | AOF |
|---|-----|-----|
| What | periodic snapshot | log of every write |
| Data loss risk | minutes | ~1 second |
| File size | small | larger |
| Restart speed | fast | slower (replays log) |

---

## See your current settings

```
CONFIG GET save            -- the RDB snapshot rules
CONFIG GET appendonly      -- is AOF on? ("yes"/"no")
CONFIG GET appendfsync     -- how often AOF flushes
```

## Turn on AOF live and test durability

You will prove AOF works in the **lab** (next-but-one lesson). The short version:

```
CONFIG SET appendonly yes      -- turn AOF on without restarting
ZADD leaderboard 8888 test_player
BGREWRITEAOF                    -- compact the AOF file
```

After this, even if Redis restarts, `test_player` is still there because the change was written to the AOF log.

**Key point:** in-memory does **not** have to mean "data is lost on restart". RDB and AOF give you the safety dial — turn it up or down based on how much you can afford to lose.

**Run the file:** [`code/03_persistence.redis`](code/03_persistence.redis)

➡️ Next: **[04-clustering-eviction-acl.md](04-clustering-eviction-acl.md)**

---

## ⭐ Must-learn from this topic

- **RDB snapshots** — `SAVE` / `BGSAVE`, the periodic-photo model.
- **AOF (Append Only File)** — `appendonly`, `appendfsync` (`always` / `everysec` / `no`).
- **The trade-off** — data-loss risk vs file size vs restart speed.

### 📚 Official docs
- [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) — RDB, AOF, and combining them.
- [CONFIG SET](https://redis.io/commands/config-set/) — change settings at runtime.
- [BGSAVE](https://redis.io/commands/bgsave/) / [BGREWRITEAOF](https://redis.io/commands/bgrewriteaof/) — the save commands.
