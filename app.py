from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt=Bcrypt(app)

app.config['SECRET_KEY'] = '9ef34b5735d31c656503a4c799d71674c7e0b4e2fd255d2c91b3e381af5c81dc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    username=db.Column(db.String(20), unique = True, nullable = False)
    email=db.Column(db.String(30), unique = True, nullable = False)
    password=db.Column(db.String(30), nullable = False)
    
class Instructor(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    username=db.Column(db.String(20), unique = True, nullable = False)
    email=db.Column(db.String(30), unique = True, nullable = False)
    password=db.Column(db.String(30), nullable = False)

class Feedback(db.Model):
    to=db.Column(db.String(20), primary_key = True, nullable = False)
    q1=db.Column(db.Text, primary_key = True, nullable = False)
    q2=db.Column(db.Text, primary_key = True, nullable = False)
    q3=db.Column(db.Text, primary_key = True, nullable = False)
    q4=db.Column(db.Text, primary_key = True, nullable = False)
    
class Mark(db.Model):
    assesment=db.Column(db.String(20), primary_key = True, nullable = False)
    mark=db.Column(db.Integer, primary_key = True, nullable = False)
    sid=db.Column(db.Integer, primary_key = True, nullable = False)

    
class Remark(db.Model):
    assesment=db.Column(db.String(20), primary_key = True, nullable = False)
    mark=db.Column(db.Integer, primary_key = True, nullable = False)
    sid=db.Column(db.Integer, primary_key = True, nullable = False)
    remark=db.Column(db.Text, nullable = False)

@app.route('/')
def home():
    pagename='home'
    return render_template('home.html', pagename=pagename)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('You Already logged in!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    username = request.form['Username']
    password = request.form['Password']
    person = Student.query.filter_by(username = username).first()
    if not person or not bcrypt.check_password_hash(person.password, password):
        if not person or not bcrypt.check_password_hash(person.password, password):
            flash('Please check your login details and try again.', 'Error')
            return render_template('login.html')
        else:
            student = False
    else:
        student = True
    if (student):
        session['type']='Student'
    else:
        session['type']='Instructor'
 
    session['name']=username
    session.permanent=True
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    session.pop('type', default = None)
    return redirect(url_for('home'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        username = request.form['Username']
        email = request.form['Email']
        type = request.form['Type']
        username_exists = Student.query.filter_by(username = username).first()
        email_exists = Student.query.filter_by(email = email).first()
        if username_exists or email_exists:
            flash('Username \'' + username + '\' has already been taken! Please try again.', 'Error')
            return render_template('register.html')
        username_exists = Instructor.query.filter_by(username = username).first()
        email_exists = Instructor.query.filter_by(email = email).first()
        if username_exists or email_exists:
            flash('Username \'' + username + '\' has already been taken! Please try again.', 'Error')
            return render_template('register.html')
        user_name_exists = Student.query.filter_by(email = email).first()
        email_exists = Student.query.filter_by(email = email).first()
        if user_name_exists or email_exists:
            flash('Username ' + email + ' has already been taken! Please try again.', 'Error')
            return render_template('register.html')
        user_name_exists = Instructor.query.filter_by(email = email).first()
        email_exists = Instructor.query.filter_by(email = email).first()
        if user_name_exists or email_exists:
            flash('Username ' + email + ' has already been taken! Please try again.', 'Error')
            return render_template('register.html')
        hashed_password=bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        reg_details =(username,
                    email,
                    hashed_password)
        if (type == 'Student'):
            add_student(reg_details)
        else:
            add_instructor(reg_details)
        flash('registration successful! Please login now:')
        return redirect(url_for('login'))

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/courseteam')
def courseteam():
    return render_template('courseteam.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/lab')
def lab():
    return render_template('lab.html')

@app.route('/lectures')
def lectures():
    return render_template('lectures.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/tests')
def tests():
    return render_template('tests.html')

def add_student(reg_details):
    user = Student(username = reg_details[0], email = reg_details[1], password = reg_details[2])
    db.session.add(user)
    db.session.commit()

def add_instructor(reg_details):
    user = Instructor(username = reg_details[0], email = reg_details[1], password = reg_details[2])
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    app.run()