from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import pathlib



### Set up the initial connection
url = 'https://randomwalksbooth.org'
driver = webdriver.Firefox()
driver.get(url)

### Go through each location
n_trips = 0
locations = driver.find_elements('tag name', 'a')
for location in locations:
    link = location.get_attribute('href')
    # exclude the email address + top-line links + family RW page
    if 'private' not in link:
        continue
    n_trips += 1
    driver.get(link)
    driver.back()

driver.quit()
print(n_trips)

# soup = BeautifulSoup(raw_html, features= 'html.parser')
# print(soup)


# Scrape the data



# Format the data
