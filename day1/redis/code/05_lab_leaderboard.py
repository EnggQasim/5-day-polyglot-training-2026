"""
Redis LAB: live leaderboard with pipelining + JSON profiles + AOF durability.

Run:  python 05_lab_leaderboard.py
Needs: pip install redis   (done in setup)
"""
import random
import redis


def main():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    assert r.ping(), "Redis is not responding"
    print("Connected to Redis.")

    # start clean
    r.delete("leaderboard")

    # 1) bulk-load 1000 players using a pipeline (one round-trip)
    pipe = r.pipeline()
    for i in range(1000):
        pipe.zadd("leaderboard", {f"player_{i}": random.randint(0, 10000)})
    pipe.execute()
    print("Loaded 1000 players with a pipeline.")

    # 2) read the top 5 and one player's rank
    top5 = r.zrevrange("leaderboard", 0, 4, withscores=True)
    print("Top 5:", top5)
    print("Rank of player_0 (0 = first):", r.zrevrank("leaderboard", "player_0"))

    # 3) store a profile as JSON (RedisJSON)
    r.execute_command(
        "JSON.SET", "profile:player_0", "$",
        '{"name":"player_0","country":"PK","level":7}',
    )
    print("Profile:", r.execute_command("JSON.GET", "profile:player_0"))

    # 4) durability test: turn AOF on, write a value, rewrite the AOF log
    r.config_set("appendonly", "yes")
    r.config_set("appendfsync", "everysec")
    r.zadd("leaderboard", {"durable_player": 9999})
    r.execute_command("BGREWRITEAOF")
    print("Wrote durable_player=9999 with AOF on.")
    print("Now run:  docker compose restart redis")
    print("Then:     docker exec -it pq_redis redis-cli ZSCORE leaderboard durable_player")
    print("It should still print 9999 after the restart.")


if __name__ == "__main__":
    main()
