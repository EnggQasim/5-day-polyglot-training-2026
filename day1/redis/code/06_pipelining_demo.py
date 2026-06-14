"""
Redis pipelining demo: compare 1000 one-by-one writes vs one pipelined batch.

Run:  python 06_pipelining_demo.py
Needs: pip install redis   (done in setup) and the Redis container running.
"""
import time
import redis


def main():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    assert r.ping(), "Redis is not responding"
    r.delete("leaderboard")

    # WITHOUT pipelining: 1000 separate round-trips
    start = time.time()
    for i in range(1000):
        r.zadd("leaderboard", {f"player_{i}": i})
    slow = time.time() - start
    print(f"one-by-one : {slow*1000:.1f} ms")

    r.delete("leaderboard")

    # WITH pipelining: queue all 1000, send in one round-trip
    start = time.time()
    pipe = r.pipeline()
    for i in range(1000):
        pipe.zadd("leaderboard", {f"player_{i}": i})
    pipe.execute()
    fast = time.time() - start
    print(f"pipelined  : {fast*1000:.1f} ms")

    if fast > 0:
        print(f"speed-up   : {slow/fast:.1f}x faster")


if __name__ == "__main__":
    main()
