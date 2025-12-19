from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Store requests in memory (Note: these vanish if you restart the app)
song_requests = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        song = request.form.get('song')
        artist = request.form.get('artist')
        message = request.form.get('message')
        
        if song and artist:
            # Add timestamp
            time_received = datetime.now().strftime("%H:%M")
            song_requests.insert(0, {'song': song, 'artist': artist, 'msg': message, 'time': time_received})
            return render_template('success.html')
            
    return render_template('index.html')

@app.route('/dj-dashboard')
def dashboard():
    # The DJ views this page to see the list
    return render_template('dashboard.html', requests=song_requests)

# Clear list feature for the DJ
@app.route('/clear')
def clear_list():
    song_requests.clear()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Render assigns a port automatically, so we must listen to it
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)