from flask import Flask, g, render_template, request, redirect, url_for, escape, session
from werkzeug.utils import secure_filename
import sqlite3
import os, sys, platform
from hashlib import md5
#added by ben
from datetime import date
today=date.today()
# end ben added stuff
print(today)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = (['cpp', 'h'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)
app.config.update(dict(
	SECRET_KEY="foobardongle",
	DATABASE="foobar.db",
	USERNAME="admin",
	PASSWORD="default",
))

def checkLogged():
	if 'username' in session:
		return True
	return False

def checkInstructor():
	db = getDB()
	instr = db.execute("SELECT * FROM login WHERE position='INSTRUCTOR' and email=?", (session['username'],)).fetchall()
	if instr:
		return True
	return False

def checkTeaches(courseID):
	db = getDB()
	instr = db.execute("SELECT * FROM class JOIN login ON login.userID=class.instructorID WHERE position='INSTRUCTOR' and email=? and classID=?", (session['username'], courseID)).fetchall()
	if instr:
		return True
	return False

def checkOwnsAssign(assignmentID):
	db = getDB()
	instr = db.execute("SELECT * FROM assignment JOIN class ON class.classID=assignment.classID JOIN login ON login.userID=class.instructorID WHERE login.email=? AND assignmentID=?", (session['username'], assignmentID)).fetchall()
	if instr:
		return True
	return False

#HAAAAAAAAH
#I'm not funny
def valiDate(unfdate):
	if unfdate[1] > "12":
		return False
	if ["01", "03", "05", "07", "08", "10", "12"].count(unfdate[1]):
		if unfdate[0] > "31":
			return False
	if ["04", "06", "09", "11"].count(unfdate[1]):
		if unfdate[0] > "30":
			return False
	if ["02"].count(unfdate[1]):
		if unfdate > "29":
			return False

	date = "%s-%s-%s" % (unfdate[2], unfdate[1], unfdate[0])
	if date < date.today:
		return False
	return True

def connectDB():
	rv = sqlite3.connect(app.config['DATABASE'])
	return rv

def getDB():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connectDB()
	return g.sqlite_db

def home():
	return redirect(url_for('root'))

def allowedFile(filename):
	return '.' in filename and filename.rsplit('.',1).lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
	if not checkLogged():
		return redirect(url_for('login'))
	return redirect(url_for("courses"))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		db = getDB()
		error = None
		validlogin = False

		password = md5(request.form['password'].encode('utf-8')).hexdigest()

		validlogin = db.execute('SELECT * FROM login WHERE email = ? AND password = ?', (request.form['username'], password)).fetchall()

		if validlogin:
			session['username'] = request.form['username']
			session['password'] = request.form['password']
			return redirect(url_for('courses'))
		else:
			emailexists = db.execute('SELECT * FROM login where email = ?', (request.form['username'],)).fetchall()
			if emailexists:
				error = "Password does not match"
			else:
				error = "Username is not registered"
			return render_template('login.html', loginerror=error)
	return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		db = getDB()
		error = None

		emailexists = db.execute('SELECT * FROM login WHERE email=?', (request.form['email'],)).fetchall()
		if emailexists:
			return render_template('signup.html', loginerror="That email is already registered")

		password = md5(request.form['password'].encode('utf-8')).hexdigest()

		db.execute('INSERT INTO login (firstName, lastName, email, password, position) VALUES (?, ?, ?, ?, ?)', (request.form['firstName'], request.form['lastName'], request.form['email'], password, request.form['type']))
		db.commit()
		session['username'] = request.form['email']
		session['password'] = request.form['password']
		session['type'] = request.form['type']
		userdir = r'./userdirs/%s' % request.form['email']
		if not os.path.exists(userdir):
			os.makedirs(userdir)
		return redirect(url_for('courses'))
	return render_template('signup.html')
@app.route('/logout')
def logout():
	if not checkLogged():
		return home()
	session.pop('username', None)
	return redirect(url_for('root'))

@app.route('/courses')
def courses():
	if checkLogged():
		db = getDB()
		utype = db.execute("SELECT position FROM login WHERE email=?", (session['username'],)).fetchall()
		if utype[0][0] == 'INSTRUCTOR':
			cs = db.execute("SELECT title, classID FROM class JOIN login on class.instructorID=login.userID WHERE login.email=?", (session['username'],)).fetchall()
			for i in range(len(cs)):
				cs[i] = list(cs[i])
				cs[i].append(db.execute("SELECT assignment.title, assignment.assignmentID FROM assignment JOIN class ON class.classID=assignment.classID WHERE class.title=?", (cs[i][0],)).fetchall())
			return render_template('professor.html', user=session['username'], courses=cs)
			
		elif utype[0][0] == 'STUDENT':
			cs = db.execute("SELECT title FROM class NATURAL JOIN takes NATURAL JOIN login WHERE login.email=?", (session['username'],)).fetchall()
			for i in range(len(cs)):
				cs[i] = list(cs[i])
				cs[i].append(db.execute("SELECT assignment.title, assignment.assignmentID FROM assignment JOIN class ON class.classID=assignment.classID WHERE class.title=?", (cs[i][0],)).fetchall())
			return render_template('courses.html', user=session['username'], courses=cs)
	return redirect(url_for('root'))

@app.route('/sandbox', methods=['GET', 'POST'])
def sandbox(code='', output=''):
	if not checkLogged():
		return home()
	code = ""
	output = ""
	filename = './userdirs/%s/sandbox.cpp' % session['username']
	ofilename = './userdirs/%s/outfile' % session['username']
	if request.method == 'POST':
		code = request.form['code']
		timeout = int(request.form['timeout'])
		codefile = open(filename, "w")
		codefile.write(code + '\n')
		codefile.close()
		if request.form['sandbox'] == 'compile':
			os.system('g++ -Wall ./userdirs/%s/sandbox.cpp -o ./userdirs/%s/sandbox 2> ./userdirs/%s/outfile' % (session['username'], session['username'], session['username']))
		elif request.form['sandbox'] == 'run':
			if platform.system() == 'Linux':
				exitstat = os.system('timeout %d ./userdirs/%s/sandbox > ./userdirs/%s/outfile' % (timeout, session['username'], session['username']))
				if os.WEXITSTATUS(exitstat) == 124:
					os.system('echo "Program timed out" > ./userdirs/%s/outfile' % (session['username'],))
			elif platform.system() == 'Darwin':
				exitstat = os.system('gtimeout %d ./userdirs/%s/sandbox > ./userdirs/%s/outfile' % (timeout, session['username'], session['username']))
				if os.WEXITSTATUS(exitstat) == 124:
					os.system('echo "Program timed out" > ./userdirs/%s/outfile' % (session['username'],))
			if os.path.exists("./userdirs/%s/sandbox" % (session['username'],)):
				os.remove("./userdirs/%s/sandbox" % (session['username'],))
		elif request.form['sandbox'] == 'save':
			pass
		elif request.form['sandbox'] == 'upload':
			if 'file' not in request.files:
				upfile = request.files['uploadfile']
			if upfile.filename == '':
				return render_template('sandbox.html', user=session['username'], code=code, output=output)
			filename = secure_filename(upfile.filename)
			userdir = 'userdirs/%s/' % session['username']
			upfile.save(os.path.join(userdir, "sandbox.cpp"))
			codefile = open(os.path.join(userdir, "sandbox.cpp"))
			code = codefile.read()
			return render_template('sandbox.html', user=session['username'], code=code, output=output)
	if os.path.exists(ofilename):
		opfile = open(ofilename, "r")
		output = opfile.read()
		opfile.close()
		os.remove(ofilename)
	if os.path.exists('./userdirs/%s/sandbox' % (session['username'],)):
		os.remove('./userdirs/%s/sandbox' % (session['username'],))
	if os.path.exists(filename):
		cfile = open(filename, "r")
		code = cfile.read()
		cfile.close()
	return render_template('sandbox.html', user=session['username'], code=code, output=output)

@app.route('/faq')
def faq():
	if not checkLogged():
		return home()
	return render_template('faq.html', user=session['username'])

@app.route('/test', methods=["GET", "POST"])
def test():
	if not checkLogged():
		return home()
	if request.method == "POST":
		db = getDB()
		userID = db.execute("SELECT userID FROM login WHERE email=?", (session['username'],)).fetchall()[0][0]
		print(userID)
		inpV = request.form['input']
		outV = request.form['output']
		print(inpV)
		print(outV)
		db.execute("INSERT INTO testCases(inputValue, outputValue, userID, type) VALUES(?, ?, ?, 'PRIVATE')", (inpV, outV, userID))
		db.commit()
	db = getDB()
	cases = db.execute("SELECT inputValue, outputValue FROM testCases JOIN login ON login.userID=testCases.userID WHERE testCases.type='PUBLIC' OR testCases.type='private' AND login.email=?", (session['username'],)).fetchall()
	return render_template('testCases.html', user=session['username'], cases = cases)

@app.route('/about')
def about():
	if not checkLogged():
		return home()
	return render_template('about.html', user=session['username'])

@app.route('/create', methods=['GET', 'POST'])
def create():
	if not checkLogged():
		return home()
	if not checkInstructor():
		return home()
	if request.method == 'POST':
		db = getDB()
		title = request.form['title']
		secNum = request.form['secNumber']
		semester = request.form['semester']
		year = request.form['courseYear']
		instructorID = db.execute("SELECT userID FROM login WHERE email=?", (session['username'],)).fetchall()
		db.execute("INSERT INTO class(instructorID, title, section, semester, year) VALUES(?, ?, ?, ?, ?)", (instructorID[0][0], title, secNum, semester, year))
		db.commit()
		names = request.form['listStudent']
		if ', ' in names:
			names = names.split(', ')
			if names:
				for name in names:
					studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
					if studentID:
						takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
					else:
						takes = 1
					if not takes:
						db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (courseID, studentID[0][0]))
		elif ',' in names:
			names = names.split(',')
			if names:
				for name in names:
					studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
					if studentID:
						takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
					else:
						takes = 1
					if not takes:
						db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (courseID, studentID[0][0]))
		elif names:
				name = names
				studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
				if studentID:
					takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
				else:
					takes = 1
				if not takes:
					db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (courseID, studentID[0][0]))
		db.commit()
		return redirect(url_for('courses'))
	return render_template('addcourse.html', user=session['username'])

@app.route('/editCourse/<int:courseID>', methods=['GET', 'POST'])
def editCourse(courseID):
	if not checkLogged():
		return home()
	if not checkInstructor():
		return home()
	if not checkTeaches(courseID):
		return home()
	db = getDB()
	if request.method == 'POST':
		title = request.form['title']
		secNum = request.form['secNumber']
		semester = request.form['semester']
		year = request.form['courseYear']
		db.execute('UPDATE class SET title=?, section = ?, semester = ?, year = ? WHERE classID=?', (title, secNum, semester, year, courseID))
		instructorID = db.execute("SELECT userID FROM login WHERE email=?", (session['username'],)).fetchall()
		names = request.form['listStudent']
		if ', ' in names:
			names = names.split(', ')
			if names:
				for name in names:
					studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
					if studentID:
						takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
					else:
						takes = 1
					if not takes:
						db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (courseID, studentID[0][0]))
		elif ', ' in names:
			names = names.split(',')
			if names:
				for name in names:
					studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
					if studentID:
						takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
					else:
						takes = 1
					if not takes:
						db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (courseID, studentID[0][0]))
		elif names:
				name = names
				studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
				if studentID:
					takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
				else:
					takes = 1
				if not takes:
					db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (courseID, studentID[0][0]))

		names = request.form['deleteStudent']
		if ', ' in names:
			names = names.split(', ')
			if names:
				for name in names:
					studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
					if studentID:
						takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
					else:
						takes = 0
					if takes:
						db.execute('DELETE FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0]))
		elif ',' in names:
			names = names.split(',')
			if names:
				for name in names:
					studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
					if studentID:
						takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
					else:
						takes = 0
					if takes:
						db.execute('DELETE FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0]))
		elif names:
				name = names
				studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
				if studentID:
					takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
				else:
					takes = 0
				if takes:
					db.execute('DELETE FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0]))
		db.commit()
		return redirect(url_for('courses'))
	info = db.execute('SELECT * FROM class WHERE classID=?', (courseID,)).fetchall()
	students = db.execute("SELECT firstName, lastName, email FROM login JOIN takes ON takes.userID=login.userID WHERE takes.classID=?", (courseID,)).fetchall()
	return render_template('editcourse.html', user=session['username'], title=info[0][2], secNum=info[0][3], year=info[0][5], sem=info[0][4], students = students)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
	if request.method == "POST":
		email = request.form['username']
		password = request.form['password']
		pw = md5(password.encode('utf-8')).hexdigest()
		db = getDB()
		db.execute("UPDATE login SET password = ? WHERE email = ?", (pw, email))
		db.commit()
		return redirect(url_for('root'))
	return render_template('forgotpw.html')

@app.route('/assignments/<int:assignmentID>', methods=["GET", "POST"])
def assignmentsID(assignmentID):
	if not checkLogged():
		return home()
	db = getDB()

	if request.method == "POST":
		pass

	a = list(db.execute("SELECT * FROM assignment WHERE assignmentID = ?", (assignmentID,)).fetchall())
	unfdate = a[0][4]
	unfdate = unfdate.split("-")
	date = "%s/%s/%s" % (unfdate[2], unfdate[1], unfdate[0])
	return render_template("assignment.html", user=session['username'], title = a[0][1], body = a[0][2], date = date)

@app.route('/createAssignment/<int:courseID>', methods=['GET', 'POST'])
def createAssignment(courseID):
	if not checkLogged():
		return home()
	if not checkInstructor():
		return home()
	if request.method == 'POST':
		db = getDB()
		title = request.form['title']
		body = request.form['assignmentDesc']
		undate = request.form['dueDate']
		unfdate = undate.split("/")
		if len(unfdate[0]) == 1:
			unfdate[0] = "0" + unfdate[0]
		if len(unfdate[1]) == 1:
			unfdate[1] = "0" + unfdate[1]
		if not valiDate(unfdate):
			return render_template('createassignment.html', title = title, body = body, date = undate, error = "Bad Date")
		date = "%s-%s-%s" % (unfdate[2], unfdate[1], unfdate[0])
		db.execute("INSERT INTO assignment(classID, title, body, dueDate) VALUES(?, ?, ?, ?)", (courseID, title, body, date))
		db.commit()
		return redirect(url_for('courses'))
	return render_template('createassignment.html', user=session['username'])

@app.route('/editAssignment/<int:assignmentID>', methods=['GET', 'POST'])
def editAssignment(assignmentID):
	if not checkLogged():
		return home()
	if not checkInstructor():
		return home()
	if not checkOwnsAssign(assignmentID):
		return home()
	db = getDB()
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['assignmentDesc']
		unfdate = request.form['dueDate']
		unfdate = undate.split("/")
		if len(unfdate[0]) == 1:
			unfdate[0] = "0" + unfdate[0]
		if len(unfdate[1]) == 1:
			unfdate[1] = "0" + unfdate[1]
		if not valiDate(unfdate):
			return render_template('editassignment.html', title = title, body = body, date = undate, error = "Bad Date")
		date = "%s-%s-%s" % (unfdate[2], unfdate[1], unfdate[0])
		db.execute("UPDATE assignment SET title = ?, body = ?, dueDate=? WHERE assignmentID = ?", (title, body, date, assignmentID))
		db.commit()
		return redirect(url_for('courses'))
	info = db.execute("SELECT * FROM assignment WHERE assignmentID = ?", (assignmentID,)).fetchall()
	unfdate = info[0][4]
	unfdate = unfdate.split("-")
	date = "%s/%s/%s" % (unfdate[2], unfdate[1], unfdate[0])
	return render_template('editassignment.html', title = info[0][1], body = info[0][2], date = date)

@app.teardown_appcontext
def closeDB(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

if __name__ == "__main__":
	app.run()
