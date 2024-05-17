from flask import Flask, render_template, request, redirect, url_for, jsonify,flash,session
import psycopg2
import os
import psycopg2.extras
from mail import send
import random

url = 'postgresql://virat:M-XHGEWhfKDhPH3wRU1bJw@glade-gerbil-4715.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full'
conn = psycopg2.connect(url)



app = Flask(__name__)

def create_tables():
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    cursor.execute('create table if not exists users(username varchar(255),password varchar(255),email varchar(255),phone int)')
    conn.commit()
    cursor.close()
    conn.close()

create_tables()

def validate_login(username, password):
    if not username or not password:
        flash('Username and password are required.', 'error')
        return False
    return True



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/already_present')
def already_present():
    return render_template('already_present.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    existing_user = cursor.fetchone()
    cursor.execute('SELECT * FROM users where password = %s',(password,))
    existing_password = cursor.fetchone()
    if existing_user and existing_password:
        flash('user already exists')
        return redirect(url_for('home'))
    else:
        conn.commit()
        flash('user not present')
        cursor.close()
        conn.close()
        return render_template('signup.html')


@app.route('/signup',methods = ['POST'])
def signup():
    return render_template('signup.html')

@app.route('/user',methods = ['POST'])
def user():
    user = request.form['user']
    
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM users WHERE username = %s',(user,))
    val = random.randint(1000,9999)
    session['val'] = val
    session['username'] = user
    send(val,cursor.fetchone())
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('otp.html')
    


val = 0
@app.route('/forgot',methods=['POST','GET'])
def forgot_password():
    if request.method == 'POST':
        return render_template('user.html')
    else:
        return "Method not allowed",405

@app.route('/OTP',methods = ['POST'])
def OTP():
    val = session.get('val')
    p = request.form['OTP']
    print(int(p),val)
    remaining_time = request.form.get('remaining_time')
    if int(p) == val and int(remaining_time)>0:
        return render_template('home.html')
    else:
        if int(remaining_time)>0:
            return render_template('otp.html', message='Invalid OTP. Please try again.')
        else:
            return render_template('otp.html', message='OTP has expired')


characters_check = {'@', '#', '$', '%', '&'}

@app.route('/signin',methods = ['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    email = request.form['Email']
    phone = request.form['Phone']
    if not validate_login(username, password):
        return redirect(url_for('signup'))
    if len(password)<12 or not any(char in password for char in characters_check):
        return render_template('signup.html',message = "This password is not strong")
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    cursor.execute('SELECT email from users where username = %s',(username,))
    user1 = cursor.fetchone()
    if user1:
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('signup.html',message = "That username already exists try a different one")
    else:
        cursor.execute('INSERT INTO users (username, password,email,phone) VALUES (%s, %s,%s,%s)', (username, password,email,phone))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('login.html')

@app.route('/resend_otp', methods=['POST'])
def resend_otp():
     # Assuming you have stored the username in the session
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    username = session.get('username')
    cursor.execute('SELECT email FROM users WHERE username = "%s"', (username,))
    val = random.randint(1000, 9999)
    session['val'] = val
    recipient_email = cursor.fetchone()
    print(recipient_email)  # Add this line to check the value of recipient_email
    send(val, recipient_email)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('otp.html')


if __name__ == '__main__':
    app.run(debug=True)
