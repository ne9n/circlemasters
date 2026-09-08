import glob
import os
import urllib.parse
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def get_relative_path(from_file, to_url):
    # Handle already relative links or external links
    if not to_url.startswith('/'):
        return to_url
        
    # Remove leading slash
    to_url = to_url.lstrip('/')
    
    # If the URL is empty (was just '/'), it points to index.html
    if not to_url:
        to_url = 'index.html'
    # If the URL doesn't have an extension and doesn't end with a slash, assume it's an html file
    elif '.' not in to_url.split('/')[-1] and not to_url.endswith('/'):
        to_url += '.html'
        
    # Calculate depth of current file to create relative path
    depth = len(from_file.replace('\\', '/').split('/')) - 1
    
    if depth == 0:
        return './' + to_url
    else:
        return '../' * depth + to_url

html_files = glob.glob('**/*.html', recursive=True)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # 1. Add border/margin to the body
        # We can add a global style block
        if not soup.find(id="global-layout-styles"):
            style_tag = soup.new_tag('style', id="global-layout-styles")
            style_tag.string = "body { max-width: 1200px; margin: 0 auto; padding: 0 20px; box-sizing: border-box; }"
            if soup.head:
                soup.head.append(style_tag)
                changed = True
        
        # 2. Fix broken www.circlemasters.com links
        for a in soup.find_all('a', href=True):
            href = a['href']
            original_href = href
            
            if href.startswith('www.circlemasters.com'):
                href = href.replace('www.circlemasters.com', '')
                if not href.startswith('/'):
                    href = '/' + href
                
                # Convert the root-relative path to a file-relative path
                href = get_relative_path(file_path, href)
                a['href'] = href
                changed = True
                
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
