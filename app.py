from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Important for session management

# Replace with your girlfriend's actual username and a secure password
USERS = {'humera': '12042002'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            return redirect(url_for('countdown'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/countdown', methods=['GET', 'POST'])
def countdown():
    if not session.get('logged_in'):
        return redirect(url_for('login'))


    return render_template('countdown.html')

@app.route('/day_<int:day>')
def advent_day(day):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return render_template(f'day_{day}.html', day=day)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)