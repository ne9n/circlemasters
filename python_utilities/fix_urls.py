import os
from bs4 import BeautifulSoup
import glob

# Get all html files
html_files = glob.glob('**/*.html', recursive=True)

def make_relative(url, file_path):
    # Skip absolute URLs or ones starting with //
    if url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '//')):
        return url
        
    # Only fix root-relative paths
    if url.startswith('/'):
        # Calculate depth
        depth = file_path.count(os.sep)
        if depth == 0:
            return '.' + url
        else:
            return ('../' * depth) + url.lstrip('/')
            
    return url

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # Update hrefs (links, stylesheets)
        for tag in soup.find_all(href=True):
            old_href = tag['href']
            new_href = make_relative(old_href, file_path)
            if old_href != new_href:
                tag['href'] = new_href
                changed = True
                
        # Update srcs (images, scripts)
        for tag in soup.find_all(src=True):
            old_src = tag['src']
            new_src = make_relative(old_src, file_path)
            if old_src != new_src:
                tag['src'] = new_src
                changed = True
                
        # Update action (forms)
        for tag in soup.find_all(action=True):
            old_action = tag['action']
            new_action = make_relative(old_action, file_path)
            if old_action != new_action:
                tag['action'] = new_action
                changed = True
                
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
