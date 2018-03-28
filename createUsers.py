#!/usr/bin/env python3

import sqlite3
from hashlib import md5

# Create the schema
def createUsers():
	conn = sqlite3.connect('foobar.db')
	c = conn.cursor()

	password = md5("foobar".encode('utf-8')).hexdigest()
	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("ADMIN", "ADMIN", ?, "admin", "ADMIN")',  (password,))

	password = md5("password".encode('utf-8')).hexdigest()
	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Jacob", "Carney", ?, "jacobsc@gmail.com", "INSTRUCTOR")',  (password,))

	password = md5("pass".encode('utf-8')).hexdigest()
	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Tyler", "Zamora-Carden", ?, "tylerzc@gmail.com", "STUDENT")',  (password,))

	password = md5("pass".encode('utf-8')).hexdigest()
	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Heather", "Switzer", ?, "heatherms@gmail.com", "STUDENT")',  (password,))

	password = md5("pass".encode('utf-8')).hexdigest()
	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Ben", "Byrnes", ?, "benb@gmail.com", "STUDENT")',  (password,))
	
	c.execute('INSERT INTO class(instructorID, title) VALUES(2, "Graph Theory")')
	c.execute('INSERT INTO class(instructorID, title) VALUES(2, "Systems Programming")')
	c.execute('INSERT INTO class(instructorID, title) VALUES(2, "Computer Science 162")')

	c.execute('INSERT INTO takes(userID, classID) VALUES(3, 2)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(3, 3)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(4, 1)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(5, 2)')

	conn.commit()
	conn.close()

# Could put more in later
def main():
	createUsers()

if __name__ == "__main__":
	print("Running database creation script.")
	main()
