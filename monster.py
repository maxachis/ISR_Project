import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# https://www.monster.com/jobs/search?q=Information+Science+Engineer&where=Pittsburgh%2C+PA&page=3&so=m.u.sh

job_role = "Information Science Engineer"

where = "Pittsburgh, PA"

# Convert job_role and where to url

# Scrape
url = 'https://www.monster.com/jobs/search?q=Information+Science+Engineer&where=Pittsburgh%2C+PA&page=3&so=m.u.sh'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
title = []
for header in soup.findAll('h2', {'class': 'title'}):
    title.append(header.text.strip())


driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(5);
driver.get(url)
print(driver.title)
element = driver.find_element_by_class_name('iQztVR')
print(element.text)

delay = 3
job_titles = []
companies = []
locations = []
try:
    myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-cardstyle__JobCardTitle-sc-1mbmxes-2')))
    print("Page is ready!")
    time.sleep(3)
    myElem = driver.find_element_by_class_name('job-cardstyle__JobCardTitle-sc-1mbmxes-2')
    elements = driver.find_elements_by_css_selector(".job-cardstyle__JobCardTitle-sc-1mbmxes-2")
    for el in elements:
        job_titles.append(el.text)
    elements = driver.find_elements_by_css_selector(".job-cardstyle__JobCardCompany-sc-1mbmxes-3")
    for el in elements:
        companies.append(el.text)
    elements = driver.find_elements_by_css_selector(".job-cardstyle__JobCardDetails-sc-1mbmxes-5")
    for el in elements:
        locations.append(el.text)
    # print(myElem.get_attribute('outerHTML'))

    print(job_titles)
    print(len(job_titles))
    print(companies)
    print(len(companies))
    print(locations)
    print(len(locations))

except TimeoutException:
    print("Loading took too much time!")
print(driver.current_url)
driver.close()

