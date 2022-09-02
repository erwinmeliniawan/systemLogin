from flask import Flask, render_template, redirect, request, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

#conection in mysql
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    alert = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        koneksi = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        koneksi.execute("SELECT * FROM accounts WHERE email=%s",(email,))
        user = koneksi.fetchone()
        koneksi.close()

        if user is None:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO accounts (username,email,password) VALUES (%s,%s,%s)",(name,email,hash_password))
            mysql.connection.commit()
            session['name']= name
            session['email']= email
            return redirect(url_for("home"))
        else:
            alert = 'Email has been used'
            return render_template("register.html", alert=alert)
    else:
        return render_template("register.html")

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), ])

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM accounts WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        print(f"User ==> {user}")

        if len(user) > 0:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['name'] = user['username']
                session['email'] = user['email']
                return render_template("home.html")
        else:
            return "Error password or user not match"
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")

           
if __name__ == '__main__':
    app.secret_key = "012#!terserah)(*^%"
    app.run(debug=True)

