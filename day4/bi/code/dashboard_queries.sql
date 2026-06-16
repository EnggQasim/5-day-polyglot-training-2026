-- The four Pixel Quest BI questions, as plain SQL.
-- Paste each into Metabase's SQL editor, or verify in psql:
--   docker exec -i pq_postgres psql -U trainer -d pixelquest < dashboard_queries.sql

-- 1) Top 10 players
SELECT username, score
FROM players
ORDER BY score DESC
LIMIT 10;

-- 2) Average score by country
SELECT country, ROUND(AVG(score)) AS avg_score, COUNT(*) AS players
FROM players
GROUP BY country
ORDER BY avg_score DESC;

-- 3) Coins spent over time (per day)
SELECT date_trunc('day', bought_at) AS day, SUM(coins) AS coins_spent
FROM purchases
GROUP BY day
ORDER BY day;

-- 4) Players per country
SELECT country, COUNT(*) AS players
FROM players
GROUP BY country
ORDER BY players DESC;
