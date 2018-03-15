from flask import Flask, g, render_template, request, redirect, url_for, escape, session
import sqlite3
app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")
    #return "Login Page"

@app.route('/signup')
def signup():
    return "Signup Page"

@app.route('/logout')
def logout():
    return "Logout Page"

@app.route('/courses')
def courses():
    return "Courses Page"

