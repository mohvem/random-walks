from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import pathlib
import requests



# ### Set up the initial connection
url = 'https://randomwalksbooth.org'
driver = webdriver.Firefox()
driver.get(url)
headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
# ### Go through each location
locations = driver.find_elements('tag name', 'a')
n_trips = 0
trips = []
raw_data = []
for index, location in enumerate(locations):
    link = location.get_attribute('href')
    # exclude the email address + top-line links + family RW page
    if 'private' not in link:
        continue
    n_trips += 1
    # click on the link
    driver.get(link)
    result = requests.get(link, headers= headers).text
    # scrape the relevant data
    soup = BeautifulSoup(result, features= 'html.parser')
    trip_leader_overall = soup.findChildren('table')[1]
    each_leader_info = trip_leader_overall.findChildren('tr')[1:]
    for row in each_leader_info:
        temp = []
        cells = row.findChildren('p')
        for cell in cells:
            value = cell.string
            if value is None:
                continue
            else:
                trips.append(link)
                temp.append(value)
        raw_data.append(','.join(temp))
    driver.back()

driver.quit()
