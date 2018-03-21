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
			error = "Incorrect username or password"
			return render_template('login.html', loginerror=error)
	return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		db = getDB()
		error = None

		password = md5(request.form['password'].encode('utf-8')).hexdigest()

		#TODO Edit later to add type
		db.execute('INSERT INTO login (firstName, lastName, email, password, position) VALUES (?, ?, ?, ?, "STUDENT")', (request.form['firstName'], request.form['lastName'], request.form['email'], password))
		print("%s %s %s %s" % (request.form['firstName'], request.form['lastName'], request.form['email'], password))
		db.commit()
		session['username'] = request.form['email']
		session['password'] = request.form['password']
		return render_template('courses.html', user=session['username'])
	return render_template('signup.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('root'))

@app.route('/courses')
def courses():
	if check_logged():
		return render_template('courses.html', user=session['username'])
	return redirect(url_for('root'))

@app.teardown_appcontext
def closeDB(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

if __name__ == "__main__":
	app.run()
