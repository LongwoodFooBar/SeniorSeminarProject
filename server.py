from flask import Flask, g, render_template, request, redirect, url_for, escape, session
import sqlite3
from hashlib import md5
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	SECRET_KEY="foobardongle",
	DATABASE="foobar.db",
	USERNAME="admin",
	PASSWORD="default"
))

def check_logged():
	if 'username' in session:
		return True
	return False

def connectDB():
	rv = sqlite3.connect(app.config['DATABASE'])
	#rv.row_factory = sqlite3.Row
	return rv

def getDB():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connectDB()
	return g.sqlite_db

@app.route('/')
def root():
	if 'username' in session:
		return redirect(url_for("courses"))
	return home()#redirect(url_for('home'))

#PLACEHOLDER
def home():
	return redirect(url_for('login'))

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
		print("%s %s %s %s %s" % (request.form['firstName'], request.form['lastName'], request.form['email'], password, request.form['type']))
		db.commit()
		session['username'] = request.form['email']
		session['password'] = request.form['password']
		session['type'] = request.form['type']
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
			cs = db.execute("SELECT title FROM class JOIN login on class.instructorID=login.userID WHERE login.email=?", (session['username'],)).fetchall()
			for i in range(len(cs)):
				cs[i] = list(cs[i])
				cs[i].append(db.execute("SELECT assignment.title FROM assignment JOIN class ON class.classID=assignment.classID WHERE class.title=?", (cs[i][0],)).fetchall())

			for c in cs:
				print(c)
			return render_template('courses.html', user=session['username'], courses=cs)
			
		elif utype[0][0] == 'STUDENT':
			cs = db.execute("SELECT title FROM class NATURAL JOIN takes NATURAL JOIN login WHERE login.email=?", (session['username'],)).fetchall()
			for c in cs:
				c = list(c)
				c.append(db.execute("SELECT assignment.title FROM assignment JOIN class ON class.classID=assignment.classID WHERE class.title=?", (c[0],)).fetchall())
				print(c)
			return render_template('courses.html', user=session['username'], courses=cs)
	return redirect(url_for('root'))

@app.route('/sandbox')
def sandbox():
	return redirect(url_for('courses'))

@app.route('/faq')
def faq():
	return redirect(url_for('courses'))

@app.route('/forgot')
def forgot():
	return redirect(url_for('root'))

@app.teardown_appcontext
def closeDB(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

if __name__ == "__main__":
	app.run()
