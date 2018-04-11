from flask import Flask, g, render_template, request, redirect, url_for, escape, session
from werkzeug.utils import secure_filename
import sqlite3
import os
from hashlib import md5
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	SECRET_KEY="foobardongle",
	DATABASE="foobar.db",
	USERNAME="admin",
	PASSWORD="default",
))

#BEN WAS HERE 
#       db= database......    
#       def upload():
#           file=request.files['inputFile']
#           newFile=FileContents(name=file.filename,data=file.read())
#           db.session.add(newFile)
#           db.session.commit()
#       def download():
#           file_data=FileContents.query.filter_by(id=1).first()
#           return send_file(BytesIO(file_data.data), attachment_filename='example.pdf',as_attachment=true)
# 
#  
#
def check_logged():
	if 'username' in session:
		return True
	return False

def check_instructor():
	db = getDB()
	instr = db.execute("SELECT * FROM login WHERE position='INSTRUCTOR' and email=?", (session['username'],)).fetchall()
	if instr:
		return True
	return False

def connectDB():
	rv = sqlite3.connect(app.config['DATABASE'])
	return rv

def getDB():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connectDB()
	return g.sqlite_db

def home():
	return redirect(url_for('login'))

@app.route('/')
def root():
	if not check_logged():
		return home()
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
		return render_template('courses.html', user=session['username'])
	return render_template('signup.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('root'))

@app.route('/courses')
def courses():
	if check_logged():
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
def sandbox():
	if not check_logged():
		return home()
	if request.method == 'POST':
		code = request.form['code']
		timeout = int(request.form['timeout'])
		filename = './userdirs/%s/sandbox.cpp' % session['username']
		ofilename = './userdirs/%s/outfile' % session['username']
		codefile = open(filename, "w")
		codefile.write(code + '\n')
		codefile.close()
		cpid = os.fork()
		if cpid == 0:
			if request.form['sandbox'] == 'compile':
				os.system('g++ ./userdirs/%s/sandbox.cpp -o ./userdirs/%s/sandbox 2> ./userdirs/%s/outfile' % (session['username'], session['username'], session['username']))
			#os.system('g++ ./userdirs/%s/sandbox.cpp -o ./userdirs/%s/sandbox 2> ./userdirs/%s/outfile && timeout %d ./userdirs/%s/sandbox >> ./userdirs/%s/outfile' % (session['username'], session['username'], session['username'], timeout, session['username'], session['username']))
				os._exit(0)
			elif request.form['sandbox'] == 'run':
				os.system('timeout %d ./userdirs/%s/sandbox > ./userdirs/%s/outfile' % (timeout, session['username'], session['username']))
				os._exit(0)
			elif request.form['sandbox'] == 'save':
				os._exit(0)
			elif request.form['sandbox'] == 'upload':
				if 'file' not in request.files:
					os._exit(0)
				upfile = request.files['file']
				if upfile.filename == '':
					os._exit(0)
				if upfile and isCPP(upfile.filename):
					filename = secure_filename(upfile.filename)
					userdir = './userdirs/%s/' % session['username']
					upfile.save(os.path.join(userdir, filename))
					codefile = open(os.path.join(userdir, filename))
					code = codefile.read()
					os._exit(0)
		os.waitpid(cpid, 0)
		opfile = open(ofilename, "r")
		output = opfile.read()
		opfile.close()
		return render_template('sandbox.html', user=session['username'], code=code, output=output)
	return render_template('sandbox.html', user=session['username'])

@app.route('/faq')
def faq():
	if not check_logged():
		return home()
	return render_template('faq.html', user=session['username'])

@app.route('/test')
def test():
	if not check_logged():
		return home()
	return render_template('testCases.html', user=session['username'])

@app.route('/about')
def about():
	if not check_logged():
		return home()
	return render_template('about.html', user=session['username'])

@app.route('/create', methods=['GET', 'POST'])
def create():
	if not check_logged():
		return home()
	if not check_instructor():
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
		names = names.split(', ')
		if names[0] != '':
			print(names)
			for name in names:
				studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
				print(studentID)
				classID = db.execute("SELECT classID FROM class WHERE instructorID = ? and title = ? and section = ? and semester = ? and year = ?", (instructorID[0][0], title, secNum, semester, year)).fetchall()
				print(classID)
				takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (classID[0][0], studentID[0][0])).fetchall()
				if not takes:
					db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (classID[0][0], studentID[0][0]))
		db.commit()
	return render_template('addcourse.html', user=session['username'])

#edit a course page
@app.route('/editCourse/<int:courseID>', methods=['GET', 'POST'])
def editCourse(courseID):
	if not check_instructor():
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
		names = names.split(', ')
		if names[0] != '':
			for name in names:
				studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
				takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
				if not takes:
					db.execute('INSERT INTO takes(classID, userID) VALUES(?, ?)', (classID[0][0], studentID[0][0]))
		names = request.form['deleteStudent']
		names = names.split(', ')
		if names[0] != '':
			for name in names:
				studentID = db.execute("SELECT userID FROM login WHERE email=?", (name,)).fetchall()
				classID = db.execute("SELECT classID FROM class WHERE instructorID = ? and title = ?", (instructorID[0][0], title)).fetchall()
				takes = db.execute('SELECT * FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0])).fetchall()
				if takes:
					db.execute('DELETE FROM takes WHERE classID = ? and userID = ?', (courseID, studentID[0][0]))
		db.commit()
	info = db.execute('SELECT * FROM class WHERE classID=?', (courseID,)).fetchall()
	return render_template('editcourse.html', user=session['username'], title=info[0][2])

@app.route('/forgot')
def forgot():
	return render_template('forgotpw.html')

@app.route('/assignments')
def assignments():
	if not check_logged():
		return home()
	return "Assignments"

@app.route('/assignments/<int:assignmentID>')
def assignmentsID(assignmentID):
	if not check_logged():
		return home()
	db = getDB()
	a = list(db.execute("SELECT * FROM assignment WHERE assignmentID = ?", (assignmentID,)).fetchall())
	return "<h1>%s</h1><p>%s</p>" % (a[0][1], a[0][2])

@app.route('/createAssignment/<int:courseID>', methods=['GET', 'POST'])
def createAssignment(courseID):
	if not check_logged():
		return home()
	if not check_instructor():
		return home()
	if request.method == 'POST':
		db = getDB()
		title = request.form['title']
		body = request.form['assignmentDesc']
		date = request.form['dueDate']
		print(date)
		db.execute("INSERT INTO assignment(classID, title, body, dueDate) VALUES(?, ?, ?, date(?))", (courseID, title, body, date))
		db.commit()
		return redirect(url_for('courses'))
	return render_template('createassignment.html', user=session['username'])

@app.route('/editAssignment/<int:assignmentID>', methods=['GET', 'POST'])
def editAssignment(assignmentID):
	db = getDB()
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['assignmentDesc']
		unfdate = request.form['dueDate']
		unfdate = unfdate.split("/")
		date = "%s-%s-%s" % (unfdate[2], unfdate[1], unfdate[0])
		db.execute("UPDATE assignment SET title = ?, body = ?, dueDate=date(?) WHERE assignmentID = ?", (title, body, date, assignmentID))
		db.commit()
		return render_template('editassignment.html', title = title, body = body)
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
