from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

users = {}
logs = []
feedbacks = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pin = request.form['pin']
        compartment = request.form['compartment']

        if username in users:
            flash('Username already exists.')
        else:
            users[username] = {
                'password': password,
                'pin': pin,
                'compartment': compartment
            }
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    compartment = users[username]['compartment']

    lockers = {
        "Common": "Locked",
        compartment: "Locked"
    }
    return render_template('dashboard.html', username=username,lockers=lockers)

@app.route('/toggle_locker', methods=['POST'])
def toggle_locker():
    if 'username' not in session:
        return redirect(url_for('login'))

    action = request.form.get('action')
    logs.append({
        'user': session['username'],
        'action': action,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    flash(f'Locker {action}ed successfully.')
    return redirect(url_for('dashboard'))

@app.route('/change_pin', methods=['GET', 'POST'])
def change_pin():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        old_pin = request.form['old_pin']
        new_pin = request.form['new_pin']

        if users[session['username']]['pin'] == old_pin:
            users[session['username']]['pin'] = new_pin
            flash('PIN changed successfully.')
        else:
            flash('Old PIN is incorrect.')

    return render_template('change_pin.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form['content']
        feedbacks.append({
            'user': session['username'],
            'content': content,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        flash('Feedback submitted successfully.')

    return render_template('feedback.html')

@app.route('/logs')
def logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('logs.html', logs=logs)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
