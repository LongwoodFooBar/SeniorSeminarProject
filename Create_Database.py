#!/usr/bin/env python3

import sqlite3
import sys

# Create the schema
def createSchema():
	conn = sqlite3.connect('masterDatabase.db')
	c = conn.cursor()

	# Creates the login table
	# Position used to denote teacher or student
	# password possibly stored as a hash?
	c.execute('''CREATE TABLE IF NOT EXISTS login (
		userID INTEGER,
		firstName TEXT,
		lastName TEXT,
		password TEXT,
		email TEXT,
		position TEXT,
		PRIMARY KEY (userID)
	)''')

	# Creates the class table
	# instructor is who is the main teacher (handles student teacher cases)
	c.execute('''CREATE TABLE IF NOT EXISTS class (
		classID INTEGER,
		userID INTEGER,
		instructor TEXT,
		PRIMARY KEY (classID),
		FOREIGN KEY (userID) REFERENCES login(userID)
	) ''')

	# Creates the assignment table
	# Mostly connects the tables together with the test cases along with searching
	c.execute('''CREATE TABLE IF NOT EXISTS assignment (
		assignmentID INTEGER,
		classID INTEGER,
		PRIMARY KEY (assignmentID, classID),
		FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID),
		FOREIGN KEY (classID) REFERENCES class(classID)
	) ''')

	# Creates the upload table
	# upload type refers to a test file or a handout/assignment
	c.execute('''CREATE TABLE IF NOT EXISTS uploads (
		userID INTEGER,
		assignmentID INTEGER,
		fileLocation TEXT,
		type TEXT,
		PRIMARY KEY (userID, assignmentID),
		FOREIGN KEY (userID) REFERENCES login(userID),
		FOREIGN KEY	(assignmentID) REFERENCES assignment(assignmentID)
	) ''')

	# Creates the test cases table
	# Type is to denote if test case is teacher, student, or secret
	# teacher can be used by class, student by individual or class, and secret for grading
	c.execute('''CREATE TABLE IF NOT EXISTS testCases (
		classID INTEGER,
		testID INTEGER,
		assignmentID INTEGER,
		inputValue TEXT,
		outputValue TEXT,
		userID INTEGER,
		type TEXT,
		PRIMARY KEY (testID),
		FOREIGN KEY (classID) REFERENCES class(classID),
		FOREIGN KEY (assignmentID) REFERENCES assignment(assignmentID),
		FOREIGN KEY (userID) REFERENCES login(userID)
	) ''')

	conn.commit()
	conn.close()

# Could put more in later
def main():
	createSchema()

if __name__ == "__main__":
	print("Running database creation script.")
	main()
