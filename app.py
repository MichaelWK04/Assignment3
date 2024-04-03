from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt=Bcrypt(app)

app.config['SECRET_KEY'] = '9ef34b5735d31c656503a4c799d71674c7e0b4e2fd255d2c91b3e381af5c81dc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
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
    sid=db.Column(db.Integer, primary_key = True, nullable = False)
    a1=db.Column(db.Integer, nullable = False)
    a2=db.Column(db.Integer, nullable = False)
    a3=db.Column(db.Integer, nullable = False)
    midterm=db.Column(db.Integer, nullable = False)
    final=db.Column(db.Integer, nullable = False)
    

    
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
        person = Instructor.query.filter_by(username = username).first()
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
        if username_exists:
            flash('Username \'' + username + '\' has already been taken! Please try again.', 'Error')
            return render_template('register.html')
        elif email_exists:
            flash('Email ' + email + ' has already been taken! Please try again.', 'Error')
            return render_template('register.html')
        username_exists = Instructor.query.filter_by(username = username).first()
        email_exists = Instructor.query.filter_by(email = email).first()
        if username_exists:
            flash('Username \'' + username + '\' has already been taken! Please try again.', 'Error')
            return render_template('register.html')
        elif email_exists:
            flash('Email ' + email + ' has already been taken! Please try again.', 'Error')
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

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if session['type']== 'Student':
        if request.method == 'GET':
            query_intructor_result = query_intructor()
            return render_template('feedback.html', query_intructor_result=query_intructor_result )
        else:
            query_intructor_result = query_intructor()
            username=request.form['InstructorName_ID']
            Instructor1 = Instructor.query.filter_by(username= username).first()
            if not Instructor1:
                flash('Please put in valid instructor name', 'Error')
                return render_template('feedback.html', query_intructor_result=query_intructor_result )
            else:
                feedback_details = (

                    request.form['InstructorName_ID'],
                    request.form['Ans1_ID'],
                    request.form['Ans2_ID'],
                    request.form['Ans3_ID'],
                    request.form['Ans4_ID']
                )
                add_feedback(feedback_details)
                message='Feedback has been received'
                return render_template('feedback.html', query_intructor_result=query_intructor_result, message=message)
    else:
        query_feedback_result=query_feedback()
        return render_template('Instructor_feedback.html', query_feedback_result=query_feedback_result)

        

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

@app.route('/grades', methods = ['GET', 'POST'])
def grades():
    if (session['type'] == 'Student'):
        student = db.session.query(Student).filter(Student.username == session['name'])
        grades = db.session.query(Mark).get(student[0].id)
        return render_template('student_grades.html', a1 = grades.a1, a2 = grades.a2, a3 = grades.a3, mid = grades.midterm, final = grades.final)
    else:
        if request.method == 'GET':
            grades = db.session.query(Mark)
            return render_template('instructor_grades.html', grades=grades)
        

def add_student(reg_details):
    user = Student(username = reg_details[0], email = reg_details[1], password = reg_details[2])
    db.session.add(user)
    db.session.commit()
    add_grades([user.id, -1, -1, -1, -1, -1])

def add_instructor(reg_details):
    user = Instructor(username = reg_details[0], email = reg_details[1], password = reg_details[2])
    db.session.add(user)
    db.session.commit()


def add_feedback(feedback_details):
        feedback = Feedback(to=feedback_details[0], q1= feedback_details[1], q2=feedback_details[2], q3=feedback_details[3], q4=feedback_details[4])
        db.session.add(feedback)
        db.session.commit()

def query_intructor():
    query_intructor=Instructor.query.all()
    return query_intructor

def query_feedback():
    name = session['name']
    query_feedback=Feedback.query.filter_by(to=name)
    return query_feedback

def add_grades(grades_details):
    grades = Mark(sid = grades_details[0], a1 = grades_details[1], a2 = grades_details[2], a3 = grades_details[3], midterm = grades_details[4], final = grades_details[5])
    db.session.add(grades)
    db.session.commit()

if __name__ == '__main__':
    app.run()