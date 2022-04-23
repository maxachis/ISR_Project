import requests
from bs4 import BeautifulSoup


def extract(jobTitle, location):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}
    template = "https://www.simplyhired.com/search?q={}&l={}"
    url = template.format(jobTitle, location)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    count = 0
    divs = soup.find_all('div', class_='SerpJob-jobCard')
    for div in divs:
        a = div.find("a", class_ ="SerpJob-link")
        # TODO: Add the other components, like salary and description?
        # Job Card:
        job = {
            'link': "https://www.simplyhired.com/" + a['href'],
            'title': a.text.strip(),
            'company': div.find("span", class_ ="jobposting-company").text.strip(),
            'salary': "",
            'rating': "",
            'location': div.find("span", class_="jobposting-location").text.strip(),
            'date': "",
            'summary': ""
        }
        sh_joblist.append(job)
    return


sh_joblist = []
def get_simply_hired_results(jobTitle, jobLocation):
    sh_joblist = []
    position = jobTitle
    location = jobLocation
    # Extracting jobs from first 3 pages
    c = extract(position, location)
    transform(c)
    return sh_joblist