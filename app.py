import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)

# --- SECURITY CONFIGURATION ---
# 1. Set a secret key (needed for sessions to work)
app.secret_key = 'super_secret_dj_key' 

# 2. Set your DJ Password here
ADMIN_PASSWORD = "gsherwoodadmin" 

song_requests = []

BANNED_KEYWORDS = [
    "baby shark",
    "macarena",
    "chicken dance",
    "gangnam style",
    "despacito",
    "ymca",
    "cotton eye joe"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        song = request.form.get('song')
        artist = request.form.get('artist')
        message = request.form.get('message')
        
        if song and artist:
            full_request = (song + " " + artist).lower()
            for banned_word in BANNED_KEYWORDS:
                if banned_word in full_request:
                    return render_template('rejected.html')

            time_received = datetime.now().strftime("%H:%M")
            song_requests.insert(0, {'song': song, 'artist': artist, 'msg': message, 'time': time_received})
            return render_template('success.html')
            
    return render_template('index.html')

# --- NEW LOGIN ROUTE ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Check if password matches
        if request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Wrong password. Try again.'
    
    return render_template('login.html', error=error)

# --- PROTECTED DASHBOARD ROUTE ---
@app.route('/dj-dashboard')
def dashboard():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    return render_template('dashboard.html', requests=song_requests)

@app.route('/clear')
def clear_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    song_requests.clear()
    return redirect(url_for('dashboard'))

# Optional: Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

