# Milvus — Step 3: LAB (50k vectors, IVF-PQ index, benchmark 100 searches)

This is the headline Milvus lab. You will:
1. Create a collection for item vectors.
2. **Insert 50,000** random 128-dimensional vectors.
3. Build an **IVF-PQ** index.
4. **`load_collection`** into memory.
5. Run **100** similarity searches and **measure** how fast they are.

Run it:

```bash
python day1/milvus/code/03_lab_vector_search.py
```

It needs `pymilvus` and `numpy` (installed in setup) and the Milvus container running.

---

## What the script does (read along)

### 1. Connect and define the collection

```python
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
connections.connect(host="localhost", port="19530")
```

A schema with id, category metadata, and a 128-dim vector (see previous lesson).

### 2. Insert 50,000 vectors (in batches)

```python
import numpy as np
N, DIM = 50_000, 128
batch = 10_000
for start in range(0, N, batch):
    ids   = list(range(start, start + batch))
    cats  = np.random.choice(["weapon","potion","armor","spell"], batch).tolist()
    vecs  = np.random.random((batch, DIM)).tolist()
    collection.insert([ids, cats, vecs])
collection.flush()
```

We insert in **batches** of 10,000 so we never hold too much at once — a good habit for large loads.

### 3. Build the IVF-PQ index

```python
collection.create_index("embedding", {
    "index_type": "IVF_PQ", "metric_type": "L2",
    "params": {"nlist": 128, "m": 16, "nbits": 8},
})
```

### 4. Load into memory (do not forget!)

```python
collection.load()
```

### 5. Benchmark 100 searches

```python
import time
queries = np.random.random((100, DIM)).tolist()   # 100 random query vectors
start = time.time()
results = collection.search(
    data=queries, anns_field="embedding",
    param={"metric_type": "L2", "params": {"nprobe": 16}},
    limit=5,                       # top-5 nearest for each query
)
elapsed = time.time() - start
print(f"100 searches took {elapsed:.3f}s -> {elapsed/100*1000:.2f} ms each")
```

The script prints the total time and the average per-search time in milliseconds. On the training laptop expect each search to be just a few milliseconds even though it is choosing from 50,000 vectors — that is the power of the index.

### 6. Try a metadata filter

```python
results = collection.search(
    data=[queries[0]], anns_field="embedding",
    param={"metric_type": "L2", "params": {"nprobe": 16}},
    limit=5,
    expr='category == "weapon"',   # only search weapons
)
```

This is the real-world combo: *"find similar items, but only in this category."*

---

## What you achieved

- Loaded **50,000 vectors** at scale, in batches.
- Built an **IVF-PQ** index and learned what IVF and PQ each do.
- Remembered the crucial **`load_collection`** step.
- **Measured** search speed — real numbers, not guesses.
- Combined vector search with a **metadata filter**.

### Deliverable for this track
Commit the script and your benchmark numbers. In your notes, compare: *the PostgreSQL pgvector K-NN from this morning vs Milvus here — when would you use each?* (Hint: a few thousand vectors inside your main database vs millions needing a dedicated, fast, scalable service.)

**Full lab file:** [`code/03_lab_vector_search.py`](code/03_lab_vector_search.py)

➡️ You have now seen all four engines. Back to the day plan: **[../README.md](../README.md)**

---

## ⭐ Must-learn from this topic

- **Batch inserts** — loading large data in chunks, then `flush()`.
- **Build → load → search** — the required order before any query.
- **Search params** — `nprobe`, `limit` (top-k), and reading results.
- **Filtered search** — `expr='category == "weapon"'` alongside the vector search.

### 📚 Official docs
- [Single-Vector Search](https://milvus.io/docs/single-vector-search.md) — the search API.
- [Filtered search (boolean expressions)](https://milvus.io/docs/boolean.md) — metadata filters.
- [Insert, Upsert & Delete](https://milvus.io/docs/insert-update-delete.md) — loading data.
