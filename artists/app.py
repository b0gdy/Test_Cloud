import mysql.connector
from mysql.connector import connect, Error
import json
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Application artists'

@app.route('/create-database')
def createDatabase():
	with connect(host='mysqldb', user='root', password='p@ssw0rd1') as connection:
		try:
			drop_database_query = "DROP DATABASE IF EXISTS projectdb"
			create_database_query = "CREATE DATABASE projectdb"
			with connection.cursor() as cursor:
				cursor.execute(drop_database_query)
				cursor.execute(create_database_query)
				connection.commit()
				return 'Database created'
				
		except errors.DatabaseError:
			pass

@app.route('/create-table')
def createTable():
	with connect(host='mysqldb', user='root', password='p@ssw0rd1', database="projectdb") as connection:
		try:
			drop_table_query = "DROP TABLE IF EXISTS artists"
			create_table_query = "CREATE TABLE artists (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(255), PRIMARY KEY (id))"
			with connection.cursor() as cursor:
				cursor.execute(drop_table_query)
				cursor.execute(create_table_query)
				connection.commit()
				return 'Table artists created'
				
		except errors.ProgrammingError:
			pass

@app.route('/artists/add', methods=('GET', 'POST'))
def addArtist():
	if request.method == 'POST':
		name = request.form['name']
		with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
			insert_query = "INSERT INTO artists (name) VALUES (%s)"
			data_query = [name]
			with connection.cursor() as cursor:
				cursor.execute(insert_query, data_query)
				connection.commit()
				#return redirect(url_for('getArtists'))
				return 'Artist added'
				
	return render_template('addArtist.html')
	
@app.route('/artists')
def getArtists():
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = "SELECT * FROM artists"
		with connection.cursor() as cursor:
			cursor.execute(select_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			artists=[]
			for row in result:
				artists.append(dict(zip(row_header, row)))
			connection.commit()
			#return jsonify(artists)
			return render_template('listArtists.html', artists=artists)

class Artist:
	def __init__(self, id, name):
		self.id = id
		self.name = name

	def getId(self):
		return self.id
	
	def getName(self):
		return self.name
	
	def setId(self, id):
		self.id = id
	
	def setName(self, name):
		self.name = name

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5000)
