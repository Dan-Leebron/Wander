SELECT name FROM people JOIN stars on people.id = stars.person_id
WHERE movie_id IN (SELECT movie_id FROM stars JOIN people ON stars.person_id = people.id WHERE name = 'Kevin Bacon' AND birth = 1958)
AND NOT name = 'Kevin Bacon' GROUP BY people.id;