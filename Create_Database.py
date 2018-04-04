#!/bin/python3
#!/usr/bin/env python3

import sqlite3

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
		classID INTEGER PRIMARY KEY AUTOINCREMENT,
		instructorID INTEGER,
		title TEXT,
		FOREIGN KEY (instructorID) REFERENCES login(userID)
	) ''')

	# Creates the assignment table
	# Mostly connects the tables together with the test cases along with searching
	c.execute('''CREATE TABLE IF NOT EXISTS assignment (
		assignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		body TEXT,
		classID INTEGER,
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
		FOREIGN KEY (userID) REFERENCES login(userID),
		FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID)
        ) ''')

	# Creates the test cases table
	# Type is to denote if test case is teacher, student, or secret
	# teacher can be used by class, student by individual or class, and grading for grading
	c.execute('''CREATE TABLE IF NOT EXISTS testCases (
		testID INTEGER PRIMARY KEY,
		uploadID INTEGER,
		inputValue TEXT,
		outputValue TEXT,
		type TEXT,
	        FOREIGN KEY (uploadID) REFERENCES uploads(uploadID)
        ) ''')

	c.execute('''CREATE TABLE IF NOT EXISTS takes (
	    userID INTEGER,
	    classID INTEGER,
	    FOREIGN KEY (userID) REFERENCES login(userID),
	    FOREIGN KEY (classID) REFERENCES class(classID),
	    PRIMARY KEY (userID, classID)
	)''')

	conn.commit()
	conn.close()

# Could put more in later
def main():
	createSchema()

if __name__ == "__main__":
	print("Running database creation script.")
	main()
