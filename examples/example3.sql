SELECT
  city
, name
, total
, pos
FROM (
  SELECT
    city
  , name
  , total
  , row_number() OVER (PARTITION BY city ORDER BY total DESC) AS pos
  FROM (
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
    ) t1
  ) t2
) t3
WHERE pos <= 3