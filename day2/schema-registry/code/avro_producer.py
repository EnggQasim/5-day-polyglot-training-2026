"""
Avro producer: send typed PlayerScore events, validated by the Schema Registry.

Run:  python avro_producer.py
Needs: pip install "confluent-kafka[avro]" requests   and the Day 2 stack running.
"""
import os
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

TOPIC = "pq-scores"
HERE = os.path.dirname(__file__)


def main():
    with open(os.path.join(HERE, "player_score.avsc")) as f:
        schema_str = f.read()

    sr = SchemaRegistryClient({"url": "http://localhost:8081"})
    avro_serializer = AvroSerializer(sr, schema_str)

    producer = SerializingProducer({
        "bootstrap.servers": "localhost:9092",
        "key.serializer": StringSerializer("utf_8"),
        "value.serializer": avro_serializer,
    })

    scores = [
        {"player": "hero_07", "points": 150},
        {"player": "elf_mona", "points": 500},
        {"player": "ninja_sara", "points": 300},
    ]

    for s in scores:
        producer.produce(topic=TOPIC, key=s["player"], value=s)
        print(f"produced PlayerScore(player={s['player']}, points={s['points']})")

    producer.flush()
    print("schema registered under subject 'pq-scores-value'")


if __name__ == "__main__":
    main()
