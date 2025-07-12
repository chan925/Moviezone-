from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
MOVIES_JSON = 'movies.json'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load existing movies
def load_movies():
    if not os.path.exists(MOVIES_JSON):
        return []
    with open(MOVIES_JSON, 'r') as f:
        return json.load(f)

# Save new movie
def save_movie(title, filename):
    movies = load_movies()
    movies.append({"title": title, "filename": filename})
    with open(MOVIES_JSON, 'w') as f:
        json.dump(movies, f, indent=2)

@app.route('/')
def index():
    movies = load_movies()
    return render_template('index.html', movies=movies)

@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    file = request.files['video']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        save_movie(title, file.filename)
    return redirect(url_for('index'))

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
