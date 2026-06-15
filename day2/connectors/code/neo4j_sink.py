"""
A runnable Kafka -> Neo4j "mini sink": consume player-scores and upsert
:Player nodes into the Day 1 Neo4j. (A sink is just a consumer that writes
to a target system.)

Run:  python neo4j_sink.py      (Ctrl+C to stop)
Needs: pip install confluent-kafka neo4j
       Day 1 Neo4j + Day 2 Kafka up, and events flowing on 'player-scores'.
"""
import json
from confluent_kafka import Consumer
from neo4j import GraphDatabase

CYPHER = """
MERGE (p:Player {name: $player})
  ON CREATE SET p.score = $points
  ON MATCH  SET p.score = coalesce(p.score, 0) + $points
"""


def main():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "trainer123"))
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "neo4j-sink",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(["player-scores"])
    print("Kafka -> Neo4j sink running... (Ctrl+C to stop)")

    try:
        with driver.session() as session:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("error:", msg.error())
                    continue
                e = json.loads(msg.value())
                session.run(CYPHER, player=e["player"], points=e["points"])
                print(f"upserted {e['player']} (+{e['points']})")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        driver.close()


if __name__ == "__main__":
    main()
