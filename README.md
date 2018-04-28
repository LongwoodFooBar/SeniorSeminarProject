# FooBar++

![FooBar++](static/logo.svg "FooBar++")

## What is it?
This is a project created by students of Longwood University for Computer Science 461: Senior Capstone.

It is a web-based system for Computer Science 160 and 162 students to test their code for projects and for instructors to assign work. Students will be able to work in a safe, sandbox environment. This system is built around operation on an internal network.

This application is intended to be run on Linux / UNIX-based machines. We do not support the use of this application on Windows.

## Dependencies
* Python 3
* Flask for Python 3
* SQLite3

## Additional Dependencies on OS X
* coreutils

## How to Operate it
### Manual
 ```bash
	python3 Create_Database.py
	export FLASK_APP=server.py
	python3 -m flask run --host 0.0.0.0 -p 7777
```
This will create an empty database and run the server on port 7777 and make the server visible to the entire local network.

### Automatic
* Create the database - `./createDB.sh`
* Run the application - `./runserver.sh`

This will create the database, populate it with sample accounts, and run the server on port 7777 and make the server visible to the local network.

## Usage
Users can connect to the application by navigating in their browser to '\<hostname\>:7777'. 

Every user will need to create an account initially. The two types of accounts are instructor and student. 

After completing the signup, the user should be redirected to their courses page. Students will not be registered for any classes initially. A professor will need to create a course and add students by their signin email. Professors should only have the option to create a new course.

The pages that are the same regardles of account type are:
* Login
	
    This page is self-explanatory and does not require an account to view.

* Signup
	
    This page is also self-explanatory and does not require an account to view.

* Courses
	
    Each user will be able to see the courses they are registered for in the system, whether they are teaching or taking the course.

* About
	
    The about page contains information about the course, project, and team members.

* FAQ
	
    The FAQ page contains information about issues that are common enough and need to be addressed. This should be populated as more issues arise.

* Forgot Password
	
    This page allows users to change their password assuming they correctly answer their security question.

* Sandbox
	
    The sandbox allows users to practice their programming or test out bits of code that they have written.

### Instructor
Instructors have the ability to create courses, edit courses, add students to and remove students from courses, create and edit assignments, and create test cases for assignments. They have access to the add course, edit course, create assignment, and edit assignment pages.

### Student


## Contributing
The project's development is limited to the team members of Longwood FooBar until the end of the spring semester of 2018.