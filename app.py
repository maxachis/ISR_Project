import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts, messages=messages)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    return projectpath

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        print(request.form)
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            #Here we could run the search and get results

            #Then we could modify this to return the search results
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))
    return render_template('create.html')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn