from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import pathlib
import requests
import re

#### Set up the initial connection
url = 'https://randomwalksbooth.org'
driver = webdriver.Firefox()
driver.get(url)
headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

#### Go through each location and add to Raw Data
locations = driver.find_elements('tag name', 'a')
raw_data_frame = pd.DataFrame(columns= ['rw_destination','rw_destination2' ,'email', 'hometown', 'undergrad_college'
                                        , 'undergrad_major', 'work_experience', 'booth_concentrations'
                                        , 'random_walk_1y', 'hobbies', 'fun_facts'])


for index, location in enumerate(locations):
    link = location.get_attribute('href')
    # exclude the email address + top-line links + family RW page
    if 'private' not in link:
        continue
    # clean up the link to extract the location
    clean_location = (re.findall(r'int\-(.+?)\.htm',link) or re.findall(r'dom\-(.+?)\.htm',link))[0]
    # click on the link and get the HTML of that page
    driver.get(link)
    result = requests.get(link, headers= headers).text
    # scrape the relevant data - the second table on the page has the trip leader data
    # within that table all after the first row contain data about a particular leader
    soup = BeautifulSoup(result, features= 'html.parser')
    trip_leader_overall = soup.findChildren('table')[1]
    each_leader_info = trip_leader_overall.findChildren('tr')[1:]
    # go through each leader and export details (stored in p)
    for row in each_leader_info:
        temp = [location, clean_location]
        cells = row.findChildren('p')
        for cell in cells:
            value = cell.string
            if value is None:
                continue
            else:
                temp.append(value)
        # add final data to dataframe
        # for initial version, skip leaders who don't have complete data
        try:
            raw_data_frame.loc[raw_data_frame.shape[0]] = temp
        except ValueError:
            print('skipping leader, missing information')
    driver.back()

driver.quit()


# Clean the data


# Export the data
raw_data_frame.to_csv('raw_uncleaned_data.csv')
