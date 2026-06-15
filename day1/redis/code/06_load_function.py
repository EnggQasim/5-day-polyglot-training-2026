"""
Load and call the 'pq' Redis Functions library from Python (no shell quoting pain).

Run:  python 06_load_function.py
Needs: pip install redis   and the Redis container running.
"""
import os
import redis

HERE = os.path.dirname(__file__)


def main():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    assert r.ping(), "Redis is not responding"

    # read the Lua library file
    with open(os.path.join(HERE, "06_functions.lua")) as f:
        code = f.read()

    # load it (replace=True so you can re-run this script after edits)
    r.function_load(code, replace=True)
    print("loaded library 'pq'")

    # set up a leaderboard and call the function a few times
    r.delete("leaderboard")
    r.zadd("leaderboard", {"hero_07": 4200, "elf_mona": 7300, "mage_lily": 5100})

    # FCALL add_and_rank, 1 key (leaderboard), args: member, points
    new_rank = r.fcall("add_and_rank", 1, "leaderboard", "hero_07", 250)
    print(f"hero_07 after +250 -> rank {new_rank} (0 = top)")

    new_rank = r.fcall("add_and_rank", 1, "leaderboard", "hero_07", 5000)
    print(f"hero_07 after +5000 -> rank {new_rank} (0 = top)")

    # show the final board
    print("leaderboard:", r.zrevrange("leaderboard", 0, -1, withscores=True))


if __name__ == "__main__":
    main()
