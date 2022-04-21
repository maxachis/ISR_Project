import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"

def get_fake_python_jobs_results(jobTitle, jobLocation):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    divs = soup.find_all('div', class_='card-content')
    results = []
    for div in divs:
        results.append({
            "link": div.find('a', text="Learn", class_='card-footer-item')["href"],
            "title": div.find('h2', class_="title is-5").text.strip(),
            "company": div.find('h3', class_="subtitle is-6 company").text.strip(),
            "location": div.find('p', class_="location").text.strip()
        })
    return results
