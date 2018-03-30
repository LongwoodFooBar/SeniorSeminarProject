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

	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Tyler", "Zamora-Carden", ?, "tylerzc@gmail.com", "STUDENT")',  (password,))

	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Heather", "Switzer", ?, "heatherms@gmail.com", "STUDENT")',  (password,))

	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Ben", "Byrnes", ?, "benb@gmail.com", "STUDENT")',  (password,))

	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("Brandon", "Lewis", ?, "brandontl@gmail.com", "STUDENT")',  (password,))
	
	c.execute('INSERT INTO class(instructorID, title) VALUES(2, "Graph Theory")')
	c.execute('INSERT INTO class(instructorID, title) VALUES(2, "Systems Programming")')
	c.execute('INSERT INTO class(instructorID, title) VALUES(2, "Computer Science 162")')

	c.execute('INSERT INTO takes(userID, classID) VALUES(3, 2)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(3, 3)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(4, 1)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(5, 2)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(6, 1)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(6, 2)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(6, 3)')

	c.execute('INSERT INTO assignment(title, body, classID) VALUES("The Royal and Most Pleasant Game of Goose","Placeholder", 1)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("NP Complete Graph Theory Problem","Placeholder", 1)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("Libraries and Linking","Placeholder", 2)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("Process Management","Placeholder", 2)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("Tiny Shell","Placeholder", 2)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("Pipes and the Cloud","Placeholder", 2)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("Date Time","Placeholder", 3)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("Recursive Plants","Placeholder", 3)')
	c.execute('INSERT INTO assignment(title, body, classID) VALUES("Sorting","Placeholder", 3)')

	conn.commit()
	conn.close()

# Could put more in later
def main():
	createUsers()

if __name__ == "__main__":
	print("Running database creation script.")
	main()
