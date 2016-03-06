import sqlite3 
import sys
import json 

conn = sqlite3.connect('hw4.db')
para = raw_input("")
paraElement = para.split()

genre_user = paraElement[0]
k = paraElement[1]

with sqlite3.connect('hw4.db') as con:
	c = con.cursor()
	c.execute("SELECT movie_actor.actor, count(*) as count_actor from movie_genre join movie_actor on (movie_actor.imdb_id = movie_genre.imdb_id) WHERE movie_genre.genre = '%s' group by movie_actor.actor order by count_actor DESC limit %s" %(genre_user, k))
	print '\n' + 'Top %s actors who played in most %s movies:' %(k, genre_user) + '\n' + 'Actor, %s Movies Played in' %genre_user
	for row in c.fetchall():
		print row[0].encode("utf-8") + ', ' + str(row[1])



