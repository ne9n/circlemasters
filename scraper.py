import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

START_URL = "https://www.circlemasters.com/"
DOMAIN = "www.circlemasters.com"

visited = set()
queue = [START_URL]

def download_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return None
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_html(url, html):
    parsed = urlparse(url)
    path = parsed.path

    if path == "" or path == "/":
        filename = "index.html"
    else:
        # remove leading slash
        filename = path.lstrip("/")
        if not filename.endswith(".html"):
            if "." not in filename:
                filename += ".html"
    
    # We might have paths like /folder/page.html, handle directories
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved {url} to {filename}")

while queue:
    current_url = queue.pop(0)
    
    # normalize url to avoid duplicate visits with/without trailing slash
    normalized_url = current_url.split("#")[0] # remove fragments
    
    if normalized_url in visited:
        continue
        
    visited.add(normalized_url)
    print(f"Visiting {normalized_url}...")
    
    html = download_page(normalized_url)
    if not html:
        continue
        
    save_html(normalized_url, html)
    
    # parse links
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        
        # Avoid mailto, tel, javascript
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue
            
        full_url = urljoin(normalized_url, href)
        parsed = urlparse(full_url)
        
        if parsed.netloc == DOMAIN or parsed.netloc == "":
            if full_url.split("#")[0] not in visited and full_url.split("#")[0] not in queue:
                queue.append(full_url.split("#")[0])

print(f"Finished scraping. Visited {len(visited)} pages.")
