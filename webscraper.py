from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd


# Set up the initial connection
url = 'https://randomwalksbooth.org'
req = Request(url)
req.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
raw_html = urlopen(req).read()
soup = BeautifulSoup(raw_html, features= 'html.parser')

# Scrape the data



# Format the data
