"""
Similarity search over the events stored by milvus_sink.py.
Embeds a sample event and finds the nearest stored events.

Run:  python milvus_search.py
Needs: pip install pymilvus numpy   and milvus_sink.py to have stored some events.
"""
import hashlib
import numpy as np
from pymilvus import connections, Collection

DIM = 8
COLLECTION = "pq_events"


def embed(player, points):
    h = hashlib.md5(f"{player}:{points}".encode()).digest()
    return (np.frombuffer(h[:DIM], dtype=np.uint8) / 255.0).tolist()


def main():
    connections.connect(host="localhost", port="19530")
    col = Collection(COLLECTION)
    col.load()

    query = embed("hero_07", 150)
    results = col.search(
        data=[query], anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 8}},
        limit=5, output_fields=["player"],
    )
    print("nearest stored events to (hero_07, 150):")
    for hit in results[0]:
        print(f"  id={hit.id} player={hit.entity.get('player')} distance={hit.distance:.4f}")


if __name__ == "__main__":
    main()
