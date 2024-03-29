from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()