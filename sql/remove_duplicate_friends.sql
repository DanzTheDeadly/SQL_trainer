INSERT INTO friends
SELECT
  user_id
, friend_id
FROM friends_duplicates
EXCEPT
SELECT
  friend_id
, user_id
FROM friends_duplicates;

DROP TABLE friends_duplicates;
