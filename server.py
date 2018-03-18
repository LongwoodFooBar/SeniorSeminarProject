from flask import Flask, g, render_template, request, redirect, url_for, escape, session
import sqlite3
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY="foobardongle"
))

def connect_db():
    pass

def get_db():
    pass

@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for("courses"))
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        validlogin = False
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        if session['username'] == "admin" and session['password'] == "foobar":
            validlogin = True

        if validlogin:
            return redirect(url_for('courses'))
        else:
            error = "Incorrect username or password"
            return render_template('login.html', loginerror=error)
    return render_template('login.html')
    #return "Login Page"

@app.route('/signup')
def signup():
    return "Signup Page"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
    #return "Logout Page"

@app.route('/courses')
def courses():
    return "Courses Page"

if __name__ == "__main__":
    app.run()
