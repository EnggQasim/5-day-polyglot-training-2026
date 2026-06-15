"""
Custom Kafka -> Milvus sink: consume player-scores, embed each event,
and store it in Milvus for later similarity search.

Run:  python milvus_sink.py     (Ctrl+C to stop)
Needs: pip install confluent-kafka pymilvus numpy
       Day 1 Milvus + Day 2 Kafka up, events flowing on 'player-scores'.
"""
import hashlib
import json

import numpy as np
from confluent_kafka import Consumer
from pymilvus import (
    connections, utility, Collection, CollectionSchema, FieldSchema, DataType,
)

DIM = 8
COLLECTION = "pq_events"


def get_collection():
    connections.connect(host="localhost", port="19530")
    if not utility.has_collection(COLLECTION):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="player", dtype=DataType.VARCHAR, max_length=32),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIM),
        ]
        col = Collection(COLLECTION, CollectionSchema(fields, "Pixel Quest events"))
        col.create_index("embedding", {"index_type": "IVF_FLAT", "metric_type": "L2",
                                       "params": {"nlist": 16}})
    else:
        col = Collection(COLLECTION)
    col.load()
    return col


def embed(event):
    # deterministic toy embedding (a real system would use an AI model)
    h = hashlib.md5(f"{event['player']}:{event['points']}".encode()).digest()
    return (np.frombuffer(h[:DIM], dtype=np.uint8) / 255.0).tolist()


def main():
    col = get_collection()
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "milvus-sink",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(["player-scores"])
    print("Kafka -> Milvus sink running... (Ctrl+C to stop)")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("error:", msg.error())
                continue
            e = json.loads(msg.value())
            col.insert([[e["player"]], [embed(e)]])
            print(f"stored embedding for {e['player']}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
