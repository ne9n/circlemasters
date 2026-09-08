import glob
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning
import re
import os

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def make_relative(url, file_path):
    if not url or url.startswith(('mailto:', 'tel:', 'javascript:', '#')):
        return url
    
    # Strip circlemasters domain
    if url.startswith('http://www.circlemasters.com'):
        url = url.replace('http://www.circlemasters.com', '')
    if url.startswith('https://www.circlemasters.com'):
        url = url.replace('https://www.circlemasters.com', '')
        
    if not url.startswith('/'):
        # It was already relative or absolute pointing somewhere else
        return url
        
    # Calculate depth
    depth = file_path.count(os.sep)
    if depth == 0:
        return url.lstrip('/') if url.startswith('/') else url
    else:
        return ('../' * depth) + url.lstrip('/')

html_files = glob.glob('**/*.html', recursive=True)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # 1. Remove iframes pointing to weebly (comments form)
        for iframe in soup.find_all('iframe', src=re.compile(r'weebly\.com', re.IGNORECASE)):
            iframe.decompose()
            changed = True
            
        # 2. Remove spans/divs with onclick pointing to weebly (reply buttons)
        for tag in soup.find_all(['span', 'div', 'a'], onclick=re.compile(r'weebly\.com', re.IGNORECASE)):
            tag.decompose()
            changed = True

        # 3. Remove Facebook like buttons or any fb:like tags which have old URLs
        for fb in soup.find_all('fb:like'):
            parent = fb.parent
            fb.decompose()
            changed = True
            if parent and parent.name == 'div' and 'blog-social-item' in parent.get('class', []):
                parent.decompose()

        # 4. Fix absolute URLs to circlemasters to be relative
        for tag in soup.find_all(href=re.compile(r'circlemasters\.com', re.IGNORECASE)):
            old = tag['href']
            new_href = make_relative(old, file_path)
            if old != new_href:
                tag['href'] = new_href
                changed = True

        for tag in soup.find_all(src=re.compile(r'circlemasters\.com', re.IGNORECASE)):
            old = tag['src']
            new_src = make_relative(old, file_path)
            if old != new_src:
                tag['src'] = new_src
                changed = True
                
        # Update meta tags as well just to be thorough
        for tag in soup.find_all('meta', content=re.compile(r'circlemasters\.com', re.IGNORECASE)):
            old = tag['content']
            new_content = make_relative(old, file_path)
            if old != new_content:
                tag['content'] = new_content
                changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Cleaned {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

