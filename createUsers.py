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
	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("Longwood", "ACM", ?, "longwoodacm@gmail.com", "INSTRUCTOR", "petName", "Captain")',  (password,))
	userdir = r'./userdirs/longwoodacm@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)

	password = md5("password".encode('utf-8')).hexdigest()
	c.execute('INSERT INTO login(firstName, lastName, password, email, position, question, answer) VALUES("First", "Team", ?, "Team1@gmail.com", "STUDENT", "petName", "Captain")',  (password,))
	userdir = r'./userdirs/Team1@gmail.com'
	if not os.path.exists(userdir):
		os.makedirs(userdir)
	
	c.execute('INSERT INTO class(instructorID, title, section, semester, year) VALUES(1, "Programming Competition 2018", 1, "Fall", 2018)')
	
	c.execute('INSERT INTO takes(userID, classID) VALUES(2, 1)')

	c.execute('INSERT INTO assignment(title, body, classID, dueDate) VALUES("Problem #1","Placeholder", 1, "2018-1-10")')


	conn.commit()
	conn.close()

# Could put more in later
def main():
	createUsers()

if __name__ == "__main__":
	print("Running database user creation script.")
	main()
