from flask import Flask, render_template

app = Flask(__name__)

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