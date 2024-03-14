SELECT
  city
, name
, total
FROM (
  SELECT
    city
  , name
  , count(user_id) as total
  FROM users
  GROUP BY city, name
) t
ORDER BY total DESC
LIMIT 1