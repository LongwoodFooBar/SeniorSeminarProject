#!/usr/bin/env python3

import sqlite3
from hashlib import md5

# Create the schema
def createSchema():
	conn = sqlite3.connect('foobar.db')
	c = conn.cursor()

	# Creates the login table
	# Position used to denote teacher or student
	# password possibly stored as a hash?
	c.execute('''CREATE TABLE IF NOT EXISTS login (
		userID INTEGER PRIMARY KEY AUTOINCREMENT,
		firstName TEXT,
		lastName TEXT,
		password TEXT,
		email TEXT,
		position TEXT
	)''')

	# Creates the class table
	# instructor is who is the main teacher (handles student teacher cases)
	c.execute('''CREATE TABLE IF NOT EXISTS class (
		classID INTEGER,
		userID INTEGER,
		instructor TEXT,
                PRIMARY KEY (classID, userID),
		FOREIGN KEY (userID) REFERENCES login(userID)
	) ''')

	# Creates the assignment table
	# Mostly connects the tables together with the test cases along with searching
	c.execute('''CREATE TABLE IF NOT EXISTS assignment (
		assignmentID INTEGER,
		classID INTEGER,
		PRIMARY KEY (assignmentID, classID),
		FOREIGN KEY (classID) REFERENCES class(classID)
	) ''')

	# Creates the upload table
	# upload type refers to a test file or a handout/assignment
	c.execute('''CREATE TABLE IF NOT EXISTS uploads (
		userID INTEGER,
		assignmentID INTEGER,
		classID INTEGER,
		fileLocation TEXT,
		type TEXT,
		PRIMARY KEY (userID, assignmentID, classID),
		FOREIGN KEY (userID) REFERENCES login(userID),
		FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID)
	) ''')

	# Creates the test cases table
	# Type is to denote if test case is teacher, student, or secret
	# teacher can be used by class, student by individual or class, and grading for grading
	c.execute('''CREATE TABLE IF NOT EXISTS testCases (
		testID INTEGER PRIMARY KEY,
		classID INTEGER,
		assignmentID INTEGER,
		inputValue TEXT,
		outputValue TEXT,
		userID INTEGER,
		type TEXT,
		FOREIGN KEY (classID) REFERENCES class(classID),
		FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID),
		FOREIGN KEY (userID) REFERENCES login(userID)
	) ''')

	password = md5("foobar".encode('utf-8')).hexdigest()
	
	print(password)
	c.execute('INSERT INTO login(firstName, lastName, password, email, position) VALUES("ADMIN", "ADMIN", ?, "admin", "ADMIN")',  (password,))
	conn.commit()
	conn.close()

# Could put more in later
def main():
	createSchema()

if __name__ == "__main__":
	print("Running database creation script.")
	main()
