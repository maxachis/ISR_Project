import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from backend import indeed


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]


@app.route('/')
def index():
    return render_template('search.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    results = []
    #Send to backend
    jobTitle = request.form['jobTitle']
    jobLocation = request.form['jobLocation']
    websites = request.form.getlist('websites')
    #If Indeed, run Indeed backend
    if "indeed" in websites:
        indeed_results = indeed.get_indeed_results(jobTitle, jobLocation)
        for result in indeed_results:
            results.append({
                "Job Title": result['title'],
                "Company": result['company'],
                "Location": result['location']
            })

    #If Glassdoor, run Glassdoor backend

    #Combine all results (TODO: Note which API they came from?)
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run()
















