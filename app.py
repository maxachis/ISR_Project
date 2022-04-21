import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from backend import indeed, fakePythonJobs, simplyHired
import spacy

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
    # Send to backend
    jobTitle = request.form['jobTitle']
    jobLocation = request.form['jobLocation']
    websites = request.form.getlist('websites')
    # If Indeed, run Indeed backend
    if "indeed" in websites:
        indeed_results = indeed.get_indeed_results(jobTitle, jobLocation)
        for result in indeed_results:
            results.append({
                "Job Title": result['title'],
                "Company": result['company'],
                "Location": result['location'],
                "Link": result["link"],
                "Source": 'Indeed'
            })

    # If Glassdoor, run Glassdoor backend

    # If Simply Hired, run Simply Hired backend
    if "simplyHired" in websites:
        sh_results = simplyHired.get_simply_hired_results(jobTitle, jobLocation)
        for i in range (0, min(len(sh_results), 10)):
            sh_result = sh_results[i]
            results.append({
                "Job Title": sh_result['title'],
                "Company": sh_result['company'],
                "Location": sh_result['location'],
                "Link": sh_result["link"],
                "Source": 'Simply Hired'
            })

    # If Fake Python Jobs, run Fake Python Jobs Backend
    if "fakePythonJobs" in websites:
        fpj_results = fakePythonJobs.get_fake_python_jobs_results(jobTitle, jobLocation)
    for i in range(0, 10):
        fpj_result = fpj_results[i]
        results.append({
            "Job Title": fpj_result['title'],
            "Company": fpj_result['company'],
            "Location": fpj_result['location'],
            "Link": fpj_result["link"],
            "Source": 'Fake Python Jobs'
        })

    results = rank_by_sentence_similarity(jobTitle, results)

    return render_template('results.html', results=results)


def rank_by_sentence_similarity(query, results):
    nlp = spacy.load("en_core_web_md")
    qdoc = nlp(u'' + query)
    for i in range(len(results)):
        results[i]["Score"] = qdoc.similarity(nlp(u'' + results[i]['Job Title']))
    sorted_results = sorted(results, key=lambda d: d['Score'], reverse=True)
    return sorted_results


if __name__ == '__main__':
    app.run()
