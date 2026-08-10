import os
import glob
import urllib.request
from bs4 import BeautifulSoup
import re
import warnings
from bs4 import XMLParsedAsHTMLWarning
from urllib.error import HTTPError

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

html_files = glob.glob('**/*.html', recursive=True)

missing_urls = set()

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check img tags
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and 'uploads/' in src:
                missing_urls.add(src)
                
        # Check inline styles for background-image
        for tag in soup.find_all(style=True):
            style = tag['style']
            urls = re.findall(r'url\([\'"]?([^)\'"]+)[\'"]?\)', style)
            for u in urls:
                if 'uploads/' in u:
                    missing_urls.add(u)
                    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

downloaded = 0
failed = 0

print(f"Found {len(missing_urls)} potential image paths with 'uploads/'. Checking...")

for url in missing_urls:
    # Clean up the URL (remove query parameters for local filename)
    clean_url = url.split('?')[0]
    
    # Extract the absolute path from the relative path
    # e.g. ../uploads/9/0/9/8/9098310/img.jpg -> /uploads/9/0/9/8/9098310/img.jpg
    # or ./uploads/... -> /uploads/...
    idx = clean_url.find('uploads/')
    if idx == -1:
        continue
        
    abs_path = '/' + clean_url[idx:]
    local_path = abs_path.lstrip('/')
    
    # If it exists locally, skip
    if os.path.exists(local_path):
        continue
        
    # Download from www.circlemasters.com
    remote_url = 'http://www.circlemasters.com' + abs_path
    
    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Download
        req = urllib.request.Request(remote_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
            out_file.write(response.read())
        downloaded += 1
        print(f"Downloaded {local_path}")
    except HTTPError as e:
        failed += 1
        print(f"Failed to download {remote_url} - {e.code}")
    except Exception as e:
        failed += 1
        print(f"Failed to download {remote_url} - {e}")

print(f"Finished. Downloaded: {downloaded}, Failed: {failed}")
