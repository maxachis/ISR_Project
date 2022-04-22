import requests
from bs4 import BeautifulSoup


def extract(page, position, location):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}
    template = "https://www.linkedin.com/jobs/search?keywords={}&location={}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum={}"
    url = template.format(position, location, page)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    div = soup.find('div', class_='base-serp-page__content')
    items = div.find_all('li')
    for i in items:
        if i.find('a'):
            # Get link:
            atag = i.find('a')
            link = atag["href"]

            # Get title:
            try:
                title = i.find('span').text.strip()
            except:
                title = ''

            # Get company:
            try:
                c = i.find('h4')
                company = c.find('a').text.strip()
            except:
                company = ""

            # Get location:
            try:
                location = i.find('span', class_="job-search-card__location").text.strip()
            except:
                location = ''

            # Get summary:
            try:
                summary = i.find('span', class_='result-benefits__text').text.strip()
            except:
                summary = ''

            # Get date:
            try:
                date = i.find('time', class_='job-search-card__listdate').text.strip()
            except:
                date = ""

            # For linkedin salary and ranking is not given
            # To have same dictionary format salary and rating will be empty for linkedIn
            salary = ''
            rating = ''

        # Job Card:
        job = {
            'link': link,
            'title': title,
            'company': company,
            'salary': salary,
            'rating': rating,
            'location': location,
            'date': date,
            'summary': summary
        }
        joblist.append(job)
    return


joblist = []
def get_linkedin_results(jobTitle, jobLocation):
    position = jobTitle
    location = jobLocation
    # Extracting jobs from first 3 pages
    for i in range(0, 40, 10):
        c = extract(i, position, location)
        transform(c)
    return joblist
