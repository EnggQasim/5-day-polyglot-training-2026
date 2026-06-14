-- MVCC demo: see row versions and the hidden xmin/xmax columns.
-- Best run line-by-line in psql so you can watch what changes.

-- 1) look at the hidden version columns
SELECT player_id, username, score, xmin, xmax
FROM players
WHERE username = 'hero_07';

-- 2) update creates a NEW version (xmin will change)
UPDATE players SET score = score + 100 WHERE username = 'hero_07';

SELECT player_id, username, score, xmin, xmax
FROM players
WHERE username = 'hero_07';

-- 3) clean up dead old versions
VACUUM (VERBOSE) players;

-- ----------------------------------------------------------
-- Two-session test (run these in TWO separate psql windows):
--
-- Window 1:
--   BEGIN;
--   UPDATE players SET score = 9999 WHERE username = 'hero_07';
--   -- (do not commit yet)
--
-- Window 2 (sees the OLD value because window 1 has not committed):
--   SELECT username, score FROM players WHERE username = 'hero_07';
--
-- Window 1:
--   COMMIT;
--
-- Window 2 (now sees 9999):
--   SELECT username, score FROM players WHERE username = 'hero_07';
-- ----------------------------------------------------------
