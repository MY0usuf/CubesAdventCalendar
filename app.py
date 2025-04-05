from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Important for session management

# Replace with your girlfriend's actual username and a secure password
USERS = {'her_username': 'her_secure_password'}

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

    today = datetime.now()
    advent_start = datetime(today.year, 12, 1)
    if today < advent_start:
        time_until_advent = advent_start - today
        days = time_until_advent.days
        hours, remainder = divmod(time_until_advent.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return render_template('countdown.html', days=days, hours=hours, minutes=minutes, seconds=seconds)
    elif today.month == 12 and today.day <= 25:
        return redirect(url_for(f'day_{today.day}'))
    else:
        return render_template('countdown.html', message="Advent Calendar is over for this year!")

@app.route('/day_<int:day>')
def advent_day(day):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    today = datetime.now()
    if today.month == 12 and 1 <= day <= 25 and today.day >= day:
        # Here you'll render the content for the specific day
        return render_template(f'day_{day}.html', day=day)
    else:
        return render_template('countdown.html', message="You'll have to wait for that day!")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)