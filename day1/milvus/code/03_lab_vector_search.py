"""
Milvus LAB: insert 50k vectors, build an IVF-PQ index, load, and benchmark 100 searches.

Run:  python 03_lab_vector_search.py
Needs: pip install pymilvus numpy   (done in setup)
       Milvus container running (docker compose up -d)
"""
import time
import numpy as np
from pymilvus import (
    connections, utility,
    FieldSchema, CollectionSchema, DataType, Collection,
)

COLLECTION = "pq_items"
N = 50_000        # total vectors
DIM = 128         # dimensions per vector
BATCH = 10_000    # insert in chunks


def main():
    connections.connect(host="localhost", port="19530")
    print("Connected to Milvus.")

    # start clean so the script can be re-run
    if utility.has_collection(COLLECTION):
        utility.drop_collection(COLLECTION)

    # 1) schema: id + category metadata + 128-dim vector
    fields = [
        FieldSchema(name="item_id",  dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=32),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIM),
    ]
    schema = CollectionSchema(fields, description="Pixel Quest item vectors")
    collection = Collection(name=COLLECTION, schema=schema)
    print("Collection created.")

    # 2) insert 50k vectors in batches
    cats = ["weapon", "potion", "armor", "spell"]
    t0 = time.time()
    for start in range(0, N, BATCH):
        ids  = list(range(start, start + BATCH))
        c    = np.random.choice(cats, BATCH).tolist()
        vecs = np.random.random((BATCH, DIM)).tolist()
        collection.insert([ids, c, vecs])
    collection.flush()
    print(f"Inserted {N} vectors in {time.time() - t0:.1f}s.")

    # 3) build IVF-PQ index
    collection.create_index("embedding", {
        "index_type": "IVF_PQ",
        "metric_type": "L2",
        "params": {"nlist": 128, "m": 16, "nbits": 8},
    })
    print("IVF-PQ index built.")

    # 4) load into memory (REQUIRED before searching)
    collection.load()
    print("Collection loaded into memory.")

    # 5) benchmark 100 searches
    queries = np.random.random((100, DIM)).tolist()
    t0 = time.time()
    results = collection.search(
        data=queries, anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 16}},
        limit=5,
    )
    elapsed = time.time() - t0
    print(f"100 searches took {elapsed:.3f}s  ->  {elapsed/100*1000:.2f} ms each")
    print("First query top-5 item_ids:", results[0].ids)

    # 6) vector search WITH a metadata filter
    filtered = collection.search(
        data=[queries[0]], anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 16}},
        limit=5,
        expr='category == "weapon"',
    )
    print("Top-5 weapons only:", filtered[0].ids)

    collection.release()   # free memory
    print("Done. Collection released from memory.")


if __name__ == "__main__":
    main()
