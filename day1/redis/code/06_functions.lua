#!lua name=pq
-- A Redis Functions library named "pq" (Pixel Quest).
-- It defines one function: add_and_rank.
--
-- add_and_rank(key, member, points):
--   1) add `points` to `member` in the sorted set `key`  (ZINCRBY)
--   2) return that member's new rank, 0 = top            (ZREVRANK)
--
-- FCALL passes keys and args separately:
--   keys[1] = the sorted set name   (e.g. leaderboard)
--   args[1] = the member            (e.g. hero_07)
--   args[2] = the points to add     (e.g. 250)

redis.register_function('add_and_rank', function(keys, args)
  redis.call('ZINCRBY', keys[1], args[2], args[1])
  return redis.call('ZREVRANK', keys[1], args[1])
end)
