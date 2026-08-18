import http.server
import socketserver
import threading
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

PORT = 8000
DIRECTORY = "c:/circlemasters/cm_web"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        pass # Suppress logging

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(1) # wait for server to start

# Now crawl
base_urls = [
    "http://localhost:8000/2024-club-newsletters.html",
    "http://localhost:8000/2025-2026-club-newsletters.html",
    "http://localhost:8000/2023-club-newsletters.html"
]

missing = []

for page in base_urls:
    r = requests.get(page)
    if r.status_code != 200:
        print(f"Failed to get {page}: {r.status_code}")
        continue
        
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http') and not href.startswith('http://localhost:8000'):
            continue # Skip external links
            
        full_url = urljoin(page, href)
        
        try:
            head_r = requests.head(full_url)
            if head_r.status_code == 404:
                missing.append((page, href, full_url))
        except Exception as e:
            print(f"Error checking {full_url}: {e}")

if not missing:
    print("No 404s found via HTTP server!")
else:
    for page, href, url in missing:
        print(f"404 Not Found: {href} (on {page.split('/')[-1]})")

