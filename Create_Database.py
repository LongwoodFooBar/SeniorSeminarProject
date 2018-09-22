#!/bin/python3
#!/usr/bin/env python3

import sqlite3

# Create the schema
def createSchema():
	conn = sqlite3.connect('acm.db')
	c = conn.cursor()

	c.execute('''CREATE TABLE IF NOT EXISTS login (
		userID INTEGER PRIMARY KEY AUTOINCREMENT,
		firstName TEXT,
		lastName TEXT,
		password TEXT,
		score INTEGER,
		email TEXT UNIQUE,
		position TEXT,
		question TEXT,
		answer TEXT
	)''')

	c.execute('''CREATE TABLE IF NOT EXISTS class (
		classID INTEGER PRIMARY KEY AUTOINCREMENT,
		instructorID INTEGER,
		title TEXT,
		section INTEGER,
		semester TEXT,
		year INTEGER,
		UNIQUE(title, section, semester, year),
		FOREIGN KEY (instructorID) REFERENCES login(userID)
	) ''')

	c.execute('''CREATE TABLE IF NOT EXISTS assignment (
		assignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		body TEXT,
		classID INTEGER,
		dueDate TEXT,
		FOREIGN KEY (classID) REFERENCES class(classID)
	) ''')

	# Creates the upload table
	# upload type refers to a test file or a handout/assignment
	c.execute('''CREATE TABLE IF NOT EXISTS uploads (
		userID INTEGER,
		uploadID INTEGER PRIMARY KEY AUTOINCREMENT,
		assignmentID INTEGER,
		fileLocation TEXT,
		type TEXT,
		completed INTEGER,
		language TEXT,
		FOREIGN KEY (userID) REFERENCES login(userID),
		FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID)
        ) ''')

	c.execute('''CREATE TABLE IF NOT EXISTS testCases (
		testID INTEGER PRIMARY KEY,
		assignmentID INTEGER,
		inputValue TEXT,
		outputValue TEXT,
		userID INTEGER,
		type TEXT,
	    FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID),
	    FOREIGN KEY (userID) REFERENCES login(userID)
        ) ''')

	c.execute('''CREATE TABLE IF NOT EXISTS takes (
	    userID INTEGER,
	    classID INTEGER,
	    FOREIGN KEY (userID) REFERENCES login(userID),
	    FOREIGN KEY (classID) REFERENCES class(classID),
	    PRIMARY KEY (userID, classID)
	)''')

	c.execute('''CREATE TABLE IF NOT EXISTS grades (
		userID INTEGER,
		assignmentID INTEGER,
		grade INTEGER,
		comment TEXT,
		FOREIGN KEY (userID) REFERENCES login(userID),
		FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID),
		PRIMARY KEY (userID, assignmentID)
	)''')

	conn.commit()
	conn.close()

# Could put more in later
def main():
	createSchema()

if __name__ == "__main__":
	print("Running database creation script.")
	main()
