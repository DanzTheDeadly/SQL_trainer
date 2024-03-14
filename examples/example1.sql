SELECT
  city
, name
, count(user_id) as total
FROM users
GROUP BY city, name
HAVING count(user_id) > 3