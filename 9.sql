SELECT name from
people JOIN stars ON people.id = stars.person_id JOIN
movies on stars.movie_id = movies.id
WHERE year = 2004 GROUP BY person_id ORDER BY birth;
