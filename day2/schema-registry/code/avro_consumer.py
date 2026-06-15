"""
Avro consumer: read PlayerScore events, decoding via the Schema Registry.

Run:  python avro_consumer.py    (Ctrl+C to stop)
Needs: pip install "confluent-kafka[avro]" requests   and the Day 2 stack running.

The consumer does NOT hard-code the schema: it reads the schema id embedded in
each message and fetches the schema from the registry to decode it.
"""
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

TOPIC = "pq-scores"


def main():
    sr = SchemaRegistryClient({"url": "http://localhost:8081"})
    avro_deserializer = AvroDeserializer(sr)

    consumer = DeserializingConsumer({
        "bootstrap.servers": "localhost:9092",
        "key.deserializer": StringDeserializer("utf_8"),
        "value.deserializer": avro_deserializer,
        "group.id": "avro-score-readers",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe([TOPIC])
    print("listening for Avro messages... (Ctrl+C to stop)")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("error:", msg.error())
                continue
            value = msg.value()      # already a dict, decoded via the registry
            print(f"{value['player']} -> {value['points']}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
