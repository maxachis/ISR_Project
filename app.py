from flask import Flask, render_template, request, url_for, flash, redirect
from backend import indeed, fakePythonJobs, simplyHired, linkedIn
import spacy
import geopy
import re
import math

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


def check_duplicate(result, results):
    # Assumption: Job is duplicate if title, company and location is same for any two jobs
    for job in results:
        title_exist = 0
        company_exist = 0
        location_exist = 0
        if result['title'] == job.get('Job Title'):
            title_exist = 1
        if result['company'] == job.get('Company'):
            company_exist = 1
        if result['location'] == job.get('Location'):
            location_exist = 1
        # Duplicate entry found
        if title_exist * company_exist * location_exist == 1:
            return (True)
    # No duplicates found
    else:
        return (False)


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
            is_duplicate = check_duplicate(result, results)
            if is_duplicate == False:
                results.append({
                    "Job Title": result['title'],
                    "Company": result['company'],
                    "Location": result['location'],
                    "Link": result["link"],
                    "Salary": result['salary'],
                    "Source": 'Indeed'
                })

    # If LinkedIn, run LinkedIn backend
    if "linkedin" in websites:
        li_results = linkedIn.get_linkedin_results(jobTitle, jobLocation)
        for i in range(0, min(len(li_results), 10)):
            li_result = li_results[i]
            is_duplicate = check_duplicate(li_result, results)
            if is_duplicate == False:
                results.append({
                    "Job Title": li_result['title'],
                    "Company": li_result['company'],
                    "Location": li_result['location'],
                    "Link": li_result["link"],
                    "Salary": li_result['salary'],
                    "Source": 'LinkedIn'
                })

    # If Simply Hired, run Simply Hired backend
    if "simplyHired" in websites:
        sh_results = simplyHired.get_simply_hired_results(jobTitle, jobLocation)
        for i in range(0, min(len(sh_results), 10)):
            sh_result = sh_results[i]
            is_duplicate = check_duplicate(sh_result, results)
            if is_duplicate == False:
                results.append({
                    "Job Title": sh_result['title'],
                    "Company": sh_result['company'],
                    "Location": sh_result['location'],
                    "Link": sh_result["link"],
                    "Salary": "",
                    "Source": 'Simply Hired'
                })

    # If Fake Python Jobs, run Fake Python Jobs Backend
    if "fakePythonJobs" in websites:
        fpj_results = fakePythonJobs.get_fake_python_jobs_results(jobTitle, jobLocation)
        for i in range(0, 10):
            fpj_result = fpj_results[i]
            is_duplicate = check_duplicate(fpj_result, results)
            if is_duplicate == False:
                results.append({
                    "Job Title": fpj_result['title'],
                    "Company": fpj_result['company'],
                    "Location": fpj_result['location'],
                    "Link": fpj_result["link"],
                    "Salary": "",
                    "Source": 'Fake Python Jobs'
                })
    if len(results) == 0:
        return render_template('no_results.html')
    results = rank_by_title_and_location_similarity(jobTitle, jobLocation, results)
    return render_template('results.html', results=results)


def rank_by_title_and_location_similarity(title, location, results):
    nlp = spacy.load("en_core_web_md")
    qdoc = nlp(u'' + title)
    results = get_location_distances(location, results)
    for i in range(len(results)):
        results[i]["Score"] = qdoc.similarity(nlp(u'' + results[i]['Job Title'])) + results[i]["DistScore"]
    sorted_results = sorted(results, key=lambda d: d['Score'], reverse=True)
    return sorted_results


def get_location_distances(location1, results):
    locator = geopy.Photon(user_agent="measurements")
    loc1 = locator.geocode(location1)
    for i in range(len(results)):
        # Because FakePythonJobs does not use actual locations, give all Fake Python Jobs results an arbitrarily long distance
        if results[i]['Source'] == 'Fake Python Jobs':
            results[i]['Distance'] = 200
        else:
            loc_orig = results[i]['Location']
            # Some Indeed sources use the phrase "remote in" in their location descriptions. Remove this.
            loc_orig = re.sub(".*[R|r]emote\sin\s", "", loc_orig)
            try:
                loc_clean = re.search('.*\,\s*\w{2}', loc_orig).group(0)
            except AttributeError:
                # Assume not in "City, ST" format. Keep going
                loc_clean = loc_orig
            loc2 = locator.geocode(loc_clean)
            results[i]['Location'] = loc_clean
            results[i]["Distance"] = math.dist([loc1.latitude, loc2.longitude], [loc2.latitude, loc2.longitude])
    maxDist = max(results, key=lambda x: x['Distance'])['Distance']
    for i in range(len(results)):
        results[i]["DistScore"] = 1 - results[i]['Distance'] / maxDist
    return results


if __name__ == '__main__':
    app.run()
