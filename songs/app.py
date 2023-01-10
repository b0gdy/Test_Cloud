import mysql.connector
from mysql.connector import connect, Error
import json
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Application songs'

@app.route('/create-table')
def createTable():
	with connect(host='mysqldb', user='root', password='p@ssw0rd1', database="projectdb") as connection:
		try:
			drop_table_query = "DROP TABLE IF EXISTS songs"
			create_table_query = "CREATE TABLE songs (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(255), artistId INT, PRIMARY KEY (id), FOREIGN KEY(artistId) REFERENCES artists(id))"
			with connection.cursor() as cursor:
				cursor.execute(drop_table_query)
				cursor.execute(create_table_query)
				connection.commit()
				return 'Table songs created'
		
		except errors.ProgrammingError:
			pass

@app.route('/songs/add', methods=('GET', 'POST'))
def addSong():
	if request.method == 'POST':
		name = request.form['name']
		artistId = request.form['artistId']
		with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
			insert_query = "INSERT INTO songs (name, artistId) VALUES (%s, %s)"
			data_query = [name, artistId]
			with connection.cursor() as cursor:
				cursor.execute(insert_query, data_query)
				connection.commit()
				#return redirect(url_for('getSongs'))
				return 'Song added'
	
	return render_template('addSong.html')
	
@app.route('/songs')
def getSongs():
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = "SELECT * FROM songs"
		with connection.cursor() as cursor:
			cursor.execute(select_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			songs=[]
			for row in result:
				songs.append(dict(zip(row_header, row)))
			connection.commit()
			return render_template('listSongs.html', songs=songs)

@app.route('/all')
def getAll():
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = """SELECT s.id AS 'song.id', s.name AS 'song.name', s.artistId AS 'song.artistId', a.name AS 'artist.name'
		FROM songs s
		JOIN artists a
		ON s.artistId = a.id
		"""
		with connection.cursor() as cursor:
			cursor.execute(select_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			songs=[]
			for row in result:
				songs.append(dict(zip(row_header, row)))
			connection.commit()
			#return jsonify(songs)
			return render_template('listAll.html', songs=songs)

class Song:
	def __init__(self, id, name, artistId):
		self.id = id
		self.name = name
		self.artistId = artistId

	def getId(self):
		return self.id
	
	def getName(self):
		return self.name

	def getArtistId(self):
		return self.artistId
	
	def setId(self, id):
		self.id = id
	
	def setName(self, name):
		self.name = name
	
	def setArtistId(self, artistId):
		self.artistId = artistId

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5001)
