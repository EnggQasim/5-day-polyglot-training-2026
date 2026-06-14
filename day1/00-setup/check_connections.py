"""
Day 1 setup checker.

Tries to connect to all four Day 1 databases and prints OK or the error
for each one. Run it after `docker compose up -d`.

Usage:
    python day1/00-setup/check_connections.py
"""

def check_postgres():
    import psycopg2
    conn = psycopg2.connect(
        host="localhost", port=5432,
        user="trainer", password="trainer", dbname="pixelquest",
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    cur.close()
    conn.close()
    return version.split(",")[0]   # short version string


def check_redis():
    import redis
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    return "PONG" if r.ping() else "no reply"


def check_neo4j():
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(
        "bolt://localhost:7687", auth=("neo4j", "trainer123")
    )
    with driver.session() as session:
        result = session.run("RETURN 1 AS ok")
        rows = result.single()["ok"]
    driver.close()
    return f"{rows} test row returned"


def check_milvus():
    from pymilvus import connections, utility
    connections.connect(alias="default", host="localhost", port="19530")
    # if this call works, the server is reachable
    _ = utility.list_collections()
    connections.disconnect("default")
    return "server reachable"


def main():
    checks = [
        ("PostgreSQL", check_postgres),
        ("Redis", check_redis),
        ("Neo4j", check_neo4j),
        ("Milvus", check_milvus),
    ]
    all_ok = True
    for name, func in checks:
        try:
            detail = func()
            print(f"{name:<10} : OK  ({detail})")
        except Exception as e:
            all_ok = False
            print(f"{name:<10} : FAILED -> {e}")

    print()
    if all_ok:
        print("All good. You are ready for Day 1.")
    else:
        print("Some checks failed. Fix them before starting the lessons.")
        print("Tip: wait a minute for containers to become healthy, then retry.")


if __name__ == "__main__":
    main()
