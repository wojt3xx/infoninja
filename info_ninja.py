#!/usr/bin/env python

import subprocess
import argparse
from bs4 import BeautifulSoup
import requests
import datetime
import re

# installing missing modules
try:
    import bs4
except ImportError:
    # If the module is not installed, run the 'pip install' command
    subprocess.call(['pip', 'install', 'bs4'])

# create an ArgumentParser object
parser = argparse.ArgumentParser(description='InfoNinja website crawler')

# add a positional argument for the URL
parser.add_argument('url', type=str, help='URL to crawl')

# parse the command line arguments
args = parser.parse_args()

# set parameters
url = args.url
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract email addresses using regular expressions
emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)

# Get the current date and time in a format suitable for a file name
current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

# Construct the file name using the current date and time and the URL
filename = f'{current_time}-{re.sub(r"https?://", "", url).replace("/", "_")}.txt'

# Open the file and write data to it
with open(filename, 'w') as f:
    f.write(f'Email addresses found on {url}:\n')
    for email in emails:
        f.write(email + '\n')
    f.write(f'\nLinks found on {url}:\n')
    for link in soup.find_all('a'):
        f.write(link.get('href') + '\n')

print("Crawling done. Enjoy!")
