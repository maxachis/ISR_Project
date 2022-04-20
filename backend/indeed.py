import requests
from bs4 import BeautifulSoup


def extract(page, position, location):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}
    template = "https://www.indeed.com/jobs?q={}&l={}&start={}&vjk=1e89c3e956dc949b"
    url = template.format(position, location, page)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    count = 0
    divs = soup.find_all('div', id='mosaic-provider-jobcards')
    for i in divs:
        atag = i.find_all("a")

        for j in atag:
            # Get link:
            if j["href"].startswith("/pagead"):
                link = 'https://www.indeed.com' + j["href"]
                count += 1
                item = j.find('div', class_='job_seen_beacon')

                # Get title:
                i = 0
                container = item.find_all('span')
                title = container[0].text.strip()
                while title == 'new':
                    i += 1
                    title = container[i].text.strip()

                    # Get Comapany:
                company = item.find('span', class_='companyName').text.strip()

                # Get Salary:
                try:
                    sal = item.find('div', class_='attribute_snippet').text.strip()
                    if '$' in sal:
                        salary = sal
                    else:
                        salary = ""
                except:
                    salary = ''

                # Get Ratings:
                try:
                    rating = item.find('span', class_='ratingNumber').text.strip()
                except:
                    rating = ''

                # Get Location:
                location = item.find('div', class_='companyLocation').text.strip()

                # Get Job Posting Date:
                date = item.find('span', class_='date').text.strip()

                # Get summary
                try:
                    summary = item.find('li').text.strip()
                except:
                    summary = ""

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
def get_indeed_results(jobTitle, jobLocation):
    position = jobTitle
    location = jobLocation
    # Extracting jobs from first 3 pages
    for i in range(0, 40, 10):
        c = extract(i, position, location)
        transform(c)
    return joblist
    # for i in joblist:
    #     print(i)
    #     print("\n")