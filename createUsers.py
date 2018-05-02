#!/bin/python3
#!/usr/bin/env python3

import sqlite3
import os
from hashlib import md5

# Create the schema
def createUsers():
	conn = sqlite3.connect('foobar.db')
	c = conn.cursor()

	password = md5("password".encode('utf-8')).hexdigest()
	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("Jacob", "Carney", ?, "jacobsc@gmail.com", "INSTRUCTOR", "petName", "Joey")',  (password,))
	userdir = r'./userdirs/jacobsc@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)

	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("Tyler", "Zamora-Carden", ?, "tylerzc@gmail.com", "STUDENT", "maidenName", "")',  (password,))
	userdir = r'./userdirs/tylerzc@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)

	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("Heather", "Switzer", ?, "heatherms@gmail.com", "STUDENT", "elemSchool", "")',  (password,))
	userdir = r'./userdirs/heatherms@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)

	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("Ben", "Byrnes", ?, "benb@gmail.com", "STUDENT", "maidenName", "")',  (password,))
	userdir = r'./userdirs/benb@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)

	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("Brandon", "Lewis", ?, "brandontl@gmail.com", "STUDENT", "", "")',  (password,))
	userdir = r'./userdirs/brandontl@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)

	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("Julian", "Dymacek", ?, "dymacekjm@gmail.com", "INSTRUCTOR", "petName", "Todd")',  (password,))
	userdir = r'./userdirs/dymacekjm@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)
	
	c.execute('INSERT INTO class(instructorID, title, section, semester, year) VALUES(1, "Graph Theory", 1, "Fall", 2018)')
	c.execute('INSERT INTO class(instructorID, title, section, semester, year) VALUES(1, "Systems Programming", 1, "Fall", 2018)')
	c.execute('INSERT INTO class(instructorID, title, section, semester, year) VALUES(1, "Computer Science 162", 1, "Fall", 2018)')

	c.execute('INSERT INTO takes(userID, classID) VALUES(2, 2)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(2, 3)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(3, 1)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(4, 2)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(5, 1)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(5, 2)')
	c.execute('INSERT INTO takes(userID, classID) VALUES(5, 3)')

	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("The Royal and Most Pleasant Game of Goose","Placeholder", 1, "2018-1-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("NP Complete Graph Theory Problem","Placeholder", 1, "2018-10-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Libraries and Linking","Placeholder", 2, "2018-10-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Process Management","Placeholder", 2, "2018-10-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Tiny Shell","Placeholder", 2, "2018-10-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Pipes and the Cloud","Placeholder", 2, "2018-10-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Date Time","Placeholder", 3, "2018-10-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Recursive Plants","Placeholder", 3, "2018-10-10")')
	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Sorting","Placeholder", 3, "2018-10-10")')

	conn.commit()
	conn.close()

# Could put more in later
def main():
	createUsers()

if __name__ == "__main__":
	print("Running database user creation script.")
	main()
