# import xml.etree.ElementTree as ET
import sqlite3 as sqlite
import sys
import json 

#--------------------------STEP 1--------------------------------######
movie_genreList = list()
movieList = list()
movie_actorList = list()

fhand = open('movie_actors_data.txt', 'rU')
for line in fhand:
	line = line.strip()
	lineJson = json.loads(line)  # turn json into python???

	imdb_id = lineJson["imdb_id"]
		# print imdb_id
	title = lineJson["title"]
		# print title
	year = lineJson["year"]
	rating =lineJson["rating"]
			# actor = lineJson["actors"]
		# movie_genre table
	for genre in lineJson["genres"]:
		# print genre
		movie_genreList.append((imdb_id, genre))
		# print movie_genreListElement[1]
	for actor in lineJson["actors"]:         #movie_actor table
		movie_actorList.append((imdb_id, actor))

	movieListElement = (imdb_id, title, year, rating)
	movieList.append(movieListElement)
	# print type(year)
	# movie_actorList.append(movie_actorListElement)
	# movie_genreList.append(movie_genreListElement)	
# print movieList

with sqlite.connect('hw4.db') as con:
	####movie_genre table
	c = con.cursor()
	c.execute("DROP TABLE IF EXISTS movie_genre")
	c.execute("CREATE TABLE movie_genre(imdb_id INT, genre TEXT)")
	c.executemany("INSERT INTO movie_genre VALUES (?,?)", movie_genreList)
  	con.commit()
  	######movie_genre table
  	c.execute("DROP TABLE IF EXISTS movie_actor")
	c.execute("CREATE TABLE movie_actor(imdb_id INT, actor TEXT)")
	c.executemany("INSERT INTO movie_actor VALUES (?,?)", movie_actorList)
	con.commit()
	#####movie table
	c.execute("DROP TABLE IF EXISTS movie")
	c.execute("CREATE TABLE movie(imdb_id INT, title TEXT, year int, rating text)")
	c.executemany("INSERT INTO movie VALUES (?,?,?,?)", movieList)
	con.commit()
	#######find top ten genre
	c.execute("SELECT genre, count(genre) as countGenre from movie_genre group by genre order by count(genre) DESC LIMIT 10")
	# rows = cur.fetchall()
	print 'Top ten genres:' + '\n' + 'Genre, Movies'
	for row in c.fetchall():
		# print type(row[0]), type(row[1])
		print row[0].encode('utf-8') + ', ' + str(row[1])
	########number of movies broken down by year in chronological order
	c.execute("SELECT year, count(title) as movies from movie group by year order by year")
	print '\n' + 'Movies broken down by year:' + '\n' + 'Year, Movies'
	for row in c.fetchall():
		# print type(row[0]), type(row[1])
		print str(row[0]) + ', ' + str(row[1])
	########all Sci-Fi movies order by decreasing rating, then by decreasing year if ratings are the same.
	c.execute("SELECT title, year, rating from movie join movie_genre on (movie.imdb_id = movie_genre.imdb_id) WHERE genre = 'Sci-Fi' order by rating DESC, year DESC")
	print '\n' + 'Sci-Fi movies:' + '\n' + 'Title, Year, Rating'
	for row in c.fetchall():
		# print type(row[0]), type(row[1])
		print row[0].encode('utf-8') + ', ' + str(row[1]) + ', ' + row[2].encode('utf-8')
	#########top 10 actors who played in most movies in and after year 2000
	c.execute("SELECT actor, count(actor) as countActor from movie_actor join movie on (movie_actor.imdb_id = movie.imdb_id) WHERE movie.year >= 2000 group by actor order by countActor DESC, actor ASC limit 10")
	print '\n' + 'In and after year 2000, top 10 actors who played in most movies:' + '\n' + 'Actor, Movies'
	for row in c.fetchall():
		# print type(row[0]), type(row[1])
		print row[0].encode('utf-8') + ', ' + str(row[1])
	###########finding pairs of actors who co-stared in 3 or more movies.
	c.execute("SELECT t1.actor, t2.actor, count(*) as countPair from movie_actor t1 join movie_actor t2 on (t1.imdb_id = t2.imdb_id) WHERE t1.actor < t2.actor group by t1.actor, t2.actor Having countPair >= 3 order by countPair DESC, t1.actor")
	print '\n' + 'Pairs of actors who co-stared in 3 or more movies:' + '\n' + 'Actor A, Actor B, Co-stared Movies'
	for row in c.fetchall():
		# print type(row[0]), type(row[1])
		print row[0].encode('utf-8') + ', ' + row[1].encode('utf-8') + ', ' + str(row[2])






