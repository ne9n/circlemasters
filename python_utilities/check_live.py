import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://www.circlemasters.com/plans-page.html"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read()
except Exception as e:
    print("Error fetching URL:", e)
    exit(1)

soup = BeautifulSoup(html, 'html.parser')
live_files = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'pdf' in href or 'zip' in href:
        filename = href.split('/')[-1]
        if filename not in live_files:
            live_files.append(filename)

print("Live files:", live_files)
