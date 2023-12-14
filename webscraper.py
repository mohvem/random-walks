from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import pathlib
import requests



#### Set up the initial connection
url = 'https://randomwalksbooth.org'
driver = webdriver.Firefox()
driver.get(url)
headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

#### Go through each location and add to Raw Data
locations = driver.find_elements('tag name', 'a')
n_trips = 0
raw_data_frame = pd.DataFrame(columns= ['rw_destination', 'leader_data_raw'])


for index, location in enumerate(locations):
    link = location.get_attribute('href')
    # exclude the email address + top-line links + family RW page
    if 'private' not in link:
        continue
    n_trips += 1
    # click on the link and get the HTML of that page
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
                temp.append(value)
        raw_data_frame.loc[raw_data_frame.shape[0]] = [location, ','.join(temp)]
    driver.back()

driver.quit()

# Format the data


# Export the data
raw_data_frame.to_csv('raw_uncleaned_data.csv')
