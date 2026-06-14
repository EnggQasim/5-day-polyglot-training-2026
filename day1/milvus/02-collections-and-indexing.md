# Milvus — Step 2: Collections, metadata, and IVF-PQ indexing

## A collection = a table for vectors

In Milvus you first define a **schema**: the fields each record has. For Pixel Quest items we use three fields:

- `item_id` — a number, the primary key.
- `category` — a short text label (e.g. "weapon", "potion"). This is **metadata** — extra info we can filter on.
- `embedding` — the 128-number vector.

```python
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection

fields = [
    FieldSchema(name="item_id",  dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=32),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128),
]
schema = CollectionSchema(fields, description="Pixel Quest item vectors")
collection = Collection(name="pq_items", schema=schema)
```

**Metadata matters:** because we stored `category`, we can later say "find similar items, *but only weapons*". Vector search + metadata filter together is what makes these systems useful.

---

## Inserting vectors

You insert columns of data. For 5 items it looks like this (the lab does 50,000):

```python
import numpy as np
ids        = [1, 2, 3, 4, 5]
categories = ["weapon", "weapon", "potion", "armor", "weapon"]
vectors    = np.random.random((5, 128)).tolist()   # 5 random 128-dim vectors

collection.insert([ids, categories, vectors])
collection.flush()    # make sure data is written
```

---

## Indexing: why IVF-PQ?

Searching every vector one by one ("brute force") is accurate but slow when you have millions. An **index** trades a tiny bit of accuracy for a huge speed gain. Milvus offers several; a popular one is **IVF-PQ**.

Break the name into two easy ideas:

- **IVF = Inverted File.** First, Milvus groups vectors into **clusters** (`nlist` of them). At search time it only looks inside the few clusters nearest your query, not all of them. (Like searching only the relevant aisles of a shop, not every shelf.)
- **PQ = Product Quantization.** It **compresses** each vector into a small code, so millions fit in memory and comparisons are fast. (Like storing a rough sketch of each vector instead of the full picture.)

Together: **IVF narrows down where to look, PQ makes each comparison cheap.** Result: fast search over huge data, using less memory.

```python
index_params = {
    "index_type": "IVF_PQ",
    "metric_type": "L2",        # L2 = straight-line distance
    "params": {
        "nlist": 128,           # number of clusters
        "m": 16,                # PQ: split 128 dims into 16 sub-parts
        "nbits": 8,             # bits per sub-part code
    },
}
collection.create_index(field_name="embedding", index_params=index_params)
```

> **Tuning knobs:** more `nlist` = finer clusters (often more accurate, a bit slower to build). At search time, `nprobe` decides how many clusters to check — higher `nprobe` = more accurate but slower. You balance speed vs accuracy.

---

## load_collection: vectors must be in memory to search

This is a Milvus gotcha worth remembering. Milvus keeps data on disk by default. **Before you can search, you must load the collection into memory:**

```python
collection.load()     # without this, a search will fail or return nothing
```

When finished, you can free memory with `collection.release()`.

**Why:** searching needs the index in RAM for speed. `load_collection` is the step beginners most often forget.

➡️ Next: the lab — **[03-lab-vector-search.md](03-lab-vector-search.md)**

---

## ⭐ Must-learn from this topic

- **Collection schema** — primary key, `VARCHAR` metadata, `FLOAT_VECTOR` with a `dim`.
- **Metadata filtering** — combining similarity search with an `expr` filter.
- **IVF-PQ** — IVF clusters (`nlist` / `nprobe`) + PQ compression (`m` / `nbits`); the speed/accuracy trade-off.
- **`load_collection`** — data must be loaded into memory **before** searching.

### 📚 Official docs
- [Manage Collections](https://milvus.io/docs/manage-collections.md) — schema and creation.
- [Index Vector Fields](https://milvus.io/docs/index-vector-fields.md) — building indexes.
- [IVF_PQ](https://milvus.io/docs/ivf-pq.md) — this index explained, with parameters.
- [Load & Release](https://milvus.io/docs/load-and-release-collection.md) — the load step.
